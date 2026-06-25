# Smart Customer Support Inbox API

> Production-grade customer support backend with real-time messaging, distributed locking, and AI-assisted reply suggestions.

Built with Django, Django REST Framework, Django Channels, Celery, Redis, and PostgreSQL.

---

## Features

- **JWT Authentication** — Secure token-based auth with refresh token support
- **Conversation Management** — Full CRUD over support conversations and message history
- **Real-time Messaging** — WebSocket-powered instant message delivery via Django Channels
- **Distributed Locking** — Redis-backed conversation locks with automatic TTL expiration
- **Async Sentiment Analysis** — Background Celery tasks keep response times low
- **AI Reply Suggestions** — Rule-based suggestions generated per conversation
- **OpenAPI Docs** — Auto-generated via `drf-spectacular`
- **Comprehensive Tests** — Full pytest suite with coverage reporting

---

## Tech Stack

| Layer            | Technology            |
| ---------------- | --------------------- |
| API              | Django REST Framework |
| Database         | PostgreSQL            |
| Authentication   | JWT (SimpleJWT)       |
| Background Jobs  | Celery                |
| Broker / Cache   | Redis                 |
| Real-time        | Django Channels       |
| Documentation    | drf-spectacular       |
| Containerization | Docker                |
| Testing          | pytest                |

---

## Architecture

```
Client
  │
  ├── REST API ──► Django + DRF
  │                    │
  │                    ├── PostgreSQL       (persistence)
  │                    ├── Redis Locks      (distributed locking)
  │                    └── Celery Tasks     (async sentiment analysis)
  │
  └── WebSocket ──► Django Channels
                         │
                         └── Redis          (pub/sub channel layer)
```

---

## Design Decisions

### Redis for Distributed Locking

Redis provides sub-millisecond locking with native TTL support. Locks expire automatically after 5 minutes — no cleanup jobs required, no stale lock accumulation.

### Celery for Sentiment Analysis

Sentiment processing happens asynchronously. HTTP response times stay low; users are never blocked waiting on ML inference.

### Django Channels for WebSockets

Channels enables persistent bidirectional communication over a Redis channel layer, allowing the server to push new messages to connected clients instantly — no polling required.

---

## Getting Started

### Prerequisites

- Docker & Docker Compose

### Setup

```bash
git clone <repository>
cd <repository>
cp .env.example .env
docker compose up --build
```

### Database Setup

```bash
# Run migrations
docker compose exec web python manage.py migrate

# Seed initial data
docker compose exec web python manage.py seed_data
```

The seed command creates a default user:

| Field    | Value          |
| -------- | -------------- |
| Email    | admin@test.com |
| Password | admin123       |

---

## Authentication

Obtain a JWT token pair:

```bash
POST /api/auth/token/

{
  "email": "admin@test.com",
  "password": "admin123"
}
```

Include the access token in subsequent requests:

```
Authorization: Bearer <access_token>
```

---

## API Reference

### Auth

| Method | Endpoint                   | Description          |
| ------ | -------------------------- | -------------------- |
| POST   | `/api/auth/token/`         | Obtain token pair    |
| POST   | `/api/auth/token/refresh/` | Refresh access token |

### Conversations

| Method | Endpoint                            | Description                  |
| ------ | ----------------------------------- | ---------------------------- |
| GET    | `/api/conversations/`               | List all conversations       |
| GET    | `/api/conversations/{id}/messages/` | Get messages in conversation |

### Messaging

| Method | Endpoint                                 | Description    |
| ------ | ---------------------------------------- | -------------- |
| POST   | `/api/conversations/{id}/messages/send/` | Send a message |

### Locks

| Method | Endpoint                        | Description       |
| ------ | ------------------------------- | ----------------- |
| POST   | `/api/conversations/{id}/lock/` | Acquire lock      |
| GET    | `/api/conversations/{id}/lock/` | Check lock status |
| DELETE | `/api/conversations/{id}/lock/` | Release lock      |

### AI Suggestions

| Method | Endpoint                                 | Description                       |
| ------ | ---------------------------------------- | --------------------------------- |
| POST   | `/api/conversations/{id}/suggest-reply/` | Get AI-generated reply suggestion |

---

## WebSockets

Connect to a conversation's real-time channel:

```
ws://localhost:8000/ws/conversations/{id}/
```

### Event: `new_message`

Emitted whenever a new message is sent in the conversation.

```json
{
  "event": "new_message",
  "message": {
    "id": 1,
    "sender": "admin@test.com",
    "message": "Hello customer"
  }
}
```

---

## Example Requests

### Get Token

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@test.com", "password": "admin123"}'
```

### Send a Message

```bash
curl -X POST http://localhost:8000/api/conversations/1/messages/send/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "How can I help you today?"}'
```

### Acquire a Lock

```bash
curl -X POST http://localhost:8000/api/conversations/1/lock/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Running Tests

```bash
# Run test suite
docker compose exec web pytest

# With coverage report
docker compose exec web pytest --cov
```

---

## Roadmap

- [ ] WebSocket JWT authentication
- [ ] Per-endpoint rate limiting
- [ ] Conversation assignment workflow
- [ ] Prometheus metrics
- [ ] Structured audit logs
- [ ] OpenTelemetry tracing

---
