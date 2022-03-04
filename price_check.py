import requests

prices = []

def check_price():
    r = requests.get(
        "https://www.vattenfall.se/api/contract-flow/newcustomer/prices?BusinessArea=Private&CallerId=AG.SE"
        "&Consumption=15000&FlowTypeId=1&GridArea=FSB&IsExistingCustomer=false&PriceDate=2022-03-03&ZipCode=60599")

    json = r.json()


    for product in json:
        if product['productName'] == "PrivateFixed1Years":
            buildPrices(product)

        if product['productName'] == "PrivateFixed3Years":
            buildPrices(product)

    print(" | ".join(prices))
    send_slack()


def buildPrices(product):
    for t in product['energySources']:
        if t['text'] == 'Fossilfri mix':
            prices.append(product['productName'] + ": " + t['totalElectricalPrice']['price'])

def send_slack():
    prices_list = " | ".join(prices)
    requests.post(webhook_link, data='{"text":"Todays prices: %s"}' % prices_list,
                  headers={"Content-type": "application/json"})

check_price()
