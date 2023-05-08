from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3

app = Flask(__name__)

SERVICES = {
    "1": "Event registration",
    "2": "Ticket payment",
    "3": "Location information"
}

def handle_message(body):
    message = body.lower()
    resp = MessagingResponse()
    responded = False

    if message == 'hi':
        resp.message(
            "Welcome to our event services bot! Please select a service by replying with the corresponding number:\n" +
            "1. Event registration\n" +
            "2. Ticket payment\n" +
            "3. Location information\n"
        )
        responded = True
    elif message in SERVICES.keys():
        service = SERVICES[message]
        if service == "Event registration":
            resp.message("To register for the event, please send your name, email, and phone number separated by commas.")
        elif service == "Ticket payment":
            resp.message("To make a payment, please visit our website at example.com/payments.")
        elif service == "Location information":
            resp.message("The event will be held at  South Eastern Kenya University.")
        responded = True

    name = None
    email = None
    phone = None

    parts = message.split(',')
    if len(parts) == 3:
        name = parts[0]
        email = parts[1]
        phone = parts[2]

        try:
            conn = sqlite3.connect('/home/kennartechs/Desktop/event registration bot/data/registration.db')
            c = conn.cursor()

            c.execute("INSERT INTO users (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
            conn.commit()
            conn.close()

            if c.rowcount > 0:
                resp.message("Thank you for registering for the event!")
            else:
                resp.message("An error occurred while registering for the event. Please try again later.")
            responded = True
        except Exception as e:
            print(e)
            resp.message("An error occurred while registering for the event. Please try again later.")
            responded = True

    if not responded:
        resp.message(
            "Sorry, I didn't understand that. Please select a service by replying with the corresponding number:\n" +
            "1. Event registration\n" +
            "2. Ticket payment\n" +
            "3. Location information\n"
        )

    return str(resp)


@app.route('/bot', methods=['POST'])
def bot():
    body = request.form['Body']
    return handle_message(body)


if __name__ == '__main__':
    app.run()