# Regras de domínio e nomenclatura

## Materiais x Estoque

### Materiais — catálogo mestre

Representa a definição do item: SKU, nome, categoria, descrição, tipo (`consumable`, `asset` ou `service`), unidade, fabricante, modelo, estoque mínimo/máximo e se exige número de série.

### Estoque — posição operacional

Representa a disponibilidade do item em cada almoxarifado. Inclui quantidade física, reservada, disponível, movimentações, transferências, ajustes, entradas e saídas.

```text
Material = o que o item é
Estoque  = onde está e quanto existe agora
```

## Escopo por setor

| Setor | Responsabilidades iniciais |
|---|---|
| TI | Ativos, equipamentos, patrimônio, custódia e manutenção |
| RH | Onboarding, desligamento, colaboradores e termos |
| ADM | Materiais gerais, consumo, conservação e serviços |
| COMPRAS | Fornecedores, cotações, pedidos e recebimento |

O setor do usuário define a navegação inicial e o escopo de dados. A API deve repetir essa validação em todas as consultas e mutações.

## Estados obrigatórios

Toda operação deve tratar carregando, vazio, sucesso, erro recuperável, sem permissão, conflito de estado e duplicidade/idempotência.

## Próximas entregas prioritárias

1. Conectar a tela de login ao endpoint JWT do Django e remover credenciais demo do fluxo de produção.
2. Implementar fornecedores, cotações, pedidos e recebimento parcial.
3. Implementar ativos, custódia, termos e devolução.
4. Implementar inventário e ajustes aprovados.
5. Implementar permissões reais por setor no backend e auditoria persistente.
6. Migrar o modo demo para PostgreSQL, storage durável e deploy backend.
