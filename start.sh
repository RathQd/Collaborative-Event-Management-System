#!/bin/bash
set -e
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 9099