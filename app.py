from flask import Flask, request, jsonify
from flask_cors import CORS
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from database import collection
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

@app.route("/send-email", methods=["POST"])
def send_marketing_email():
    data = request.json
    recipient = data["recipient"]
    subject = data["subject"]
    body = data["body"]

    message = Mail(
        from_email="sinhalipika2000@gmail.com",
        to_emails=recipient,
        subject=subject,
        html_content=body,
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return jsonify({"message": "Email sent", "status": response.status_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.json
    result = collection.insert_one(data)

    try:
        recipient = data["contactDetails"]["email"]
        name = data["contactDetails"]["name"]
        date = data["date"]
        subject = "Appointment Confirmation"
        body = f"<p>Hi {name},</p><p>Your car service appointment is booked for {date}.</p>"

        message = Mail(
            from_email="sinhalipika2000@gmail.com",
            to_emails=recipient,
            subject=subject,
            html_content=body,
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print("Failed to send acknowledgment email:", str(e))

    return jsonify({"message": "Appointment created", "id": str(result.inserted_id)}), 201


@app.route("/appointments", methods=["GET"])
def get_appointments():
    appointments = []
    for appt in collection.find():
        appt["_id"] = str(appt["_id"])
        appointments.append(appt)
    return jsonify(appointments)

@app.route("/")
def index():
    return jsonify({"message": "Car Workshop Appointment API Running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)