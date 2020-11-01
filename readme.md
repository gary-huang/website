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

## adding a dependency

```bash
docker-compose run web yarn add <dep>
docker-compose up -d --build
```

## useful commands

```bash
# format python code
docker-compose run app black --exclude migrations .

# format ts/js code
docker-compose run web yarn fmt

# execute a shell in the server container
docker-compose exec app fish

# get the logs from the app
docker-compose logs -f app web
```
