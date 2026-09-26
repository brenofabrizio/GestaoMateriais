# Roadmap de sprints — Gestão de Materiais

## Sprint 01 — Fundação técnica e arquitetura

Objetivo: criar uma base executável, testável e preparada para produção.

Entregas:

- Monorepo organizado;
- Backend Django + DRF;
- Frontend Next.js;
- Configuração por ambiente;
- PostgreSQL preparado;
- CI com lint, testes e build;
- Documentação de arquitetura;
- Padrão de commits e branches;
- Health check da API.

Critério de aceite: backend e frontend executam localmente e o pipeline valida o projeto.

## Sprint 02 — Identidade, organizações e autorização

Entregas:

- Usuário customizado por e-mail;
- Organizações;
- Filiais;
- Áreas e departamentos;
- Perfis e permissões;
- Escopo de acesso por organização e área;
- Login, refresh e logout;
- Recuperação de senha;
- Auditoria de autenticação;
- Testes de autorização.

Critério de aceite: um usuário de RH não acessa dados de TI sem permissão explícita.

## Sprint 03 — Catálogo de materiais

Entregas:

- Categorias;
- Materiais consumíveis;
- Ativos individualizados;
- Unidades de medida;
- Fabricantes e modelos;
- Código interno, SKU, patrimônio e número de série;
- Estoque mínimo e máximo;
- Anexos e imagens;
- Importação validada por planilha.

## Sprint 04 — Almoxarifado e estoque

Entregas:

- Almoxarifados e locais;
- Entradas;
- Saídas;
- Transferências;
- Ajustes e estornos;
- Reservas;
- Bloqueios;
- Livro imutável de movimentações;
- Saldo por local;
- Regras para impedir estoque negativo.

## Sprint 05 — Solicitações e aprovações

Entregas:

- Solicitação interna;
- Itens e quantidades;
- Fluxo por status;
- Aprovação por área, valor e tipo de material;
- Atendimento parcial;
- Rejeição com justificativa;
- Cancelamento;
- Notificações;
- Histórico completo.

## Sprint 06 — Compras e fornecedores

Entregas:

- Fornecedores;
- Solicitação de compra;
- Cotações;
- Comparativo de propostas;
- Pedido de compra;
- Aprovação financeira;
- Recebimento parcial;
- Nota fiscal;
- Divergências.

## Sprint 07 — Entrega, custódia e ativos

Entregas:

- Entrega para colaborador;
- Termo de responsabilidade;
- Assinatura;
- QR Code;
- Devolução;
- Troca de equipamento;
- Manutenção;
- Pendências de desligamento;
- Histórico de custódia.

## Sprint 08 — Inventário e auditoria

Entregas:

- Inventário por local;
- Leitura por QR Code;
- Contagem parcial;
- Divergências;
- Ajustes com aprovação;
- Trilha de auditoria;
- Exportação de evidências;
- Logs protegidos.

## Sprint 09 — Dashboards e relatórios

Entregas:

- Dashboard por área;
- Estoque mínimo;
- Consumo por período;
- Compras em aberto;
- Itens por colaborador;
- Relatórios exportáveis;
- Indicadores de SLA.

## Sprint 10 — IA e automações

Entregas:

- Serviço de IA separado;
- Classificação de solicitações;
- Previsão de consumo;
- Sugestão de reposição;
- Leitura de notas fiscais;
- Busca semântica;
- Assistente interno com controle de acesso;
- Registro das decisões da IA.

Regra: a IA poderá recomendar, mas ações críticas exigirão aprovação humana.

## Sprint 11 — Produção e governança

Entregas:

- CI/CD;
- Ambientes dev, homologação e produção;
- Backups;
- Monitoramento;
- Alertas;
- Controle de custos;
- Política de retenção;
- LGPD;
- Disaster recovery;
- Teste de restauração.
