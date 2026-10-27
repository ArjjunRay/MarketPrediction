.PHONY: help up down logs backend-test backend-check frontend-test frontend-check frontend-e2e check

help:
	@echo "QStream local commands"
	@echo "  make up             Start the base Docker Compose stack"
	@echo "  make down           Stop the stack"
	@echo "  make check          Run backend and frontend checks"

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

backend-test:
	cd backend && uv run pytest

backend-check:
	cd backend && uv run ruff check . && uv run mypy app

frontend-test:
	cd frontend && npm test

frontend-check:
	cd frontend && npm run format:check && npm run lint && npm run typecheck

frontend-e2e:
	cd frontend && npm run test:e2e

check: backend-check backend-test frontend-check frontend-test
