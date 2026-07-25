from flask import Flask, jsonify, request

app = Flask(__name__)

# এটি আপনার ইউজার ডাটাবেজ (সহজে বোঝার জন্য ডিকশনারি হিসেবে দেওয়া হলো)
# চাইলে এখানে লিসেন্স কি (Key) বা পিসির Hardware ID ব্যবহার করতে পারেন
VALID_LICENSES = {
    "USER-101": {"name": "Sultan Sheikh", "active": True},
    "USER-102": {"name": "Rahim Ahmed", "active": False}, # বন্ধ করা আছে
}

@app.route('/verify', methods=['POST'])
def verify_license():
    data = request.get_json()
    license_key = data.get('license_key', '')

    user = VALID_LICENSES.get(license_key)

    if user and user['active']:
        return jsonify({
            "status": "success",
            "message": f"Welcome {user['name']}!",
            "allowed": True
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "আপনার সাবস্ক্রিপশন শেষ হয়ে গেছে বা সফটওয়্যারটি বন্ধ করা হয়েছে!",
            "allowed": False
        }), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)