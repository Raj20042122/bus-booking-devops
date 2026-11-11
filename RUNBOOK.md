# Bus Booking Platform – Operations Runbook

## 1. Project Information

Application: Bus Booking API  
Deployment: AWS EC2 Ubuntu  
Application: FastAPI  
Database: PostgreSQL  
Reverse Proxy: Nginx

## 2. Access the Server

Connect through SSH:

```bash
ssh -i "bus-booking-key.pem" ubuntu@YOUR_PUBLIC_IP
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

View container logs:

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

## 4. Health Checks

Application health:

```bash
curl http://localhost:8000/health
```

Database readiness:

```bash
curl http://localhost:8000/ready
```

## 5. Nginx Management

Check Nginx:

```bash
sudo systemctl status nginx --no-pager
```

Validate configuration:

```bash
sudo nginx -t
```

Restart Nginx:

```bash
sudo systemctl restart nginx
```

## 6. Database Backup

Create a PostgreSQL backup:

```bash
sudo docker exec busbooking-db pg_dump -U bususer -d busbooking -F c -f /tmp/busbooking_backup.dump
```

Copy backup to the server:

```bash
sudo docker cp busbooking-db:/tmp/busbooking_backup.dump ~/busbooking_backup.dump
```

## 7. Database Restore

Create a test database:

```bash
sudo docker exec busbooking-db createdb -U bususer busbooking_restore_test
```

Restore the backup:

```bash
sudo docker exec -i busbooking-db pg_restore -U bususer -d busbooking_restore_test --clean --if-exists < ~/busbooking_backup.dump
```

Verify tables:

```bash
sudo docker exec busbooking-db psql -U bususer -d busbooking_restore_test -c "\dt"
```

## 8. Troubleshooting

If the application is unhealthy:

1. Check container status.
2. Inspect application logs.
3. Check PostgreSQL health.
4. Check Nginx status.
5. Restart the affected service.
6. Verify /health and /ready.

## 9. Recovery Evidence

The project has been tested for:

- Docker container restart and recovery.
- PostgreSQL backup creation.
- Database restore into a separate test database.
- Verification of restored tables and records.

## 10. Important Safety Notes

- Never commit `.env` or private SSH keys.
- Never run `docker compose down -v` unless intentionally deleting persistent database data.
- Keep backup files in a secure location.