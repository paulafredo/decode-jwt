# api/app.py

from flask import Flask, request, jsonify
import jwt
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Decode token run" })

@app.route('/decode', methods=['GET'])
def decode_jwt():
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        # It's generally unsafe to not verify the signature in production.
        # This is for demonstration/decoding purposes only.
        decoded = jwt.decode(token, options={"verify_signature": False})
        header = jwt.get_unverified_header(token)
        return jsonify({
            "header": header,
            "payload": decoded,
            "signature": token.split('.')[-1]
        })
    except jwt.DecodeError:
        return jsonify({"error": "Invalid JWT token"}), 400

# This line is crucial for Vercel to recognize your Flask app
# handler = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)