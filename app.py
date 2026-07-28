from flask import Flask, jsonify, request

app = Flask(__name__)

# ইউজার লিসেন্স ডাটাবেজ
VALID_LICENSES = {
    "USER-101": {"name": "Sultan Sheikh", "active": False},
    "USER-102": {"name": "Rahim Ahmed", "active": False},
        "Sultan-20066": {"name": "Rahim Ahmed", "active": True}, # নিষ্ক্রিয় অ্যাকাউন্ট
}

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Server is running!"}), 200

@app.route('/verify', methods=['POST'])
def verify_license():
    try:
        data = request.get_json() or {}
        license_key = data.get('license_key', '')

        user = VALID_LICENSES.get(license_key)

        if user and user['active']:
            return jsonify({
                "status": "success",
                "message": f"স্বাগতম {user['name']}!",
                "allowed": True
            }), 200
        elif user and not user['active']:
            return jsonify({
                "status": "error",
                "message": "আপনার সাবস্ক্রিপশন শেষ হয়ে গেছে বা সফটওয়্যারটি বন্ধ করা হয়েছে!",
                "allowed": False
            }), 403
        else:
            return jsonify({
                "status": "error",
                "message": "অবৈধ লিসেন্স কী (Invalid License Key)!",
                "allowed": False
            }), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "allowed": False}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
