# Day 08 - Pydantic Schemas and Database CRUD

## Backend Architecture

Client
↓
HTTP Request
↓
FastAPI
↓
Pydantic
↓
SQLAlchemy ORM
↓
Session
↓
MySQL


## File Responsibilities

.env
- Database configuration

database.py
- Load environment variables
- Create DATABASE_URL
- Create Engine
- Create SessionLocal

models.py
- SQLAlchemy ORM models
- Map Python classes to database tables

schemas.py
- Define request and response data structures
- Validate HTTP data

main.py
- Define API routes
- Execute CRUD business logic


## ORM

ORM = Object Relational Mapping

Python class
↔
Database table

Python object
↔
Database row


## CRUD Patterns

CREATE

ORM object
→ db.add()
→ db.commit()
→ db.refresh()


READ

select()
→ db.scalars()
→ .all() / .first()


UPDATE

select()
→ modify ORM object
→ db.commit()
→ db.refresh()


DELETE

select()
→ db.delete()
→ db.commit()


## Important Difference

Pydantic Schema
- HTTP data

SQLAlchemy Model
- Database mapping

Session
- Database operations and transactions


## Current Session Management

Current version:

db = SessionLocal()

...

db.close()

This is intentionally explicit for learning.

Next step:
FastAPI dependency injection with get_db() and Depends().