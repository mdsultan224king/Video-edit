from flask import Flask, jsonify, request

app = Flask(__name__)

# 🔒 অনুমোদিত HWID ডাটাবেজ (HWID অনুযায়ী ইউজারের তথ্য)
VALID_HWIDS = {
    "92851BF2-1ADC-DE1E-A7A6-345A6001C880": {
        "name": "Sultan Sheikh",
        "active": True,
    },
    "4C4C4544-004B-4D10-8032-B2C04F423532": {
        "name": "User 2",
        "active": True,
    },
    # নতুন কোনো পিসি যুক্ত করতে চাইলে নিচে এভাবে HWID বসিয়ে দিবেন
}


@app.route("/", methods=["GET"])
def home():
  return jsonify({"status": "Server is running!"}), 200


@app.route("/verify", methods=["POST"])
def verify_license():
  try:
    data = request.get_json() or {}

    # ক্লায়েন্ট থেকে আসা HWID সংগ্রহ
    user_hwid = data.get("hwid", "").strip()

    if not user_hwid:
      return (
          jsonify({
              "status": "error",
              "message": "পিসির HWID পাওয়া যায়নি!",
              "allowed": False,
          }),
          400,
      )

    # ডাটাবেজে HWID সার্চ করা
    user = VALID_HWIDS.get(user_hwid)

    if user and user.get("active"):
      return (
          jsonify({
              "status": "success",
              "message": (
                  f"ডিভাইস ভ্যালিডেশন সফল! স্বাগতম {user.get('name')}।"
              ),
              "allowed": True,
          }),
          200,
      )

    elif user and not user.get("active"):
      return (
          jsonify({
              "status": "error",
              "message": (
                  "আপনার ডিভাইসের সাবস্ক্রিপশন শেষ বা বন্ধ করে দেওয়া হয়েছে!"
              ),
              "allowed": False,
          }),
          403,
      )

    else:
      return (
          jsonify({
              "status": "error",
              "message": "এই পিসিতে সফটওয়্যারটি ব্যবহারের অনুমতি নেই!",
              "allowed": False,
          }),
          404,
      )

  except Exception as e:
    return (
        jsonify({"status": "error", "message": str(e), "allowed": False}),
        500,
    )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
