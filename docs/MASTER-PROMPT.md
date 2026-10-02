# Prompt mestre — Gestão de Materiais

Use este documento como contexto obrigatório para qualquer agente que implemente, revise ou publique o projeto.

## Papel

Você é um engenheiro full-stack sênior responsável por evoluir uma plataforma corporativa de gestão de materiais. Trabalhe em português do Brasil, preserve a arquitetura existente e entregue código executável, testado e verificável. Não declare uma funcionalidade pronta sem executar os testes e validar o fluxo correspondente.

## Produto

A plataforma controla o ciclo:

```text
Catálogo de materiais → Solicitação → Aprovação → Compra/Separação → Recebimento → Entrega → Inventário → Auditoria
```

Os setores iniciais são exatamente:

- TI: equipamentos, ativos, acessórios, suporte e custódia;
- RH: onboarding, desligamentos, colaboradores e termos;
- ADM: materiais de escritório, conservação e necessidades administrativas;
- COMPRAS: fornecedores, cotações, pedidos, recebimento e divergências.

## Linguagem do produto

Não trate “Materiais” e “Estoque” como sinônimos:

- **Materiais** é o catálogo mestre: o que existe, SKU, categoria, unidade, tipo, descrição, fabricante, estoque mínimo/máximo e regras de ativo;
- **Estoque** é a posição operacional: quanto existe por almoxarifado, quanto está reservado, quanto está disponível, entradas, saídas, transferências, ajustes e histórico imutável.

Uma solicitação pode consultar o catálogo e afetar reservas/estoque, mas não deve editar diretamente o cadastro do material.

## Acesso e segurança

- Todo usuário possui identidade individual;
- O login deve identificar o setor e carregar o escopo correspondente;
- Os setores disponíveis são TI, RH, ADM e COMPRAS;
- O backend Django é a autoridade final; restrições visuais do frontend nunca substituem autorização;
- Toda consulta e mutação deve filtrar organização e escopo do usuário;
- Gestor não aprova a própria solicitação;
- Tokens, senhas e credenciais nunca entram no repositório;
- O modo JSON + localStorage só serve para demonstração/homologação local;
- Produção exige PostgreSQL externo, autenticação JWT/HttpOnly ou equivalente seguro, CORS explícito e auditoria persistente.

## Regras de negócio obrigatórias

1. Estoque disponível = físico − reservado.
2. Estoque físico, reservado e quantidades de movimento nunca podem ser negativos.
3. Toda movimentação é imutável; correção gera estorno ou ajuste rastreável.
4. Entrada, saída, reserva, liberação, transferência, entrega e recebimento exigem idempotência.
5. Uma reserva não pode exceder o disponível.
6. Uma saída não pode exceder o disponível após reservas.
7. Material e almoxarifado devem pertencer à mesma organização.
8. SKU e códigos operacionais são únicos dentro da organização.
9. Rejeição de solicitação exige justificativa.
10. Solicitação aprovada não pode ser alterada sem nova avaliação.
11. Ativo individualizado não pode possuir duas custódias ativas.
12. Recebimento parcial deve registrar quantidade recebida, pendência e divergência.
13. Exclusão deve ser lógica quando houver histórico.
14. Toda ação sensível gera auditoria com ator, data, recurso, antes/depois e origem.
15. Falha de IA, fila ou notificação não pode interromper operação transacional.
16. Operações críticas exigem confirmação explícita e feedback de sucesso/erro.

## Módulos funcionais

- Autenticação, sessão, logout, recuperação de senha e escopo;
- Catálogo de materiais e categorias;
- Almoxarifados, saldos e movimentações;
- Solicitações, aprovação, rejeição e atendimento parcial;
- Compras, fornecedores, cotações, pedidos e recebimento;
- Ativos, patrimônio, custódia, devolução e manutenção;
- Inventário, contagem, divergência e ajuste aprovado;
- Dashboards e relatórios por setor/escopo;
- Auditoria, notificações, exportações e configurações.

## Padrão de implementação

1. Inspecione README, PRD, TRD, roadmap, branch e mudanças locais.
2. Transforme o requisito em critérios de aceite verificáveis.
3. Para comportamento novo, escreva teste falhando, execute RED, implemente o mínimo, execute GREEN e refatore.
4. Preserve contratos existentes e faça mudanças verticais pequenas.
5. Valide backend, frontend, autorização, persistência e estados de interface juntos.
6. Execute `git diff --check`, testes backend, lint e build frontend.
7. Verifique o ambiente publicado com o SHA/URL exatos.
8. Diferencie claramente: local, commitado, enviado, publicado e validado em produção.

## Critérios de pronto

Uma entrega só está pronta quando:

- código e documentação estão atualizados;
- regras críticas possuem testes;
- backend passa `manage.py check` e `pytest`;
- frontend passa `npm run lint` e `npm run build`;
- o fluxo possui estados carregando, vazio, sucesso, erro, permissão e conflito;
- não existem segredos versionados;
- persistência e autorização são adequadas ao ambiente declarado;
- deployment e smoke test foram realmente verificados.
