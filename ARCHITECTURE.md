# Bus Booking Platform – Architecture

## 1. Project Overview

A containerized bus trip and seat reservation API developed using FastAPI and PostgreSQL.

## 2. Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose
- GitHub Actions
- AWS EC2 (Ubuntu)
- Nginx
- Pytest
- Ruff

## 3. System Architecture

```text
                  Users / Browser
                         |
                         v
                  AWS EC2 Instance
                         |
                         v
                    Nginx :80
                  Reverse Proxy
                         |
                         v
                FastAPI Application
                  Docker :8000
                         |
                         v
                   PostgreSQL
                  Docker :5432
                         |
                         v
                  Persistent Volume
```

## 4. Application Components

- FastAPI: Provides REST API endpoints.
- PostgreSQL: Stores routes, stops, trips, seats and bookings.
- Docker: Packages the application and database services.
- Docker Compose: Manages containers and service dependencies.
- Nginx: Acts as the reverse proxy.
- GitHub Actions: Runs automated checks, tests and Docker image builds.

## 5. CI/CD Workflow

1. Developer pushes code to GitHub.
2. GitHub Actions starts the workflow.
3. Ruff performs code-quality checks.
4. Pytest executes automated API tests.
5. Docker image is built with a version-specific tag.
6. Build artifacts and test reports are uploaded.

## 6. Deployment

- Cloud provider: AWS
- Compute: EC2 instance
- Operating system: Ubuntu
- Application access: Nginx reverse proxy
- Database: PostgreSQL container
- Application health: /health
- Database readiness: /ready

## 7. Security

- Application runs as a non-root user inside its container.
- PostgreSQL is not directly exposed publicly.
- SSH access is restricted to the administrator's IP.
- Environment variables are used for configuration.
- Persistent storage is configured for PostgreSQL.

## 8. Backup and Recovery

PostgreSQL backups are created using pg_dump and restored using pg_restore. Docker Compose restart is used to verify service recovery.