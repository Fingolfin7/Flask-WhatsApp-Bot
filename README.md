# WhatsApp Chatbot

This chatbot is built using Flask and Twilio and has several commands to help you find information quickly.

## Commands

- `#quote`: Search for a quote
- `#poem`: Search for a poem title
- `#wiki`: Get a quick Wikipedia summary
- `#fact`: Get a random fact

## Installation

To install the required dependencies for this project, navigate to the project's root directory and run the following command:


    pip install -r requirements.txt


## Usage
Run the app.py file and add your server's IP address as the forwarding address in the
Twilio Whatsapp Sandbox Settings of your account.

Make sure to add the '/sms' route to the end of your url/IP address.

To use the chatbot, simply send one of the commands to the bot's WhatsApp number. The bot will respond with the requested information.

## Built With

- Flask: A micro web framework written in Python
- Twilio: A cloud communications platform for building SMS, Voice & Messaging applications

## License

This project is licensed under the MIT License.