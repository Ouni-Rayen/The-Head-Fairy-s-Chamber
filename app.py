import os

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="/static")

FLAG = os.environ.get("FLAG", "SheHacks{Th3_Gu4rd_Tru5ts_Wh4t_Y0u_S4y}")

# The only hint in the whole challenge. It rides on every /api/knock response,
# so players only see it by reading raw responses (DevTools Network tab, Burp, curl -i).
GUARD_NOTE = (
    "The guards ignore what the page says. They only trust what a visitor "
    "announces in the envelope of the request, and a pixie's dust is the name of our club."
)


def client_ip():
    xff = request.headers.get("X-Forwarded-For", "")
    return xff.split(",")[0].strip() if xff else ""


def reply(payload, status=200):
    resp = jsonify(payload)
    resp.status_code = status
    resp.headers["X-Guard-Note"] = GUARD_NOTE
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/knock", methods=["GET", "POST"])
def knock():
    # Lock 1: who are you? (User-Agent)
    if "specialist" not in request.headers.get("User-Agent", "").lower():
        return reply({
            "ok": False, "locks_open": 0,
            "message": "The Red Fountain guard studies your badge. 'You are no Specialist of ours.'",
        }, 403)

    # Lock 2: where do you come from? (X-Forwarded-For)
    if client_ip() not in ("127.0.0.1", "::1"):
        return reply({
            "ok": False, "locks_open": 1,
            "message": "The gate only opens for those who come from inside Alfea's own walls.",
        }, 403)

    # Lock 3: the pixie wants her dust. (X-Fairy-Dust)
    if request.headers.get("X-Fairy-Dust", "").strip().lower() != "winx":
        return reply({
            "ok": False, "locks_open": 2,
            "message": "A pixie hovers by the keyhole. 'Show me some X-Fairy-Dust, dear.'",
        }, 403)

    return reply({
        "ok": True, "locks_open": 3,
        "message": "All three locks glow. The head fairy's door swings open.",
        "flag": FLAG,
    })


@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
