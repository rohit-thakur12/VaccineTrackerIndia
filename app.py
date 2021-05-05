import requests
import json
from datetime import datetime
from twilio.rest import Client

# Setting up logging
import logging
logging.basicConfig(level=logging.INFO, filename="vaccine.log", format='%(asctime)s - %(message)s')

# Load date
date = datetime.today().strftime('%d-%m-%Y')

# Load the config file
with open("config.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Setting up twilio
accountSid = data['twilio-sid']
authToken = data['twilio-auth']
client = Client(accountSid, authToken)
myTwilioNumber = data['twilio-number'] 
destCellPhone = data['myNumber']

# Setting up everything
def main():
    for pincode in data['pincode']:
        _URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}"
        response = requests.get(_URL)
        scrape = response.json()
        for i in scrape['centers']:
            sess = i['sessions']
            for sessions in sess:
                if sessions['available_capacity'] > 0 and sessions['min_age_limit'] == data['age']:
                    messageBody = f"Vaccine available at {i['name']} -  {i['address']} - {i['pincode']} on {sessions['date']} and the variant is {sessions['vaccine']}"
                    client.api.account.messages.create(to= destCellPhone, from_=myTwilioNumber, body=messageBody) 
                else:
                    logging.info(f"Vaccine not available at {i['name']} - {i['pincode']}")

if __name__ == "__main__":
    main()

