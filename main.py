from flask import session
import paypalrestsdk
from dotenv import load_dotenv
import os
from extensions import app, mysql, session_cleared
import routes
load_dotenv()

app.template_folder = "templates"
app.static_folder = "static"

app.secret_key = os.getenv("SECRET_KEY")

app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_PORT'] = int(os.getenv("MYSQL_PORT"))
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
})

@app.before_request
def clear_session_once():
    global session_cleared
    if not session_cleared:
        session.clear()
        session_cleared = True

if __name__ == '__main__':
    app.run(debug=True)
