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

Próximo módulo:

- Compras, fornecedores e recebimento.
