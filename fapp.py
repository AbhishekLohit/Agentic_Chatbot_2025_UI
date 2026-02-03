from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
from config import FASTAPI_URL, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Dummy users (replace with database in production)
users_db = {
    "Cust_0410": "pass123",
    "Cust_002": "mypassword"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        password = request.form.get("password")
        if customer_id in users_db and users_db[customer_id] == password:
            session['user_id'] = customer_id
            return redirect(url_for('chat'))
        else:
            return render_template("login.html", error="Invalid ID or password")
    return render_template("login.html")

@app.route("/chat")
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("index.html", user_id=session['user_id'])

@app.route("/get", methods=["POST"])
def get_bot_response():
    print("Inside get_bot_response")
    data = request.get_json()  # <-- Use JSON instead of form data
    user_msg = data.get("msg", "")
    user_id = session.get('user_id', 'default_user')

    try:
        res = requests.post(
            FASTAPI_URL,
            json={"customer_id": user_id,
                   "session_id":"sess123", 
                   "user_query": user_msg}
        )
        print(res.json())
        # bot_reply = res.json().get("entity_extraction_response", "No response from bot")
        bot_reply = str(res.json())
    except Exception as e:
        bot_reply = f"Error contacting FastAPI: {e}"

    return jsonify({"response": bot_reply})

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
