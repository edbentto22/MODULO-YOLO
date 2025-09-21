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

# Upload Service

## Variáveis de Ambiente
- BASE_URL: (opcional) URL base para compor links públicos. Se não definida, o serviço infere automaticamente via cabeçalhos X-Forwarded-* ou request.base_url.
  - Ex.: `export BASE_URL="https://preprocessor.matika.app"`
- CORS_ORIGINS: (recomendado em produção) lista separada por vírgula dos domínios permitidos para chamadas do navegador.
  - Ex.: `export CORS_ORIGINS="https://preprocessor.matika.app,https://www.seudominio.com"`

## CORS
- Em desenvolvimento local, o serviço libera por padrão `http://localhost:8000` e `http://127.0.0.1:8000`.
- Em produção, defina CORS_ORIGINS para restringir o acesso aos domínios da UI.

## Links Públicos
- Em produção atrás de proxy (Coolify/Traefik), deixar BASE_URL em branco é suportado: o backend detectará automaticamente o esquema/host usando `X-Forwarded-Proto`, `X-Forwarded-Host` e `X-Forwarded-Port`, caindo para `request.base_url` quando ausentes.

## Docker Compose
Exemplo:

```yaml
services:
  app:
    build: .
    environment:
      - CORS_ORIGINS=https://preprocessor.matika.app
      # BASE_URL opcional; se omitido, será inferido por request
      # - BASE_URL=https://preprocessor.matika.app
    ports:
      - "8002:8002"
```
- Em "Estrutura de Pastas", use a `imagens/` (ignorada no Git):
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