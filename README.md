# Bus Booking Platform – Cloud Deployment & CI/CD

A containerized bus trip and seat reservation REST API, deployed on AWS EC2 using Docker, PostgreSQL and Nginx, with automated CI/CD using GitHub Actions.

## Project Information

| Field | Details |
|---|---|
| Organization | ALGIONS AI LABS PRIVATE LIMITED |
| Project | Cloud Deployment & CI/CD – Bus Booking Platform |
| Role | DevOps & Cloud Engineering |
| Application | Bus Booking REST API |
| Deployment | AWS EC2 (Ubuntu) |

## Technology Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Cloud:** AWS EC2
- **Reverse Proxy:** Nginx
- **Testing:** Pytest
- **Code Quality:** Ruff

## Project Overview

The project implements a bus trip and seat reservation API. It provides endpoints for retrieving routes, viewing trips and available seats, creating bookings, retrieving booking details and cancelling reservations.

The application is containerized and deployed on an AWS EC2 Ubuntu instance. Nginx acts as a reverse proxy, while PostgreSQL stores application data.

## Key Features

- REST API built using FastAPI.
- Route and trip management.
- Seat availability and reservation.
- Booking creation and cancellation.
- PNR generation and booking retrieval.
- Duplicate confirmed seat reservation protection.
- PostgreSQL persistent storage.
- Docker-based application deployment.
- Automated CI/CD pipeline.
- Application health and database readiness checks.
- Database backup and restore procedures.

## System Architecture

```text
             Users / Browser
                    |
                    v
                AWS EC2
                    |
                    v
                 Nginx
              Reverse Proxy
                    |
                    v
             FastAPI Application
                    |
                    v
                PostgreSQL
                    |
                    v
             Persistent Volume
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Home |
| GET | `/health` | Application health |
| GET | `/ready` | Database readiness |
| GET | `/routes` | Get routes |
| GET | `/trips` | Get trips |
| GET | `/trips/{trip_id}/seats` | Get seats |
| POST | `/bookings` | Create booking |
| GET | `/bookings/{pnr}` | Retrieve booking |
| PATCH | `/bookings/{pnr}/cancel` | Cancel booking |

## Deployment

The application is deployed on AWS EC2 running Ubuntu.

**Public API Documentation:**  
http://13.239.41.176/docs

**Health Check:**  
http://13.239.41.176/health

**Readiness Check:**  
http://13.239.41.176/ready

The API is currently accessible over HTTP. HTTPS has not yet been configured.

## Docker Deployment

Build and start the application:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker ps
```

View application logs:

```bash
docker compose logs -f app
```

Check application health:

```bash
curl http://localhost:8000/health
```

## CI/CD Pipeline

GitHub Actions automates the following workflow:

1. Checkout repository.
2. Set up Python environment.
3. Install project dependencies.
4. Run Ruff code-quality checks.
5. Execute automated Pytest tests.
6. Build Docker image.
7. Upload test reports and Docker image build artifacts.

The workflow runs on pushes and pull requests to the configured branches.

## Testing

Automated API tests are maintained in the `tests/` directory.

Run tests locally:

```bash
pytest -v
```

Run code-quality checks:

```bash
ruff check app tests
```

## Backup and Recovery

PostgreSQL database backup is performed using `pg_dump`, and restoration is performed using `pg_restore`.

The project has been tested for:

- Database backup creation.
- Restoration into a separate test database.
- Verification of restored tables and records.
- Docker container restart and service recovery.

See [RUNBOOK.md](RUNBOOK.md) for operational procedures.

## Project Documentation

- [Architecture Documentation](ARCHITECTURE.md)
- [Operations Runbook](RUNBOOK.md)

## Repository

[GitHub – Bus Booking DevOps](https://github.com/Raj20042122/bus-booking-devops)

## Project Status

Core application development, containerization, CI/CD pipeline and AWS deployment have been completed. Database backup/restore and container recovery have also been verified.

Further improvements include HTTPS configuration and additional reliability testing.