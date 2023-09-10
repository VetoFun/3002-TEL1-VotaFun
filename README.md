# 3002-TEL1-VotaFan

1. To start all services: `docker-compose up -d`
2. To bring down services: `docker-compose down`
3. To view logs: `docker-compose logs`

- Alternatively, refer to the README for each service to see how to start it independently
- for backend development, i suggest starting flask and redis separately, ie create .venv, start flask, and start redis in Docker container. Redis is accessible on `localhost:6379`
