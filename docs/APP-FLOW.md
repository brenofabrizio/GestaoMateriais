# App Flow — Gestão de Materiais

## 1. Entrada no sistema

```mermaid
flowchart TD
    A[Usuário acessa o sistema] --> B{Sessão válida?}
    B -- Não --> C[Tela de login]
    C --> D{Credenciais válidas?}
    D -- Não --> E[Erro de autenticação]
    E --> C
    D -- Sim --> F[Carregar contexto: organização, área e papéis]
    B -- Sim --> F
    F --> G[Dashboard conforme escopo]
```

## 2. Solicitação interna

```mermaid
flowchart TD
    A[Dashboard] --> B[Nova solicitação]
    B --> C[Selecionar área de atendimento]
    C --> D[Adicionar materiais e quantidades]
    D --> E[Salvar rascunho]
    E --> F{Itens válidos?}
    F -- Não --> D
    F -- Sim --> G[Enviar para aprovação]
    G --> H[Aguardando aprovação]
    H --> I{Decisão do gestor}
    I -- Rejeitar --> J[Informar justificativa]
    J --> K[Rejeitada + notificar solicitante]
    I -- Aprovar --> L[Aprovada]
    L --> M{Tem estoque?}
    M -- Sim --> N[Reservar e separar]
    M -- Não --> O[Criar/encaminhar compra]
    N --> P[Entregar]
    O --> Q[Receber material]
    Q --> N
    P --> R[Finalizar solicitação]
```

## 3. Estoque

```mermaid
flowchart TD
    A[Operação de estoque] --> B{Tipo}
    B -- Entrada --> C[Validar material e almoxarifado]
    C --> D[Lock do saldo]
    D --> E[Incrementar físico]
    E --> F[Registrar movimento]
    B -- Saída --> G[Calcular disponível]
    G --> H{Saldo suficiente?}
    H -- Não --> I[Rejeitar operação]
    H -- Sim --> D
    B -- Reserva --> J[Calcular disponível]
    J --> K{Saldo suficiente?}
    K -- Não --> I
    K -- Sim --> L[Incrementar reservado]
    L --> F
    B -- Transferência --> M[Lock origem e destino]
    M --> N{Origem suficiente?}
    N -- Não --> I
    N -- Sim --> O[Baixar origem e creditar destino]
    O --> F
```

## 4. Compra

```mermaid
flowchart TD
    A[Solicitação aprovada sem estoque] --> B[Solicitação de compra]
    B --> C[Selecionar fornecedores]
    C --> D[Registrar cotações]
    D --> E[Comparar preço, prazo e condição]
    E --> F[Aprovação da compra]
    F --> G[Pedido de compra]
    G --> H[Aguardando fornecedor]
    H --> I[Receber materiais]
    I --> J[Conferir pedido e nota fiscal]
    J --> K{Divergência?}
    K -- Sim --> L[Registrar divergência]
    K -- Não --> M[Entrada no estoque]
    L --> N[Resolver com fornecedor]
    N --> M
```

## 5. TI — custódia de ativo

```mermaid
flowchart TD
    A[Ativo disponível] --> B[Solicitação aprovada]
    B --> C[Separar ativo individual]
    C --> D[Gerar termo]
    D --> E[Assinar entrega]
    E --> F[Custódia ativa]
    F --> G{Troca ou desligamento?}
    G -- Não --> F
    G -- Sim --> H[Solicitar devolução]
    H --> I[Conferir estado]
    I --> J{Dano ou perda?}
    J -- Sim --> K[Registrar ocorrência]
    J -- Não --> L[Retornar ao estoque]
    K --> L
```

## 6. Perfis e navegação

```text
Administrador
 ├── Dashboard global
 ├── Usuários e papéis
 ├── Todas as áreas
 ├── Auditoria
 └── Configurações

Gestor de área
 ├── Dashboard da área
 ├── Solicitações para aprovação
 ├── Materiais da área
 └── Relatórios do escopo

Estoquista
 ├── Estoque
 ├── Entrada
 ├── Saída
 ├── Transferência
 ├── Reservas
 └── Separação

Solicitante
 ├── Nova solicitação
 ├── Minhas solicitações
 └── Minhas entregas

Comprador
 ├── Compras
 ├── Cotações
 ├── Fornecedores
 └── Recebimento
```

## 7. Estados obrigatórios de interface

Todo fluxo deve possuir:

- Carregando;
- Vazio;
- Sucesso;
- Erro recuperável;
- Erro de permissão;
- Conflito de estado;
- Operação duplicada;
- Confirmação antes de ação irreversível.
