cd deployment/pg
docker rm -f $(docker ps -aq)
docker volume rm $(docker volume ls -q)
docker compose up -d i2b2-ml i2b2-jupyter
docker rm -f i2b2-ml; docker-compose up -d  i2b2-ml;  docker-compose logs -f i2b2-ml