from flask import Flask, request, abort, jsonify
import json
import pyspark, sys
from pyspark.mllib.fpm import FPGrowth


# VERIFY SERVER ARGUMENTS
if not len(sys.argv) > 1:
    print("Missing Spark Cluster URL to connect to. (e.g. mesos://host:port, spark://host:port)")
    exit(-1)

# INITIALIZE FLASK AND SPARK
app = Flask(__name__)
spark = pyspark.sql.SparkSession.builder \
            .master(sys.argv[1]) \
            .appName("LOG8430 Server") \
            .getOrCreate()


# DEFAULT ROUTE
@app.route('/')
def get_hello():
    return "LOG8430 - Service REST"


# NEW RECEIPT ROUTE
#
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

        # TODO: write to DB (depends on DB used)

        return jsonify(receipt)


# TODO: format, table & keyspace need to be validated against actual database used
DB_FORMAT = "org.apache.spark.sql.cassandra"
DB_OPTIONS_TABLE = "receipts"
DB_OPTIONS_KEYSPACE = "items"

# GET DATA
def _get_dataframe():
    df = spark.read.format(DB_FORMAT) \
        .options(table=DB_OPTIONS_TABLE,keyspace=DB_OPTIONS_KEYSPACE) \
        .load()

    return df


# GET FREQUENT ITEMS ROUTE
@app.route('/receipt/frequent', methods=['GET'])
def get_frequent():
    output = {"frequency":[]}

    df = _get_dataframe()
    # TODO: Get from Spark
    # https://spark.apache.org/docs/latest/mllib-frequent-pattern-mining.html
    # transactions = df.map(lambda line: line.strip().split(' '))
    # model = FPGrowth.train(transactions, minSupport=0.2, numPartitions=10)
    # result = model.freqItemsets().collect()
    # for fi in result:
    #     output['frequency'].append(fi)

    return output   # may need to serialize the object


if __name__ == '__main__':
    app.run(debug=True)