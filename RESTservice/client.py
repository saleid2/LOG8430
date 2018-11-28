import requests
import sys
import json


DONE_ADDING = "!s"                              # Flag to stop adding items to receipt and send request to server
QUIT = "!q"                                     # Flag to quit client code
new_receipt_route = "/receipt/new"              # Route to add new receipt
get_frequent_route = "/receipt/frequent"        # Route to get frequent items

server_host = "http://127.0.0.1:5000"           # Default host (when running serv.py directly in python)
new_receipt = True                              # Add new receipt or get frequent items


def new_receipt():
    print("To stop adding items to receipt and send to server, type \'" + DONE_ADDING + "\'")
    print("To quit without sending, type \'" + QUIT + "\'")

    items = []
    stop = False

    while not stop:
        item_name = input("Product name : ")

        if item_name == DONE_ADDING:
            stop = True
            break
        elif item_name == QUIT:
            quit(-1)

        while True:
            item_price = input("Product price (as double) : ")

            if item_price == DONE_ADDING:
                stop = True
                break
            elif item_price == QUIT:
                quit(-1)
            else:
                try:
                    item_price = float(item_price)
                    break
                except ValueError:
                    # Entered value isn't a float. Try again
                    continue

        item = {"name": item_name, "price": item_price}

        items.append(item)

        print("Added ", item)

    if len(items) < 0:
        print("There is nothing to be sent")
        exit(0)

    print()
    print("The following receipt will be sent to the server")
    print(items)

    params = {'receipt': {"items": items}}
    headers = {"content-type": "application/json"}
    r = requests.post(server_host + new_receipt_route, json=params, headers=headers)


def get_frequent():
    r = requests.get(server_host + get_frequent_route)
    results = r.json()
    sorted_results = sorted(results, key=lambda x: x['freq'], reverse=True)
    print(json.dumps(sorted_results, indent=4))


#
# python client.py http://HOSTNAME:PORT X
# if x = 0   : new receipt
# if x != 0  : get frequent item

if len(sys.argv) > 1:
    server_host = "http://" + sys.argv[1]

if len(sys.argv) > 2:
    if sys.argv[2] != 0:
        new_receipt = False

print("Server is found at " + server_host)

if new_receipt:
    new_receipt()
else:
    get_frequent()