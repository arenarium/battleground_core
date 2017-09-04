docker-compose -f docker-compose-ui.yml -f docker-compose.prod.yml down
docker-compose -f docker-compose-ui.yml -f docker-compose.prod.yml pull
docker-compose -f docker-compose-ui.yml -f docker-compose.prod.yml up -d
