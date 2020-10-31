# crossroads website

> we'll CROSS that bridge when we get der

# dev

## running the app

```bash
cp docker-compose.override.yml.example docker-compose.override.yml
# (optionally) edit app configuration in docker-compose.override.yml

# run the frontend
cd web && yarn run webpack-dev-server --hot
docker-compose up -d --build
```

## useful commands

```bash
# format code
black --exclude migrations .

# execute a shell in the container
docker-compose exec app fish

# get the logs from the app
docker-compose logs -f app
```
