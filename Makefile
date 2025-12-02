# Geonosis Makefile
# ==================
# Development commands for the Geonosis monorepo
# Note: Windows users should use WSL or Git Bash

.DEFAULT_GOAL := help

.PHONY: help install setup-api db-start db-stop db-reset dev-api dev-ui dev \
        docker-up docker-down docker-logs docker-build \
        test test-api test-ui lint format \
        migrate migrate-create clean clean-docker

# ============================================
# Help
# ============================================

help:
	@echo ""
	@echo "Geonosis Development Commands"
	@echo "=============================="
	@echo ""
	@echo "First-time Setup:"
	@echo "  make install        Install all dependencies (Node.js + Python)"
	@echo "  make setup-api      Create Python venv and install requirements"
	@echo ""
	@echo "Database:"
	@echo "  make db-start       Start PostgreSQL container"
	@echo "  make db-stop        Stop PostgreSQL container"
	@echo "  make db-reset       Reset database (destroys all data)"
	@echo ""
	@echo "Development Servers:"
	@echo "  make dev-api        Start FastAPI development server"
	@echo "  make dev-ui         Start Next.js development server"
	@echo "  make dev            Show instructions for running both servers"
	@echo ""
	@echo "Docker (Full Stack):"
	@echo "  make docker-up      Start all services in Docker"
	@echo "  make docker-down    Stop all Docker services"
	@echo "  make docker-logs    Follow logs for all services"
	@echo "  make docker-build   Build all Docker containers"
	@echo ""
	@echo "Testing:"
	@echo "  make test           Run all tests"
	@echo "  make test-api       Run API tests"
	@echo "  make test-ui        Run UI tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           Run linters"
	@echo "  make format         Format code with Prettier"
	@echo ""
	@echo "Database Migrations:"
	@echo "  make migrate        Run pending migrations"
	@echo "  make migrate-create Create a new migration"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Remove generated files and caches"
	@echo "  make clean-docker   Remove Docker containers, images, and volumes"
	@echo ""

# ============================================
# First-time Setup
# ============================================

## Install all dependencies (npm install at root, npm install in apps/ui, and setup-api)
install:
	@echo "Installing root dependencies..."
	npm install
	@echo "Installing UI dependencies..."
	cd apps/ui && npm install
	@echo "Setting up API..."
	$(MAKE) setup-api
	@echo ""
	@echo "✓ All dependencies installed!"

## Create Python virtual environment and install requirements
setup-api:
	@echo "Creating Python virtual environment..."
	cd apps/api && python3 -m venv venv
	@echo "Installing Python dependencies..."
	cd apps/api && . venv/bin/activate && pip install -r requirements.txt
	@echo ""
	@echo "✓ API setup complete!"

# ============================================
# Database
# ============================================

## Start PostgreSQL container
db-start:
	@echo "Starting PostgreSQL..."
	docker-compose up -d db
	@echo "✓ PostgreSQL is running on port 5432"

## Stop PostgreSQL container
db-stop:
	@echo "Stopping PostgreSQL..."
	docker-compose stop db
	@echo "✓ PostgreSQL stopped"

## Reset database (destroys all data)
db-reset:
	@echo "Resetting database..."
	docker-compose down -v
	docker-compose up -d db
	@echo "✓ Database reset complete"

# ============================================
# Development Servers
# ============================================

## Start FastAPI development server with hot reload
dev-api:
	@echo "Starting FastAPI server..."
	cd apps/api && . venv/bin/activate && uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

## Start Next.js development server
dev-ui:
	@echo "Starting Next.js server..."
	cd apps/ui && npm run dev

## Show instructions for running both development servers
dev:
	@echo ""
	@echo "To run the full development environment, open two terminals:"
	@echo ""
	@echo "  Terminal 1 (API):  make dev-api"
	@echo "  Terminal 2 (UI):   make dev-ui"
	@echo ""
	@echo "Or use Docker for the full stack:"
	@echo ""
	@echo "  make docker-up"
	@echo ""

# ============================================
# Docker (Full Stack)
# ============================================

## Start all services in Docker
docker-up:
	@echo "Starting all services..."
	docker-compose up -d
	@echo ""
	@echo "✓ Services started!"
	@echo "  - API: http://localhost:8000"
	@echo "  - UI:  http://localhost:3000"
	@echo ""

## Stop all Docker services
docker-down:
	@echo "Stopping all services..."
	docker-compose down
	@echo "✓ All services stopped"

## Follow logs for all services
docker-logs:
	docker-compose logs -f

## Build all Docker containers
docker-build:
	@echo "Building all containers..."
	docker-compose build
	@echo "✓ Build complete"

# ============================================
# Testing (placeholder for later)
# ============================================

## Run all tests
test:
	@echo "Tests not yet implemented"

## Run API tests
test-api:
	@echo "API tests not yet implemented"

## Run UI tests
test-ui:
	@echo "UI tests not yet implemented"

# ============================================
# Code Quality (placeholder for later)
# ============================================

## Run linters via Turborepo
lint:
	npm run lint

## Format code with Prettier
format:
	npx prettier --write "**/*.{js,jsx,ts,tsx,json,md}"

# ============================================
# Database Migrations (placeholder for later)
# ============================================

## Run pending database migrations
migrate:
	@echo "Migrations not yet configured"

## Create a new migration
migrate-create:
	@echo "Migrations not yet configured"

# ============================================
# Cleanup
# ============================================

## Remove generated files and caches
clean:
	@echo "Cleaning generated files..."
	rm -rf node_modules
	rm -rf apps/ui/node_modules
	rm -rf apps/ui/.next
	rm -rf apps/api/venv
	rm -rf apps/api/__pycache__
	rm -rf apps/api/src/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .turbo
	@echo "✓ Cleanup complete"

## Remove Docker containers, images, and volumes for this project
clean-docker:
	@echo "Cleaning Docker resources..."
	docker-compose down -v --rmi local
	@echo "✓ Docker cleanup complete"
