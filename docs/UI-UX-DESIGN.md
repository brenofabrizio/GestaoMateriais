# UI/UX Design — Gestão de Materiais

## 1. Direção visual

A interface deve transmitir controle operacional, confiança e clareza. O produto não será um painel genérico de cards: cada tela deve priorizar decisão, status e próxima ação.

Direção:

- Editorial operacional;
- Alta legibilidade;
- Densidade controlada;
- Contraste claro entre estado e ação;
- Componentes consistentes;
- Microinterações discretas;
- Sem excesso de gradientes;
- Sem emojis como ícones de ação.

## 2. Tokens iniciais

```css
--color-forest-900: #123b35;
--color-forest-700: #20554b;
--color-lime-400: #c8f36c;
--color-surface: #f4f7f5;
--color-card: #ffffff;
--color-text: #17221f;
--color-muted: #718078;
--color-border: #dce7df;
--color-success: #2f7d52;
--color-warning: #b7791f;
--color-danger: #b64242;
```

A implementação deve evoluir para tokens semânticos, evitando cores espalhadas em componentes.

## 3. Tipografia

- Títulos: Manrope, peso 700/800;
- Corpo: DM Sans, peso 400/500;
- Base: 16px;
- Texto auxiliar: mínimo 12px;
- Line-height do corpo: 1.5 ou maior;
- Títulos curtos e orientados à ação.

## 4. Layout principal

```text
┌───────────────────────────────────────────────┐
│ Sidebar fixa/retrátil │ Topbar / contexto     │
│                      ├────────────────────────│
│ Navegação por módulo │ Conteúdo da página     │
│ Área e perfil         │                        │
└───────────────────────────────────────────────┘
```

A sidebar deve conter:

- Marca;
- Organização atual;
- Navegação por módulo;
- Indicador de área;
- Perfil e logout.

A topbar deve conter:

- Breadcrumb;
- Título;
- Filtros de contexto;
- Notificações;
- Usuário atual.

## 5. Telas prioritárias

### Login

- E-mail;
- Senha;
- Recuperação;
- Estado de erro próximo ao campo;
- Mensagem de bloqueio sem revelar se o e-mail existe;
- Foco automático no primeiro campo.

### Dashboard

- Indicadores operacionais;
- Solicitações aguardando ação;
- Estoque abaixo do mínimo;
- Compras atrasadas;
- Ativos pendentes;
- Atalhos para próxima ação.

### Lista de materiais

- Busca;
- Filtros por categoria, tipo e status;
- SKU;
- Saldo disponível;
- Estoque mínimo;
- Localização;
- Ação de visualizar;
- Ação de editar conforme permissão.

### Estoque

- Saldo físico;
- Reservado;
- Disponível;
- Histórico de movimentações;
- Entrada, saída, transferência e reserva;
- Confirmação para operações críticas;
- Chave de idempotência gerada no cliente e validada no backend.

### Solicitações

- Linha do tempo de status;
- Itens e quantidades;
- Justificativa;
- Aprovadores;
- Comentários;
- Estado atual destacado;
- Próxima ação disponível conforme papel.

## 6. Componentes

- Button;
- IconButton com `aria-label`;
- Input;
- Select;
- Combobox de materiais;
- DataTable;
- StatusBadge;
- Timeline;
- Modal de confirmação;
- Drawer de detalhes;
- Toast;
- EmptyState;
- ErrorState;
- Skeleton;
- Pagination;
- PermissionGate visual.

`PermissionGate` controla apresentação, mas nunca substitui a autorização no Django.

## 7. Estados de status

Não usar apenas cor para comunicar estado. Sempre combinar:

```text
cor + texto + ícone/forma + contexto
```

Exemplos:

- Aprovada: verde + texto “Aprovada”;
- Pendente: âmbar + texto “Aguardando aprovação”;
- Rejeitada: vermelho + motivo visível;
- Cancelada: neutro + texto explícito.

## 8. Formulários

- Labels sempre visíveis;
- Ajuda contextual;
- Validação próxima ao campo;
- Resumo de erros no topo para acessibilidade;
- Não limpar dados em erro de envio;
- Desabilitar botão durante submissão;
- Informar sucesso com confirmação clara;
- Campos obrigatórios marcados semanticamente.

## 9. Acessibilidade

- Navegação completa por teclado;
- Foco visível;
- Contraste mínimo WCAG AA;
- Alvos de toque de pelo menos 44px;
- `aria-label` em ícones;
- Tabelas com cabeçalhos semânticos;
- Modais com foco controlado;
- Respeito a `prefers-reduced-motion`;
- Mensagens de erro anunciáveis;
- Não depender apenas de cor.

## 10. Responsividade

Breakpoints:

```text
mobile: até 640px
 tablet: 641–1024px
 desktop: acima de 1024px
```

Em mobile:

- Sidebar vira navegação recolhida;
- Tabelas oferecem visual de lista/cartão;
- Ações principais ficam acessíveis no rodapé ou cabeçalho;
- Não criar rolagem horizontal invisível;
- Formulários ficam em uma coluna.

## 11. Feedback e movimento

- Transições curtas entre 150–250ms;
- Loading visível em toda ação assíncrona;
- Animação deve explicar mudança de estado;
- Não animar elementos críticos de forma chamativa;
- Respeitar redução de movimento;
- Erro deve permanecer visível até correção ou dismiss explícito.

## 12. Critérios de qualidade visual

Antes de considerar uma tela pronta:

- Não há placeholder de template;
- Não há dados fictícios apresentados como reais;
- Todos os estados foram desenhados;
- Ações têm feedback;
- Ícones têm significado e acessibilidade;
- Desktop e mobile foram verificados;
- A hierarquia visual deixa a próxima ação evidente.
