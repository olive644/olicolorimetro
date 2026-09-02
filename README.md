# olicolorimetro

Colorímetro que usa a câmera do celular para estimar concentração de uma amostra a partir de uma curva de calibração.

## Estrutura

- `index.html`: frontend estático (HTML/JS puro). Acessa a câmera, deixa selecionar a região da amostra e envia a imagem para a API.
- `backend/`: API em FastAPI + OpenCV que processa a imagem, calcula a cor média da amostra, guarda os pontos de calibração e estima a concentração.

## Rodando o backend localmente

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

A API sobe em `http://localhost:8000`. Endpoints principais:

- `POST /api/calibration-points`: recebe uma imagem, a região (ROI) e a concentração conhecida; salva o ponto de calibração.
- `GET /api/calibration-points`: lista os pontos salvos.
- `DELETE /api/calibration-points/{id}`: remove um ponto.
- `GET /api/fit`: retorna a curva linear (m, b) ajustada aos pontos salvos.
- `POST /api/readings`: recebe uma imagem e a ROI, calcula a cor e retorna a concentração estimada usando a curva salva.

## Frontend

Abra `index.html` no navegador (ou hospede via GitHub Pages) e informe o endereço da API rodando (local ou já publicada) no campo "Endereço da API".

## Publicando

- Frontend: GitHub Pages (estático, gratuito).
- Backend: qualquer serviço que rode Python 24 horas, como Render ou Railway (planos gratuitos existem, com limitações de uso).
