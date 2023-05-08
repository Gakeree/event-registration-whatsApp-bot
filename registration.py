from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
import urllib
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
            # Add ticket prices to choose from
            resp.message("Please select a ticket price from the following options:\n" +
                         "1. VIP (KES 5,000)\n" +
                         "2. Regular (KES 2,000)\n" +
                         "3. Student (KES 1,000)\n")


                         #location information
        elif service == "Location information":
           event_location = "South Eastern Kenya University"
           event_location_url = f"https://goo.gl/maps/hQ72SG4vHmjgkbZT7?coh=178573&entry=tt/?api=1&query={urllib.parse.quote(event_location)}"
           resp.message(f"The event will be held at {event_location}. Here is the Google Maps link: {event_location_url}")
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