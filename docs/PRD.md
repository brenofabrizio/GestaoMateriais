# PRD — Gestão de Materiais

**Produto:** Gestão de Materiais Corporativo  
**Status:** Fundação implementada; evolução por sprints  
**Público:** TI, Suprimentos, Administrativo, RH, gestores, almoxarifado e auditoria

## 1. Visão do produto

O Gestão de Materiais é uma plataforma corporativa para controlar o ciclo completo dos materiais, ativos e solicitações:

```text
Catálogo → Solicitação → Aprovação → Reserva/Compra → Recebimento → Entrega → Inventário → Auditoria
```

O produto deve substituir planilhas e controles isolados por uma fonte única, rastreável e segura.

## 2. Objetivos

- Reduzir perdas, compras emergenciais e estoque parado;
- Dar visibilidade por área, filial, departamento e almoxarifado;
- Garantir que toda movimentação tenha responsável e histórico;
- Automatizar aprovações e notificações;
- Controlar materiais consumíveis e ativos individualizados;
- Preparar dados confiáveis para previsões e automações com IA;
- Atender requisitos de segregação de acesso e auditoria.

## 3. Não objetivos iniciais

- Substituir um ERP financeiro completo;
- Fazer contabilidade;
- Aprovar automaticamente ações críticas com IA;
- Criar microsserviços independentes antes de existir necessidade operacional;
- Permitir contas compartilhadas por área.

## 4. Personas

| Persona | Necessidade principal |
|---|---|
| Solicitante | Pedir materiais e acompanhar o atendimento |
| Gestor | Aprovar ou rejeitar solicitações da área |
| Estoquista | Receber, separar, transferir e dar baixa |
| Comprador | Cotar, negociar e acompanhar pedidos |
| RH | Controlar kits, uniformes e devoluções |
| TI | Controlar ativos, patrimônio e custódia |
| Auditor | Consultar evidências e trilhas sem alterar dados |
| Administrador | Configurar organização, usuários e permissões |

## 5. Áreas iniciais

- TI;
- Suprimentos;
- Administrativo;
- RH.

As áreas são registros configuráveis e não condicionais fixos no código.

## 6. Requisitos funcionais

### RF-01 — Identidade e acesso

- Login por e-mail;
- Refresh token;
- Logout com invalidação do refresh token;
- Usuário vinculado a uma organização e área;
- Papéis vinculados à organização;
- Controle de escopo por organização e área;
- Recuperação de senha;
- Auditoria de ações sensíveis.

### RF-02 — Catálogo

- Categorias por organização;
- Materiais com SKU único por organização;
- Tipos: consumível, ativo e serviço;
- Unidade de medida;
- Estoque mínimo e máximo;
- Número de série obrigatório para ativos quando aplicável;
- Ativação e desativação sem apagar histórico.

### RF-03 — Estoque

- Almoxarifados por organização;
- Saldo por material e almoxarifado;
- Entradas;
- Saídas;
- Reservas;
- Liberações;
- Transferências;
- Idempotência;
- Livro imutável de movimentações;
- Bloqueio de saldo negativo.

### RF-04 — Solicitações

- Criação em rascunho;
- Inclusão de itens;
- Envio para aprovação;
- Aprovação e rejeição;
- Justificativa obrigatória para rejeição;
- Atendimento parcial;
- Histórico de status;
- Isolamento por organização.

### RF-05 — Compras

- Fornecedores;
- Solicitação de compra;
- Cotação;
- Comparativo de propostas;
- Pedido de compra;
- Recebimento parcial;
- Nota fiscal;
- Divergência entre pedido e recebimento;
- Entrada no estoque após conferência.

### RF-06 — Ativos e custódia

- Número de patrimônio e série;
- Entrega para colaborador;
- Termo de responsabilidade;
- Assinatura;
- Devolução;
- Troca de equipamento;
- Manutenção;
- Pendências de desligamento.

### RF-07 — Inventário

- Inventário por local;
- Contagem parcial;
- QR Code;
- Divergências;
- Ajustes aprovados;
- Evidências e relatórios.

### RF-08 — IA

- Classificação de solicitações;
- Previsão de consumo;
- Sugestão de reposição;
- Leitura de notas fiscais;
- Busca semântica;
- Assistente interno com controle de escopo.

A IA recomenda. Ações críticas continuam exigindo aprovação humana.

