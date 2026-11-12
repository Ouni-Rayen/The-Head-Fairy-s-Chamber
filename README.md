# SHE HACKS: The Head Fairy's Chamber (request header manipulation)

Easy to medium web challenge. Flask, one container, no database.

## Deploy

```bash
FLAG='SheHacks{your_real_flag}' docker compose up -d --build
```

Open `http://<host>:8083`. Port taken? `HOST_PORT=8090 docker compose up -d --build`. Health check: `/health`.

## Description for players

> Three guards seal the head fairy's door, and your browser is not what any of them is looking for. Make them believe you, and bring back the secret behind the door.
>
> Flag format: `SheHacks{...}`

Suggested: category Web, difficulty Easy/Medium, about 150 points. Players need a tool that can edit requests: Burp, Caido, curl, or "Edit and Resend" in the browser DevTools (browsers will not let page JavaScript set `User-Agent`).

## Writeup (organizers only, do not publish)

The "Knock" button sends `POST /api/knock`. The server checks three headers in order, and each failure says which lock is still closed (`locks_open`).

1. `User-Agent` must contain `Specialist`. Failure: "You are no Specialist of ours."
2. `X-Forwarded-For` must be `127.0.0.1`. Failure: "come from inside Alfea's own walls".
3. `X-Fairy-Dust` must be `winx`. Failure: the pixie asks for `X-Fairy-Dust`.

Working request:

```bash
curl -s -X POST http://localhost:8083/api/knock \
  -H 'User-Agent: Red Fountain Specialist' \
  -H 'X-Forwarded-For: 127.0.0.1' \
  -H 'X-Fairy-Dust: winx'
```

The single hint is the `X-Guard-Note` response header on every `/api/knock` reply: guards only trust what a visitor announces in the request "envelope" (headers), and "a pixie's dust is the name of our club" (the value `winx`). It is only visible in the raw response (DevTools Network tab, Burp, `curl -i`).

## Notes

- The flag lives only in the `FLAG` environment variable.
- Nothing about the headers is validated against a real proxy: the first `X-Forwarded-For` entry is trusted on purpose.
