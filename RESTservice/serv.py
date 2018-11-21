from flask import Flask, request, abort, jsonify
import json

app = Flask(__name__)

@app.route('/')
def get_hello():
    return "LOG8430 - Service REST"


# How to send to server
# Content-Type : application/json
# KEY : VALUE
# receipt : { "items": [ { "name": "Potato", "price": "$50.00" } ] }


@app.route('/receipt/new', methods=['POST'])
def post_receipt():
    if 'receipt' not in request.json and 'items' not in request.json['receipt']:
        abort(400)
    else:
        receipt = request.json['receipt']
        # TODO: Send to Apache Spark
        return jsonify(receipt)


@app.route('/receipt/frequent', methods=['GET'])
def get_frequent():
    # TODO: Fetch from Apache Spark (Q2c)
    return "Okay"


if __name__ == '__main__':
    app.run(debug=True)