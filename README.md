# API de Tarefas – Guia de Instalação e Uso (Docker)

Este README descreve como configurar, executar e testar a **API de Tarefas** utilizando **Docker** e **Postman**.

---

---
## Configurações inicias
### 1. Clonar o repositório

```bash
git clone https://github.com/DaviGomesO/desafio-catskillet.git
cd desafio-catskillet
```

---

### 2. Configurar variáveis de ambiente

1. Crie um arquivo `.env` na raiz do projeto.
2. Defina as seguintes variáveis (substitua pelos seus valores):

   ```.env
   # Banco de dados (Docker Compose)
   ENGINE=django.db.backends.postgresql
   NAME=railway
   USER=postgres
   PASSWORD=kjzaytVcxliSlntLkmgpzSkdivRYTgGF
   HOST=db
   PORT=5432

   # Redis (cache e broker)
   REDIS_URL=redis://redis:6379/1

   # Mailtrap (testes de e-mail)
   EMAIL_HOST=sandbox.smtp.mailtrap.io
   EMAIL_HOST_USER=57096c51e71226
   EMAIL_HOST_PASSWORD=a5da974cb625d2
   EMAIL_PORT=2525
   DEFAULT_FROM_EMAIL=no-reply@tasks.com

   # JWT (em minutos)
   ACCESS_TOKEN_LIFETIME=60
   REFRESH_TOKEN_LIFETIME=1440
   ```

---

### 3. Construir e subir containers

```bash
docker-compose up --build -d
```

Isso criará e iniciará os serviços:

* **web**: Django
* **db**: PostgreSQL
* **redis**: Redis (cache)

---

### 4. Migrar banco e criar superusuário

```bash
# Obter id do container
docker ps -a
docker-compose exec -it <id_container> /bin/bash

# Execute
python manage.py migrate
python manage.py createsuperuser
```

Acesse o Admin em: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

### 5. Documentação dos Endpoints (Postman)

Uma coleção Postman está disponível em [Desafio_Catskillet.postman_collection.json](docs/Desafio_Catskillet.postman_collection.json). Importe-a no seu Postman para testar rapidamente todos os endpoints.

#### Principais rotas da API

| Método | Endpoint                 | Descrição                                   | Autenticação | Parâmetros                                                                               |
| ------ | ------------------------ | ------------------------------------------- | ------------ | ---------------------------------------------------------------------------------------- |
| POST   | `/api/v1/register/`      | Criar novo usuário                          | Não          | `{ "username", "email", "password" }`                                                    |
| POST   | `/api/v1/token/`         | Obter tokens JWT (access e refresh)         | Não          | `{ "username", "password" }`                                                             |
| POST   | `/api/v1/token/refresh/` | Renovar access token usando refresh token   | Não          | `{ "refresh": "<refresh_token>" }`                                                       |
| GET    | `/api/v1/tasks/`         | Listar tarefas do usuário                   | Sim          | Query params opcionais: `title`, `description`, `execution_date`, `status`, `categories` |
| POST   | `/api/v1/tasks/`         | Criar nova tarefa                           | Sim          | `{ "title", "description", "execution_date", "status", "categories": [id,...]}`          |
| GET    | `/api/v1/tasks/{id}/`    | Recuperar detalhes de uma tarefa específica | Sim          | `id` na URL                                                                              |
| PUT    | `/api/v1/tasks/{id}/`    | Atualizar completamente uma tarefa          | Sim          | Mesmos campos do POST                                                                    |
| DELETE | `/api/v1/tasks/{id}/`    | Excluir uma tarefa                          | Sim          | `id` na URL                                                                              |
| GET    | `/api/v1/tasks/agenda/`  | Retorna agenda (tarefas ordenadas)          | Sim          | Mesmos filtros da listagem; resposta cacheada por usuário                                |

> **Importante**: inclua o header HTTP `Authorization: Bearer <access_token>` em todos os endpoints protegidos.
