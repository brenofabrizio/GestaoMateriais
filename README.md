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
