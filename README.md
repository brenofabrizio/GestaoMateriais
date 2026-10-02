# Gestão de Materiais

Sistema corporativo para gestão de materiais, estoque, compras, ativos, solicitações e distribuição para TI, Suprimentos, Administrativo e RH.

## Objetivo

Criar uma plataforma modular, auditável e escalável para controlar o ciclo completo dos materiais:

```text
Catálogo → Solicitação → Aprovação → Compra/Separação → Recebimento → Entrega → Inventário
```

## Stack

- Frontend: Next.js, React, TypeScript e Tailwind CSS
- Backend: Django + Django REST Framework
- Banco: PostgreSQL gerenciado (Neon ou Supabase)
- Autenticação: Django REST Framework + JWT/HttpOnly cookies
- Jobs e filas: Celery + Redis gerenciado
- Arquivos: S3, Supabase Storage ou Cloudflare R2
- IA futura: serviço Python/FastAPI separado
- Testes: Pytest, Vitest, Testing Library e Playwright

## Estrutura

```text
frontend/      Aplicação Next.js
backend/       API Django + Django REST Framework
ai-service/    Serviço Python/FastAPI para IA futura
infra/         Configurações de deploy e serviços externos
docs/          Arquitetura, regras e decisões
```

## Primeiro marco

O primeiro marco funcional será a fundação de identidade e organização:

- Login e logout;
- Recuperação de senha;
- Organizações;
- Áreas: TI, Suprimentos, Administrativo e RH;
- Usuários;
- Perfis e permissões;
- Escopo de acesso por área;
- Auditoria das ações de acesso.

## Modo demo e dados iniciais

O frontend possui uma camada de demonstração funcional para permitir deploy imediato na Vercel mesmo antes de conectar o backend:

- `frontend/src/data/seed.json` é o banco inicial versionado, com organização, áreas, usuários, catálogo, almoxarifados, saldos, solicitações, movimentações e auditoria;
- `frontend/src/lib/store.ts` valida e carrega o seed e persiste alterações no `localStorage` usando a chave `gestao-materiais:data:v1`;
- a interface permite navegar pelo catálogo, estoque, solicitações, relatórios e criar novas solicitações;
- “Restaurar demo” remove alterações locais e volta ao conjunto inicial.

Esse modo é adequado para demonstração/homologação. Para produção multiusuário, a fonte de verdade deve ser a API Django com PostgreSQL; `localStorage` não substitui autenticação, autorização ou persistência transacional.

## Deploy do frontend na Vercel

Configure o projeto Vercel apontando para a pasta `frontend` (ou use `frontend/vercel.json`). Os comandos versionados são:

```bash
npm ci
npm run lint
npm run build
npm run start
```

O build usa Webpack para funcionar também em ambientes Windows onde o binding nativo do Turbopack pode ser bloqueado por política de segurança. A aplicação demo não exige variável de ambiente; quando a API for conectada, defina `NEXT_PUBLIC_API_URL`.

## Ambiente local

Requisitos mínimos:

- Node.js 22+
- Python 3.11+
- NPM
- pip ou uv
- Conta GitHub
- Banco PostgreSQL gerenciado

Docker é opcional no desenvolvimento inicial. O frontend será implantado na Vercel e o backend Django em Railway, Render ou Fly.io.

## Princípios do projeto

- Toda regra de negócio deve estar no backend;
- O frontend nunca decide permissão sozinho;
- Dados financeiros, de estoque e auditoria devem ser rastreáveis;
- Movimentações de estoque são imutáveis;
- Exclusões serão lógicas quando houver histórico;
- Toda mudança relevante gera auditoria;
- Testes devem acompanhar cada regra crítica;
- Não usar dados fictícios como substituto do banco transacional.

## Documentação

- `docs/PRD.md` — requisitos, escopo e roadmap;
- `docs/TRD.md` — arquitetura e requisitos técnicos;
- `docs/APP-FLOW.md` — fluxos do produto;
- `docs/UI-UX-DESIGN.md` — diretrizes de interface;
- `docs/IMPLEMENTATION-PLAN.md` — plano de execução;
- `docs/README.md` — índice da documentação.
