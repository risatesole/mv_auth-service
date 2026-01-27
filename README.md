# Authentication Microservice

Lightweight authentication service built with FastAPI and PostgreSQL, held together with tape, hopes, and dreams.

## Features

- User authentication with secure password hashing  
- Token-based authentication (JWT-ready, no magic involved)  
- Clean separation of concerns (routes, services, repositories)  
- Built on FastAPI for high performance and async support  
- PostgreSQL-backed persistence (boring, reliable, battle-tested)  
- Docker-first setup with a minimal `docker-compose` for local dev  
- Environment-based configuration (no hardcoded secrets, promise)  
- Designed to be testable without summoning dark rituals  
- Easy to extend with roles, permissions, refresh tokens, or OAuth  
- Opinionated just enough to stay sane, flexible enough to evolve  

> Not enterprise-grade™ yet — but it *wants* to be.


example docker-compose file:

```yml
version: "3.9"

services:
  authserv:
    build: .
    container_name: auth-service
    ports:
      - "8000:8000"
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: mydb
      DB_USER: myuser
      DB_PASSWORD: mypassword
    depends_on:
      - db

  db:
    image: postgres:16
    container_name: pg-container
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - pg-data:/var/lib/postgresql/data

volumes:
  pg-data:
```
