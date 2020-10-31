# crossroads website

> we'll CROSS that bridge when we get der

# dev

## running the app

```bash
cp docker-compose.override.yml.example docker-compose.override.yml

docker-compose up -d --build
```

The app will run by default on port 8000. This can be configured in
`docker-compose.override.yml`.

## useful commands

```bash
# format python code
black --exclude migrations .

# format ts/js code
yarn fmt

# execute a shell in the container
docker-compose exec app fish

# get the logs from the app
docker-compose logs -f app
```
