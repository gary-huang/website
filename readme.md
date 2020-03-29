# dev

```bash
# set-up local environment
$ cp .env.dev.template .env  # customize

# custom django local overrides
$ vim crossroads/settings/local.py

$ # format code
$ black --exclude migrations .

$ docker-compose up -d --build dev
```


# prod

```bash
$ cp .env.prod.template .env  # fill in with prod secrets
$ docker-compose up -d --build prod
```


# TODO/brainstorming
## priority
- [ ] rest of info pages
- [ ] prayer requests page
- [ ] site footer
- [ ] bible verse widget
- [ ] bootstrap scrollspy for service page navbar
- [ ] production docker config

## stretch
- [ ] alternate comment background colours
- [ ] find out how volunteer schedules are managed
- [x] collapsible service sections
- [ ] when service is "active" (during/before)
- [x] when audio/video is available after service post player at the top (or should be sticky to page)
- [ ] all sections collapse when service is over
- [ ] prayer items
- [ ] email functionality
  - [ ] email prayer digests

- [ ] real-time
  - [ ] follow-through of service (power-point guys would "advance the service")
  - [ ] mute feature to turn screen black during prayer, etc


POST APPROVAL
- [ ] log-in logic


# dev


```bash
$ docker-compose exec server bash
```

```bash
$ docker-compose logs -f server
```
