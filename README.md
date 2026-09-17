# TwitterClone

Projeto final do curso Full Stack Python (EBAC) — um clone funcional do Twitter, construído com Django. O projeto é **monolítico** (views + templates Django) e também expõe uma **API REST completa** (Django REST Framework) sobre os mesmos dados.

## Funcionalidades

- Cadastro e login de usuários
- Edição de perfil (foto, nome, bio, redes sociais, senha) — nenhum campo é obrigatório na edição
- Seguir / deixar de seguir outros usuários, com listas de seguidores e seguidos
- Feed com posts apenas de quem você segue
- Criar, editar e deletar tweets
- Curtir tweets
- Comentar tweets

## Tecnologias

- Backend: Django 3.2 + Django REST Framework
- Banco de dados: PostgreSQL (produção) / SQLite (desenvolvimento local)
- Frontend: templates Django (Bootstrap)
- Deploy: Docker + Render

## Rodando localmente

Pré-requisitos: Python 3.10+ e [Poetry](https://python-poetry.org/).

```bash
git clone https://github.com/TheHenrique/twitter-clone.git
cd twitter-clone
poetry install --no-root
poetry run python manage.py migrate
poetry run python manage.py createsuperuser   # opcional, para acessar o /admin/
poetry run python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`.

## Rodando os testes

```bash
poetry run python manage.py test
```

## Rodando com Docker

```bash
docker build -t twitter-clone .
docker run -p 8000:8000 twitter-clone
```

## Variáveis de ambiente

Por padrão o projeto roda com SQLite sem configuração nenhuma. Para usar Postgres (produção), defina:

| Variável | Descrição | Padrão |
|---|---|---|
| `SECRET_KEY` | Chave secreta do Django | (valor de desenvolvimento embutido) |
| `DEBUG` | `"True"` ou `"False"` | `True` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos, separados por espaço | `127.0.0.1 localhost cedric.pythonanywhere.com` |
| `SQL_ENGINE` | `django.db.backends.postgresql` para Postgres | `django.db.backends.sqlite3` |
| `SQL_DATABASE`, `SQL_USER`, `SQL_PASSWORD`, `SQL_HOST`, `SQL_PORT` | Credenciais do banco Postgres | — |

## API REST

Base: `/api/v1/`

| Endpoint | Método | Descrição |
|---|---|---|
| `/api/v1/auth/register/` | POST | Cria um usuário e retorna o token |
| `/api/v1/auth/token/` | POST | Login — recebe `username`/`password`, retorna o token |
| `/api/v1/tweets/` | GET, POST | Lista todos os tweets / cria um tweet (autenticado) |
| `/api/v1/tweets/{id}/` | GET, PATCH, DELETE | Detalhe, editar ou deletar (só o dono) |
| `/api/v1/tweets/feed/` | GET | Feed com tweets só de quem você segue (autenticado) |
| `/api/v1/tweets/{id}/like/` | POST | Curte/descurte o tweet (autenticado) |
| `/api/v1/comments/?tweet={id}` | GET, POST | Lista comentários de um tweet / adiciona um comentário |
| `/api/v1/profiles/` | GET | Lista perfis |
| `/api/v1/profiles/{id}/follow/` | POST | Segue o perfil (autenticado) |
| `/api/v1/profiles/{id}/unfollow/` | POST | Deixa de seguir o perfil (autenticado) |

Autenticação via token: envie o header `Authorization: Token <seu-token>` obtido em `/api/v1/auth/register/` ou `/api/v1/auth/token/`.

## Deploy

Aplicação disponível em: **_(adicionar link do deploy aqui depois de publicar no Render)_**