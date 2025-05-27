from flask import Flask, jsonify, request, send_from_directory
import time, string, random, json, os

app = Flask(__name__, static_folder='public', static_url_path='')
DB_FILE = "keys.json"

def load_keys():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_keys(keys):
    with open(DB_FILE, "w") as f:
        json.dump(keys, f)

def generate_key():
    return "KEY-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@app.route("/api/generate")
def api_generate():
    keys = load_keys()
    key = generate_key()
    keys[key] = time.time()
    save_keys(keys)
    return jsonify({"key": key})

@app.route("/api/check")
def api_check():
    key = request.args.get("key")
    keys = load_keys()
    if key in keys:
        if time.time() - keys[key] < 86400:
            return "VALID"
        else:
            return "EXPIRED"
    return "INVALID"

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
