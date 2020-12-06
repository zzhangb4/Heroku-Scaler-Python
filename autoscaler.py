import requests
import base64
import json

from apscheduler.schedulers.blocking import BlockingScheduler

from config import APP, KEY, PROCESS


#############
### tasks ###
#############

# Generate Base64 encoded API Key
BASEKEY = base64.b64encode(KEY)
# Create headers for API call
HEADERS = {
    "Accept": "application/vnd.heroku+json; version=3",
    "Authorization": BASEKEY
}


def scale(size):
    payload = {'quantity': size}
    json_payload = json.dumps(payload)
    url = "https://api.heroku.com/apps/" + APP + "/formation/" + PROCESS
    try:
        result = requests.patch(url, headers=HEADERS, data=json_payload)
    except:
        return None
    if result.status_code == 200:
        return "Success!"
    else:
        return "Failure"


def get_current_dyno_quantity():
    url = "https://api.heroku.com/apps/" + APP + "/formation"
    try:
        result = requests.get(url, headers=HEADERS)
        for formation in json.loads(result.text):
            current_quantity = formation["quantity"]
            return current_quantity
    except:
        return None


#################
### scheduler ###
#################

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def job():
    print("This test is run every minute.")


@sched.scheduled_job('cron', hour=7)
def scale_out_to_three():
    print("Restarting...")
    scale(1)


@sched.scheduled_job('cron', hour=22)
def scale_in_to_two():
    print("Restarting...")
    scale(1)


@sched.scheduled_job('cron', hour=3)
def scale_in_to_one():
    print("Restarting...")
    scale(1)

sched.start()
