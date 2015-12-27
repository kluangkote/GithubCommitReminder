from flask import Flask, request
import requests
import json
import twilio.twiml
from crontab import CronTab

app = Flask(__name__)

@app.route("/receiveSMS", methods=['POST'])
def recieveSMS():
    incoming = request.values.get('Body', None)

    # Using crontab to run daily job
    my_user_cron = CronTab(user=True)

    # Get new time
    if "SET TIME: " in incoming:
        time = incoming[10:]
        hour = time.rsplit(':', 1)[0]
        minute = incoming[-2:]
        if minute.startswith('0'):
            minute = minute[1:]
        my_user_cron.remove_all() # Remove previous job
        # Write new job. Make sure to put YOUR directory.
        job = my_user_cron.new(command='/your/pathway/here/send_sms.py')
        job.setall(minute + " " + hour + " * * *") #Set new time for job
        my_user_cron.write()
        resp = twilio.twiml.Response()
        resp.message("New time set to " + time)
        return str(resp)

    # Turn off reminders    
    elif incoming == "TURN OFF":
        my_user_cron.remove_all()
        my_user_cron.write()
        resp = twilio.twiml.Response()
        resp.message("Reminders turned off")
        return str(resp)

    # Turn on reminders    
    elif incoming == "TURN ON":
        my_user_cron.remove_all() # Remove any previous jobs
        # Write new job. Make sure to put YOUR directory.
        job = my_user_cron.new(command='/your/pathway/here/send_sms.py')
        job.setall('0 22 * * *') # Set time back to 10:00 PM
        my_user_cron.write()
        resp = twilio.twiml.Response()
        resp.message("Reminders turned on")
        return str(resp)

    # Give instructions to user    
    elif incoming == "START":
        resp = twilio.twiml.Response()
        resp.message("Welcome to your personal Github commit reminder.\n\nTo set your reminder time, text \"SET TIME: <hour>:<minute>\". (Note: time must be in military time)\n\nTo turn reminders off, text \"TURN OFF\".\n\nTo turn reminders back on, text \"TURN ON\" (Note: reminder time will be set back to default of 10:00 PM)")
        return str(resp)

    # Error message    
    else:
        resp = twilio.twiml.Response()
        resp.message("Invalid request")
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)