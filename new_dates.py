import datetime
import json
import time

import requests
import schedule


def send_email(date):
    requests.post('webhook_link', data='{"text":"New date available: %s"}' % date, headers={"Content-type": "application/json"})
def check_date():
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://fp.trafikverket.se/Boka/",
        "Origin": "https://fp.trafikverket.se",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Content-Type": "application/json"
    }
    currentDT = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    data = {
        "bookingSession": {
            "bookingModeId": 0,
            "examinationTypeId": 0,
            "excludeExaminationCategories": [],
            "ignoreBookingHindrance": False,
            "ignoreDebt": False,
            "licenceId": 4,
            "paymentIsActive": False,
            "rescheduleTypeId": 0,
            "socialSecurityNumber": "19880509-4490"},
        "occasionBundleQuery": {
            "startDate": currentDT,
            "locationId": 1000329,
            "languageId": 13,
            "vehicleTypeId": 1,
            "tachographTypeId": 1,
            "occasionChoiceId": 1,
            "examinationTypeId": 2
        }
    }
    json_data = json.dumps(data);
    r = requests.post("https://fp.trafikverket.se/Boka/occasion-bundles", data=json_data, headers=headers)
    dates = []
    if r.status_code == requests.codes.ok:
        js = json.loads(r.content)

        if js and js['data']:
            for dataVal in js['data']['bundles']:
                if dataVal and dataVal['occasions']:
                    for occasionsVal in dataVal['occasions']:
                        if occasionsVal and occasionsVal['date']:
                            dates.append(occasionsVal['date'])
    else:
        print
        'An error occurred on server side. %s' % r.status_code
    dates.sort()
    # print('Earliest available date is: %s' % dates[0])
    if len(dates) > 0:
        if '2021-06-30' >= dates[0] > '2021-06-16':
            print('NEW DATE AVAILABLE! %s' % dates[0])
            send_email(dates[0])
        else:
            print('No new date is available')
    else:
        print('No dates available? Something must be wrong')


schedule.every(20).seconds.do(check_date)

while True:
    schedule.run_pending()
    time.sleep(1)
