#!/bin/bash


sleep 10
alembic upgrade head
gunicorn app:app --bind 0.0.0.0:4800
