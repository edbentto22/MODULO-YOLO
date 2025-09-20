from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import base64, os, re, uuid
from typing import Optional

IMAGES_ROOT = os.path.abspath("./imagens")
os.makedirs(IMAGES_ROOT, exist_ok=True)

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8002")

DATA_URL_RE = re.compile(r"^data:(?P<mime>[\w\-\.+/]+);base64,(?P<b64>.+)$")
ALLOWED_MIMES = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}
MAX_SIZE_MB = 25

FILENAME_RE = re.compile(r"^(?P<registro>\d+)-(?P<ponto>\d+)\.(?P<ext>jpg|jpeg|png|webp)$", re.IGNORECASE)

class UploadIn(BaseModel):
    filename: str
    data_url: str
    registro: Optional[int] = None
    ponto: Optional[int] = None

app = FastAPI(title="Upload Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/imagens", StaticFiles(directory=IMAGES_ROOT), name="imagens")

def parse_data_url(data_url: str):
    m = DATA_URL_RE.match(data_url)
    if not m:
        raise HTTPException(status_code=400, detail="data_url inválido")
    mime = m.group("mime")
    b64 = m.group("b64")
    if mime not in ALLOWED_MIMES:
        raise HTTPException(status_code=400, detail=f"MIME não permitido: {mime}")
    try:
        binary = base64.b64decode(b64, validate=True)
    except Exception:
        raise HTTPException(status_code=400, detail="base64 inválido")
    if len(binary) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"Arquivo > {MAX_SIZE_MB}MB")
    return mime, binary


# Adiciona parâmetro opcional 'start' para iniciar a busca a partir de um índice específico
def next_sequential_name(dir_path: str, base_prefix: str, ext: str, start: int = 1) -> str:
    n = max(1, int(start))
    while True:
        candidate = f"{base_prefix}-{n}.{ext}"
        full = os.path.join(dir_path, candidate)
        try:
            with open(full, "xb") as f:
                f.write(b"")
            return candidate
        except FileExistsError:
            n += 1


@app.post("/upload")
async def upload(payload: UploadIn, request: Request):
    mime, binary = parse_data_url(payload.data_url)
    ext_by_mime = ALLOWED_MIMES[mime]
    filename = os.path.basename(payload.filename or f"upload.{ext_by_mime}")

    registro = payload.registro
    ponto = payload.ponto

    mfn = FILENAME_RE.match(filename.lower())
    if mfn:
        if registro is None:
            registro = int(mfn.group("registro"))
        if ponto is None:
            ponto = int(mfn.group("ponto"))

    if registro is None:
        dir_path = os.path.join(IMAGES_ROOT, "misc")
        os.makedirs(dir_path, exist_ok=True)
        base_prefix = uuid.uuid4().hex[:8]
    else:
        if not isinstance(registro, int) or registro < 0:
            raise HTTPException(status_code=400, detail="registro inválido")
        dir_path = os.path.join(IMAGES_ROOT, str(registro))
        os.makedirs(dir_path, exist_ok=True)
        base_prefix = str(registro)

    if ponto is not None and (not isinstance(ponto, int) or ponto < 0):
        raise HTTPException(status_code=400, detail="ponto inválido")

    if ponto is not None:
        # Se o arquivo com o ponto informado já existir, escolhe automaticamente o próximo livre
        tentative_name = f"{base_prefix}-{ponto}.{ext_by_mime}"
        full_path = os.path.join(dir_path, tentative_name)
        if os.path.exists(full_path):
            final_name = next_sequential_name(dir_path, base_prefix, ext_by_mime, start=ponto + 1)
            full_path = os.path.join(dir_path, final_name)
        else:
            final_name = tentative_name
    else:
        final_name = next_sequential_name(dir_path, base_prefix, ext_by_mime)
        full_path = os.path.join(dir_path, final_name)

    with open(full_path, "wb") as f:
        f.write(binary)

    if registro is None:
        rel_url = f"/imagens/misc/{final_name}"
    else:
        rel_url = f"/imagens/{registro}/{final_name}"

    link = f"{BASE_URL}{rel_url}"

    return {
        "link": link,
        "mime": mime,
        "size": len(binary),
        "registro": registro,
        "ponto": ponto,
        "path": rel_url,
    }