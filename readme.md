# RoleForum

A role-based blog/forum REST API built with FastAPI — public content, private permissions, and admin moderation.

## What it does

- **Public access** — anyone can read posts and comments, no account needed
- **Authenticated writes** — only logged-in users can create posts and comments
- **Ownership-based editing** — users can edit or delete their own posts/comments
- **Admin override** — admins can edit or delete *any* post or comment, regardless of ownership
- **JWT authentication** — hashed passwords, signed/expiring tokens, protected routes

## Stack

Python · FastAPI · PostgreSQL · SQLAlchemy · Alembic · JWT · Docker

## Data model

- **User** — has a `role` (`user` or `admin`)
- **Post** — belongs to one User (author)
- **Comment** — belongs to both a Post and a User simultaneously

## Permission logic

| Action | Who can do it |
|---|---|
| Read posts/comments | Anyone (public) |
| Create post/comment | Any logged-in user |
| Edit/delete a post or comment | The author, **or** an admin |

## Setup

1. Clone the repo and create a virtual environment:
```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in your own values (database credentials, JWT secret key).

3. Start the database:
```bash
   docker-compose up -d
```

4. Run migrations:
```bash
   alembic upgrade head
```

5. Start the server:
```bash
   uvicorn main:app --reload
```

6. Open `http://127.0.0.1:8000/docs` for the interactive API docs.

## API overview

- `POST /auth/register` — create an account
- `POST /auth/login` — get a JWT access token
- `GET /auth/me` — get your own account details (protected)
- `GET /post/` — list all posts (public)
- `GET /post/{id}` — get a single post (public)
- `POST /post/` — create a post (protected)
- `PUT /post/{id}` / `DELETE /post/{id}` — edit/delete a post (owner or admin)
- `GET /comment/{post_id}` — list comments on a post (public)
- `POST /comment/{post_id}` — add a comment (protected)
- `PUT /comment/{id}` / `DELETE /comment/{id}` — edit/delete a comment (owner or admin)

## Notes

This project was built to learn authorization beyond simple ownership — specifically, role-based access where an admin can act on behalf of any user. Every permission path (owner success, non-owner rejection, admin override) was manually tested with multiple accounts before being considered complete.