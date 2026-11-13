
# Bus Booking Platform – Operations Runbook

## 1. Project Information

- **Application:** Bus Booking API
- **Deployment:** AWS EC2 Ubuntu
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Containerization:** Docker and Docker Compose
- **Reverse Proxy:** Nginx

## 2. Access the Server

Connect to the EC2 instance through SSH:

```bash
ssh -i "bus-booking-key.pem" ubuntu@13.239.41.176
```

Navigate to the project directory:

```bash
cd ~/bus-booking-devops
```

## 3. Container Management

View running containers:

```bash
sudo docker ps
```

View all containers, including stopped containers:

```bash
sudo docker ps -a
```

View combined container logs:

```bash
sudo docker compose logs -f
```

Restart services:

```bash
sudo docker compose restart
```

Stop services:

```bash
sudo docker compose down
```

Start services:

```bash
sudo docker compose up -d
```

Check Docker Compose service status:

```bash
sudo docker compose ps
```

## 4. Health Checks

Check application health:

```bash
curl http://localhost:8000/health
```

Check application readiness and database connectivity:

```bash
curl http://localhost:8000/ready
```

Expected responses:

**Health endpoint:**

```json
{
  "status": "healthy"
}
```

**Readiness endpoint:**

```json
{
  "status": "ready",
  "database": "connected"
}
```

Public endpoints:

- Health: http://13.239.41.176/health
- Readiness: http://13.239.41.176/ready
- API Documentation: http://13.239.41.176/docs

## 5. Nginx Management

Check Nginx status:

```bash
sudo systemctl status nginx --no-pager
```

Validate Nginx configuration:

```bash
sudo nginx -t
```

Restart Nginx:

```bash
sudo systemctl restart nginx
```

Reload Nginx configuration:

```bash
sudo systemctl reload nginx
```

View Nginx error logs:

```bash
sudo tail -n 100 /var/log/nginx/error.log
```

## 6. Database Backup

Create a PostgreSQL backup inside the database container:

```bash
sudo docker exec busbooking-db pg_dump -U bususer -d busbooking -F c -f /tmp/busbooking_backup.dump
```

Copy the backup from the container to the EC2 host:

```bash
sudo docker cp busbooking-db:/tmp/busbooking_backup.dump ~/busbooking_backup.dump
```

Restrict access to the backup file:

```bash
chmod 600 ~/busbooking_backup.dump
```

Verify the backup file:

```bash
ls -lh ~/busbooking_backup.dump
```

The backup is stored in PostgreSQL custom dump format.

## 7. Database Restore

**Important:** Perform restoration in a separate test database to avoid overwriting production data.

Create a test database:

```bash
sudo docker exec busbooking-db createdb -U bususer busbooking_restore_test
```

Restore the backup:

```bash
sudo docker exec -i busbooking-db pg_restore -U bususer -d busbooking_restore_test --clean --if-exists < ~/busbooking_backup.dump
```

Verify restored tables:

```bash
sudo docker exec busbooking-db psql -U bususer -d busbooking_restore_test -c "\dt"
```

Verify restored record counts:

```bash
sudo docker exec busbooking-db psql -U bususer -d busbooking_restore_test -c "SELECT COUNT(*) FROM routes; SELECT COUNT(*) FROM trips; SELECT COUNT(*) FROM seats; SELECT COUNT(*) FROM bookings;"
```

## 8. Troubleshooting

If the application becomes unhealthy, follow these steps.

### Step 1: Check container status

```bash
sudo docker ps -a
```

### Step 2: Inspect application logs

```bash
sudo docker logs busbooking-api --tail 100
```

### Step 3: Inspect database logs

```bash
sudo docker logs busbooking-db --tail 100
```

### Step 4: Check PostgreSQL health

```bash
sudo docker exec busbooking-db pg_isready -U bususer -d busbooking
```

### Step 5: Check Nginx status

```bash
sudo systemctl status nginx --no-pager
```

Validate its configuration:

```bash
sudo nginx -t
```

### Step 6: Restart services if necessary

```bash
sudo docker compose restart
```

If Nginx is not running:

```bash
sudo systemctl restart nginx
```

### Step 7: Verify recovery

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
```

Also verify public access:

```bash
curl http://13.239.41.176/health
```

## 9. Recovery Evidence

The project has been tested for:

- Docker container restart and recovery.
- PostgreSQL backup creation.
- Database restoration into a separate test database.
- Verification of restored database tables and records.
- Application health verification after restart.
- Database readiness verification after restart.
- Concurrent booking requests to verify duplicate seat prevention.
- Booking cancellation and status verification.

## 10. Important Safety Notes

- Never commit `.env` files or private SSH keys to GitHub.
- Never run `docker compose down -v` unless intentionally deleting persistent database data.
- Keep database backups in a secure location.
- Restrict access to backup files.
- Do not expose PostgreSQL port 5432 publicly.
- Keep SSH access restricted to trusted IP addresses.
- Do not expose the application port 8000 publicly when Nginx is configured as the reverse proxy.
- Verify the backup and restore process before relying on a backup for recovery.
- Avoid modifying the production database during testing.
- Keep application and database logs available for troubleshooting.

---

**End of Operations Runbook**
