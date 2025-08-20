from flask import Flask, request, jsonify, render_template
import uuid, socket

app = Flask(__name__)

# --- helper to get local IP ---
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# generate a test API key
TEST_KEY = str(uuid.uuid4())
print("Test API key:", TEST_KEY)

LOCAL_IP = get_local_ip()
PORT = 31621
#PORT = 5000
@app.route("/public", methods=["GET"])
def public():
    if "text/html" in request.headers.get("Accept", ""):
        return render_template(
            "public.html",
            message="Hello from public endpoint",
            ip=LOCAL_IP,
            port=PORT
        )
    return jsonify(message="Hello from public endpoint")

@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_data(as_text=True)
    print(f"[ECHO ENDPOINT] Received: {data}")
    return jsonify(you_sent=data)

@app.route("/protected", methods=["GET"])
def protected():
    api_key = request.headers.get("x-api-key")
    if api_key != TEST_KEY:
        return jsonify(error="Missing/invalid API key"), 401
    return jsonify(message="You accessed a protected resource!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
