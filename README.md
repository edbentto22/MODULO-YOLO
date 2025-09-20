# MODULO-YOLO

Frontend estático + Backend FastAPI para pré-processamento de imagens com opção de redimensionamento 640x640 (YOLO-style letterbox), geração de links públicos e envio de payload.

## Funcionalidades
- Pré-processamento no navegador com opção de redimensionar para 640x640 (letterbox, preserva proporção).
- Conversão para JPEG (qualidade 0.9) no browser.
- Renomeação manual e automática (registro-sequencial.jpg).
- Geração de link público por imagem via endpoint de upload.
- Envio de payload com imagens inline (base64) ou somente links.
- Backend em FastAPI servindo uploads estáticos.
- Evita conflitos: backend auto-incrementa o nome quando o arquivo já existe.

## Requisitos
- Python 3.11+

## Instalação
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

## Execução
- Backend (FastAPI):
```bash
uvicorn app:app --host 127.0.0.1 --port 8002
```
- Frontend (http.server):
```bash
python3 -m http.server 8000
```
- Acesse a UI: http://localhost:8000/

## Configuração na UI
- Em "Gerar link público por imagem", use o endpoint:
  - http://127.0.0.1:8002/upload
- Em "Destino do Webhook", configure o seu endpoint de destino.
- Campo "Registro" opcional para organizar os uploads por pasta.
- Campo "Ponto": se preencher, o servidor garantirá nome único (auto-incrementa em caso de conflito).

## Variáveis de Ambiente
- BASE_URL: URL base para compor links públicos (padrão: http://127.0.0.1:8002)
  - Ex.: `export BASE_URL="https://api.seu-dominio.com"`

## Estrutura de Pastas
- `imagens/` (ignorada no Git):
  - `imagens/<registro>/registro-<n>.jpg`
  - `imagens/misc/<uuid>-<n>.jpg`

## Segurança
- CORS liberado para desenvolvimento (allow_origins=["*"]). Restrinja em produção.
- Em produção, defina BASE_URL para o domínio público do backend (HTTPS recomendado).

## Comandos Git sugeridos
```bash
git init
git checkout -b main || git branch -M main
git add .
git commit -m "feat: FastAPI upload + UI YOLO 640x640; link generation fix; auto-increment on conflict"
# Depois crie o repo vazio no GitHub e rode:
# git remote add origin https://github.com/<usuario>/<repo>.git
# git push -u origin main
```

## Licença
Defina a licença de sua preferência (MIT/Apache-2.0/etc.).