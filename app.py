# api/app.py

from flask import Flask, request, jsonify
import jwt
import os
import time

app = Flask(__name__)


SECRET_KEY = os.environ.get("SECRET_KEY")  
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Decode token run" })

@app.route('/decode', methods=['GET'])
def decode_jwt():
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        
        decoded = jwt.decode(token, options={"verify_signature": False})
        header = jwt.get_unverified_header(token)
        signature = token.split('.')[-1]

        
        now = int(time.time())
        exp = decoded.get("exp")
        is_expired = exp is not None and now > exp

        
        signature_valid = None
        if SECRET_KEY:
            try:
                jwt.decode(token, key=SECRET_KEY, algorithms=[header.get("alg", "HS256")])
                signature_valid = True
            except jwt.InvalidTokenError:
                signature_valid = False

        # Résumé
        valid = not is_expired and (signature_valid is not False)

        return jsonify({
            "valid": valid,
            "expired": is_expired,
            "signature_valid": signature_valid,
            "header": header,
            "payload": decoded,
            "signature": signature
        })

    except jwt.DecodeError:
        return jsonify({"error": "Invalid JWT token"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
