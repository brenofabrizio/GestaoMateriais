# Infraestrutura

Arquitetura de deploy inicial:

```text
frontend Next.js → Vercel
backend Django  → Railway, Render ou Fly.io
PostgreSQL      → Neon ou Supabase
Redis           → Upstash ou Redis gerenciado
Arquivos        → S3, R2 ou Supabase Storage
```

Docker é opcional no ambiente local e poderá ser adicionado depois para padronizar desenvolvimento e CI.
