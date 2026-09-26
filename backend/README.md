# Backend Django

O backend principal será um monólito modular em Django:

- Django;
- Django REST Framework;
- PostgreSQL;
- SimpleJWT ou autenticação por cookies HttpOnly;
- Celery + Redis para jobs;
- Pytest para testes.

Módulos iniciais planejados:

```text
apps/accounts
apps/organizations
apps/materials
apps/inventory
apps/requests
apps/purchasing
apps/audit
```

A IA não será implementada dentro das requisições transacionais. Quando necessário, o Django publicará um job para o serviço `ai-service`.