## 7. Regras de negócio principais

1. Cada pessoa possui seu próprio usuário.
2. O backend é a autoridade final de autenticação e autorização.
3. Um usuário só atua dentro da organização autorizada.
4. Materiais e almoxarifados devem pertencer à mesma organização.
5. O estoque disponível é `físico - reservado`.
6. O estoque nunca pode ficar negativo.
7. Movimentações não são editadas nem apagadas.
8. Correções geram ajuste ou estorno rastreável.
9. Operações de estoque exigem chave de idempotência.
10. O solicitante não aprova a própria solicitação.
11. Rejeição exige justificativa.
12. Toda mudança de status gera histórico.
13. Ativo individualizado não pode ter duas custódias ativas.
14. Exclusão lógica preserva auditoria e histórico.
15. IA não conclui operações críticas sem aprovação humana.

## 8. Sprints realizadas

### Sprint 01 — Fundação técnica

**Concluída.**

- Monorepo;
- Django + DRF;
- Next.js;
- Ambiente Python;
- CI;
- Documentação inicial;
- Estrutura para IA;
- Deploy planejado por GitHub.

### Sprint 02 — Identidade e autorização

**Concluída na fundação inicial.**

- Usuário customizado por e-mail;
- Organização;
- Área;
- Papéis;
- JWT;
- Refresh;
- Logout com blacklist;
- `/api/auth/me/`;
- Contexto de papéis.

### Sprint 03 — Catálogo de materiais

**Concluída.**

- Categorias;
- Materiais;
- SKU por organização;
- Consumível, ativo e serviço;
- Unidade;
- Estoque mínimo e máximo;
- Regras de integridade.

### Sprint 04 — Estoque e almoxarifado

**Concluída na primeira versão.**

- Almoxarifados;
- Saldo por local;
- Entrada;
- Saída;
- Reserva;
- Liberação;
- Transferência;
- Livro de movimentações;
- API protegida;
- Idempotência;
- Proteção contra saldo negativo.

### Sprint 05 — Solicitações e aprovações

**Concluída na primeira versão.**

- Solicitação;
- Itens;
- Status;
- Aprovação;
- Rejeição;
- Justificativa;
- Histórico;
- API de solicitações.

## 9. Sprints restantes

### Sprint 06 — Compras, fornecedores e recebimento

- Fornecedores;
- Cotações;
- Pedidos;
- Recebimento parcial;
- Nota fiscal;
- Divergência;
- Entrada automática após conferência.

### Sprint 07 — Entrega, custódia e ativos

- Separação;
- Entrega;
- Termo;
- QR Code;
- Assinatura;
- Devolução;
- Manutenção;
- Desligamento.

### Sprint 08 — Inventário e auditoria

- Inventário rotativo;
- Contagem;
- Divergências;
- Ajustes aprovados;
- Evidências;
- Auditoria expandida.

### Sprint 09 — Dashboards e relatórios

- Dashboard por área;
- Consumo;
- Estoque mínimo;
- Compras abertas;
- Custódia;
- Exportações;
- Indicadores.

### Sprint 10 — IA e automações

- Serviço FastAPI;
- Jobs assíncronos;
- Classificação;
- Previsão;
- OCR de notas;
- Busca semântica;
- Assistente interno.

### Sprint 11 — Produção e governança

- Ambientes;
- CI/CD;
- Monitoramento;
- Backups;
- Restauração testada;
- LGPD;
- Retenção;
- Gestão de custos;
- Disaster recovery.

## 10. Métricas de sucesso

- Percentual de solicitações atendidas dentro do SLA;
- Redução de estoque abaixo do mínimo;
- Redução de compras emergenciais;
- Percentual de ativos com custódia válida;
- Divergência de inventário;
- Tempo médio de aprovação;
- Tempo médio de atendimento;
- Percentual de movimentações auditáveis;
- Taxa de sucesso de integrações.

## 11. Critérios de aceite do produto

O produto será considerado pronto para produção quando:

- Todos os fluxos críticos tiverem testes automatizados;
- Houver controle de acesso por organização e área;
- Estoque não puder ficar negativo;
- Aprovações tiverem histórico completo;
- Backups e restauração forem comprovados;
- CI estiver verde;
- Logs e alertas estiverem configurados;
- Ambiente de homologação tiver dados controlados;
- Não existirem dados fictícios substituindo o banco transacional.
