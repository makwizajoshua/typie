# Typie Backend

Typie is an early-stage backend for a chat application. It is built with FastAPI,
SQLAlchemy, and Pydantic. The current code defines users, chatrooms, and messages,
with initial HTTP routes for account operations, chatroom membership, and message
history.

> **Project status:** this is a work in progress, not a production-ready chat
> service. Several route implementations and other parts of application startup
> are incomplete. The feature descriptions below report what the code currently
> attempts to provide, not a guarantee that every endpoint works.

## Contents

- [Current features](#current-features)
- [API routes](#api-routes)
- [Data model](#data-model)
- [Configuration and running](#configuration-and-running)
- [Known issues and remaining work](#known-issues-and-remaining-work)
- [Project layout](#project-layout)

## Current features

- **FastAPI application:** creates an app titled `Typie`, registers auth,
  chatroom, and message routers, and defines `GET /health`.
- **Relational models:** users, chatrooms, and messages are represented with
  SQLAlchemy models. Chatrooms and users have a many-to-many membership
  association; messages belong to a chatroom.
- **Account route scaffolding:** registration checks for an existing username
  and email; login looks up a user by username and email.
- **Chatroom operations:** create a named room with existing users, list rooms
  associated with a user, join a room, and delete a room.
- **Message history route:** queries messages by chatroom ID.
- **JWT helpers:** utility functions exist to issue and validate JWTs, but the
  account routes do not yet use them.
- **Connection manager scaffold:** an in-memory WebSocket connection manager
  supports accepting connections and sending personal or broadcast text. It is
  not connected to a working messaging endpoint.
- **Health check:** `GET /health` returns `{"status": "ok"}` when the application
  has started successfully.

## API routes

These are the routes registered by `src/main.py`. A route being listed here
means it is present in the application source; see [Known issues and remaining
work](#known-issues-and-remaining-work) for current limitations.

| Method | Path | Purpose | Current behavior / limitation |
|---|---|---|---|
| `GET` | `/health` | Basic health response | Returns a static `status` value. Does not check database connectivity. |
| `POST` | `/auth/register` | Register a user | Checks username/email uniqueness, then attempts to insert a user. The request has no password and the model requires `password_hash`; the handler also does not return a response. |
| `POST` | `/auth/login` | Log in | Looks up the submitted username and email separately. Password verification and token creation are TODOs; the handler does not return a response. |
| `GET` | `/chatroom/all/{user_id}` | List rooms for a user | Joins rooms to clients and filters on the user ID. Response shape needs correction and is not explicitly documented by a response schema. |
| `POST` | `/chatroom/create` | Create a room | Accepts a name and a list of client IDs, looks up users, and creates a room if at least one user is found. |
| `POST` | `/chatroom/join/{chatroom_id}?user_id={user_id}` | Join a room | Checks for the room and user, then appends the user if they are not already a member. |
| `DELETE` | `/chatroom/delete/{chatroom_id}` | Delete a room | Deletes the room if it exists. |
| `GET` | `/message/all/{chatroom_id}` | Get room messages | Queries messages by room ID. The current implementation returns ORM rows instead of the response objects it builds, and the response schema does not match the model's `author` field. |
| WebSocket | `/message/message/ws/{chatroom_id}` | Intended to send messages | The current handler is not implemented as a working WebSocket handler; it takes a Pydantic message body and database dependency but does not accept or use a WebSocket connection. |

### Example chatroom request

The chatroom schema expects a name and client user IDs:

```json
{
  "name": "General",
  "clients": [1, 2]
}
```

`POST /chatroom/create` currently requires at least one of the supplied IDs to
match a user in the database. `clients` contains IDs in the request; the ORM
relationship itself contains `User` objects.

### Routes present in source but not registered

- `src/routers/user_router.py` defines `GET /user/user/{user_id}`, but
  `src/main.py` does not include that router.
- `src/routers/chatroom.py` is a second chatroom router module and is not the
  module included by `src/main.py`. Its extra `PATCH /chatroom/update/{chatroom_id}`
  route is therefore not part of the current application API.

## Data model

- **User (`users`):** integer ID, unique username and email, required
  `password_hash`, creation timestamp, optional image filename, and chatroom
  memberships.
- **ChatRoom (`chatrooms`):** integer ID, unique indexed name, user memberships,
  and messages.
- **Chatroom membership (`chatroom_clients`):** association table linking user
  IDs to chatroom IDs.
- **Message (`messages`):** integer ID, author ID value, content (up to 512
  characters), creation timestamp, and required chatroom ID.

The `Message.author` field is currently a plain integer, not a foreign key or
relationship to `User`. The models are currently created with
`Base.metadata.create_all()` at application import time; there is no migration
system in the project configuration.

## Configuration and running

The dependency list is in `pyproject.toml` (also mirrored in
`requirements.txt`) and requires Python 3.11 or newer. The application uses
`python-dotenv` to load configuration from a `.env` file in the working
directory. Start by copying `.env.example` to `.env`.

### Database URL

`src/db.py` uses `DATABASE_URL` to configure SQLAlchemy. If it is unset, the
application defaults to a local SQLite database at `./database.db` (relative
to the process working directory). SQLite connections are configured for use
from FastAPI's request threads. PostgreSQL is also supported through the
`psycopg` driver listed in the project dependencies.

Local SQLite example:

```dotenv
DATABASE_URL=sqlite:///./database.db
```

PostgreSQL example:

```dotenv
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/typie
```

Replace the example credentials with your own, and URL-encode special
characters in the username or password. Do not commit `.env` or real
credentials.

### Other environment variables

- `SECRET_KEY`: secret used by the JWT helper functions. Use a unique,
  randomly generated value outside local development.
- `TOKEN_HOURS`: JWT lifetime in hours, required by the token-creation helper.
  The example sets it to `24`.

These authentication helpers are not yet wired into the account routes, so
setting the JWT variables does not currently enable login or protected API
access.

## Known issues and remaining work

### Blocking basic use

1. **Fix application startup paths.** Ensure model imports and static/template
   paths work consistently from the documented launch location.
2. **Add database migrations.** `create_all()` does not update existing tables
   when model definitions change. Add a migration tool and a migration for the
   chatroom membership association table and any existing databases.
3. **Finish registration and login.** Add password input to the appropriate
   schema, hash passwords before storing them, verify passwords at login, return
   the declared response models, and issue JWTs.
4. **Protect routes.** Apply the current-user dependency to endpoints that
   require an authenticated user. Derive the acting user from the token rather
   than trusting a caller-supplied user ID.
5. **Repair message history output.** Return the constructed response objects or
   enable ORM attribute mapping, align `author`/`author_id`, and define ordering
   and pagination.
6. **Implement realtime messaging.** Use a `WebSocket` parameter, accept and
   cleanly disconnect connections, scope connections to chatrooms, persist
   messages, and broadcast messages to the right room. Decide and document the
   message protocol and error behavior.

### Complete and harden the API

- Add response schemas for chatroom and message operations and ensure they
  serialize ORM objects correctly.
- Decide how to handle partially invalid client ID lists when creating a room;
  currently invalid IDs are ignored if some valid users were found.
- Add the chatroom update operation to the registered router only after its
  behavior and request semantics are defined.
- Register or remove the user router, and avoid keeping duplicate chatroom
  router implementations that can drift apart.
- Add foreign keys/relationships for message authors, and define delete and
  membership behavior explicitly.
- Configure CORS for the actual frontend origins; the current middleware does
  not explicitly list allowed origins.
- Add validation and consistent error responses for missing resources,
  duplicate names, invalid IDs, and unauthorized access.
- Use a managed connection lifecycle for WebSockets and handle stale
  connections during broadcasts.
- Add automated tests for schemas, route behavior, authorization, ORM
  relationships, database migrations, and WebSocket communication.
- Add operational documentation for supported database engines, environment
  variables, startup commands, and deployment.

## Project layout

```text
src/
  core/          WebSocket connection manager
  models/        SQLAlchemy user, chatroom, and message models
  routers/       FastAPI route modules
  schemas/       Pydantic request and response schemas
  db.py          SQLAlchemy engine, declarative base, and DB dependency
  main.py        FastAPI app and registered routers
```