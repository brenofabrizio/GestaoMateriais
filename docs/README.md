# Documentação — Gestão de Materiais

| Documento | Conteúdo |
|---|---|
| [PRD](PRD.md) | Visão do produto, requisitos, regras e sprints |
| [TRD](TRD.md) | Arquitetura, dados, segurança, API e operação |
| [App Flow](APP-FLOW.md) | Fluxos de login, estoque, solicitações, compras e ativos |
| [UI/UX Design](UI-UX-DESIGN.md) | Sistema visual, telas, componentes e acessibilidade |
| [Plano de implementação](IMPLEMENTATION-PLAN.md) | Fases, tarefas, critérios de aceite e gates |
| [Arquitetura inicial](arquitetura-inicial.md) | Decisões estruturais iniciais |
| [Sprints](sprints.md) | Roadmap detalhado por sprint |
| [Ambiente local](ambiente-local.md) | Pré-requisitos e deploy |
| [Regras de domínio](DOMAIN-RULES.md) | Diferença entre catálogo e estoque, escopos e regras obrigatórias |
| [Prompt mestre](MASTER-PROMPT.md) | Contexto completo para implementação, revisão e publicação |

## Estado atual

Implementado:

- Fundação Django + DRF;
- Next.js;
- Usuários, organizações, áreas e papéis;
- JWT, refresh e logout com blacklist;
- Catálogo de materiais;
- Estoque, reservas e transferências;
- Solicitações e aprovação;
- CI e testes automatizados.

- Próximo módulo:

- Compras, fornecedores e recebimento.

## PDFs para visualização

- [TRD](pdf/TRD-Gestao-de-Materiais.pdf)
- [App Flow](pdf/App-Flow-Gestao-de-Materiais.pdf)
- [UI/UX Design](pdf/UI-UX-Design-Gestao-de-Materiais.pdf)
- [Plano de implementação](pdf/Plano-Implementacao-Gestao-de-Materiais.pdf)
- [Arquitetura inicial](pdf/Arquitetura-Inicial-Gestao-de-Materiais.pdf)

Os PDFs são gerados por `docs/tools/generate_pdfs.py` a partir dos Markdown versionados.
