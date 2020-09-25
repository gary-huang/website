# crossroads website

> we'll CROSS that bridge when we get der

# dev

```bash
# set-up local environment
$ cp .env.dev.template .env  # customize

$ # format code
$ black --exclude migrations .

# run the frontend
$ cd web && yarn run webpack-dev-server --hot
# run the backend
$ docker-compose up -d --build dev
```


# prod

```bash
$ cp .env.prod.template .env  # fill in with prod secrets
$ docker-compose up -d --build prod
```


# dev

Useful commands

```bash
$ docker-compose exec dev bash
$ docker-compose logs -f dev
```
