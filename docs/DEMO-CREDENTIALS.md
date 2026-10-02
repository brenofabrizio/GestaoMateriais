# Credenciais do ambiente de demonstração

> **Atenção:** estas credenciais são fictícias e existem somente para testar o frontend publicado. Não reutilize as senhas em homologação real ou produção.

## Acessos por setor

| Setor | E-mail | Senha | Perfil demo |
|---|---|---|---|
| TI | `ti@acme.demo` | `Demo@123` | Gestor de TI |
| RH | `rh@acme.demo` | `Demo@123` | Gestor de RH |
| ADM | `adm@acme.demo` | `Demo@123` | Gestor Administrativo |
| COMPRAS | `compras@acme.demo` | `Demo@123` | Comprador |

## Como testar

1. Acesse o frontend publicado;
2. Selecione um setor;
3. Confirme o e-mail preenchido;
4. Informe `Demo@123`;
5. Clique em **Entrar**;
6. Use **Sair** para testar o encerramento da sessão;
7. Troque de setor e repita o fluxo.

## Limitações do modo demo

- A sessão é armazenada no `localStorage` do navegador;
- O catálogo e as operações demo também usam `localStorage`;
- Não há autenticação multiusuário real nesse modo;
- Não use esses usuários para dados oficiais;
- A senha aparece no código do frontend por ser um ambiente demonstrativo.

## Migração para produção

Quando o backend estiver disponível, configure no projeto frontend:

```env
NEXT_PUBLIC_API_URL=https://api.seu-dominio.com/api
```

O login de produção deverá usar o endpoint Django `/auth/token/`, usuários persistidos, senha com hash, refresh token, logout e autorização por organização/setor. As credenciais desta página deverão ser removidas do fluxo publicado antes do go-live.
