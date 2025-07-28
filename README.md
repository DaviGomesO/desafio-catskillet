# API de Tarefas – Guia de Instalação e Uso (Docker)

Este README descreve como configurar, executar e testar a **API de Tarefas** utilizando **Docker** e **Postman**.

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
   PASSWORD=<DB_PASS>
   HOST=db
   PORT=5432

   # Redis (cache e broker)
   REDIS_URL=redis://redis:6379/1

   # Mailtrap (testes de e-mail)
   EMAIL_HOST=sandbox.smtp.mailtrap.io
   EMAIL_HOST_USER=<host_user_mailtrap>
   EMAIL_HOST_PASSWORD=<host_pass_mailtrap>
   EMAIL_PORT=2525
   DEFAULT_FROM_EMAIL=no-reply@tasks.com

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



### 5.1 Documentação Manual por Endpoint

A seguir, cada rota da API com método, URL, cabeçalhos, parâmetros de entrada e exemplo de resposta.

---

#### 5.1.1 Registrar Usuário

* **Método:** `POST`
* **URL:** `/api/v1/register/`
* **Autenticação:** Não
* **Body (JSON):**

  ```json
  {
    "username": "novo_usuario",
    "email": "usuario@example.com",
    "password": "senhaSegura123"
  }
  ```
* **Resposta (201 Created):**

  ```json
  {
    "id": 1,
    "username": "novo_usuario",
    "email": "usuario@example.com"
  }
  ```

---

#### 5.1.2 Obter Tokens JWT

* **Método:** `POST`
* **URL:** `/api/v1/token/`
* **Autenticação:** Não
* **Body (JSON):**

  ```json
  {
    "username": "novo_usuario",
    "password": "senhaSegura123"
  }
  ```
* **Resposta (200 OK):**

  ```json
  {
    "refresh": "<refresh_token>",
    "access": "<access_token>"
  }
  ```

---

#### 5.1.3 Renovar Access Token

* **Método:** `POST`
* **URL:** `/api/v1/token/refresh/`
* **Autenticação:** Não
* **Body (JSON):**

  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```
* **Resposta (200 OK):**

  ```json
  {
    "access": "<new_access_token>"
  }
  ```

---

#### 5.1.4 Listar Tarefas

* **Método:** `GET`
* **URL:** `/api/v1/tasks/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Query Params Opcionais:**

  * `title` (filtros por substring do título)
  * `description` (substring da descrição)
  * `execution_date` (YYYY-MM-DD)
  * `status` (P, A, C)
  * `categories` (nome de categoria, substring)
* **Resposta (200 OK):**

  ```json
  [
    {
      "id": 5,
      "title": "Comprar suprimentos",
      "description": "Estojo de canetas e papel",
      "execution_date": "2025-08-01",
      "status": "P",
      "categories": [
        2
      ]
    }
  ]
  ```

---

#### 5.1.5 Criar Tarefa

* **Método:** `POST`
* **URL:** `/api/v1/tasks/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Body (JSON):**

  ```json
  {
    "title": "Nova tarefa",
    "description": "Detalhes...",
    "execution_date": "2025-08-05",
    "status": "P",
    "categories": [1,3]
  }
  ```
* **Resposta (201 Created):**

  ```json
  {
    "id": 8,
    "title": "Nova tarefa",
    "description": "Detalhes...",
    "execution_date": "2025-08-05",
    "status": "P",
    "categories": [1,3]
  }
  ```

---

#### 5.1.6 Recuperar/Atualizar/Deletar Tarefa

* **Métodos & URLs:**

  * `GET /api/v1/tasks/{id}/`
  * `PUT /api/v1/tasks/{id}/`
  * `DELETE /api/v1/tasks/{id}/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Parâmetro de URL:** `id` (número da tarefa)
* **Body para atualização (PUT):** mesmo formato de criação
* **Respostas:**

  * `GET`: 200 OK com objeto JSON da tarefa
  * `PUT`: 200 OK com dados atualizados
  * `DELETE`: 204 No Content

---

#### 5.1.7 Agenda (Tarefas Ordenadas)

* **Método:** `GET`
* **URL:** `/api/v1/tasks/agenda/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Query Params:** iguais à listagem de tarefas
* **Cache:** manual por usuário, expira em 5 minutos
* **Resposta (200 OK):**

  ```json
  [
    {
      "id": 3,
      "title": "Reunião equipe",
      "execution_date": "2025-07-28",
      "status": "A",
      "categories": [ ... ]
    },
    {
      "id": 7,
      "title": "Enviar relatório",
      "execution_date": "2025-07-30",
      "status": "P",
      "categories": [ ... ]
    }
  ]
  ```
