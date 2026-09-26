# Ambiente local e deploy

## Requisitos

- Node.js 22+
- Python 3.11+
- NPM
- pip ou uv
- Git
- Conta GitHub
- PostgreSQL gerenciado: Neon ou Supabase

Docker é opcional no desenvolvimento inicial.

## Desenvolvimento

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Backend:

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
python manage.py runserver
```

## Deploy inicial

```text
frontend Next.js → Vercel
backend Django  → Railway, Render ou Fly.io
PostgreSQL      → Neon ou Supabase
Redis           → Upstash ou Redis gerenciado
```

O GitHub será a origem do código e cada serviço poderá ser conectado ao repositório para deploy automático.
