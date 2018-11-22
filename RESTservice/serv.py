from flask import Flask, request, abort, jsonify
import json, pyspark, server_config as sc
from pyspark.mllib.fpm import FPGrowth
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
# Source: https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
from pprint import pprint
from pymongo import MongoClient

# CONNECTION TO MONGODB
MONGODB_URL = sc.get_mongo_url()
client = MongoClient(MONGODB_URL)
db = client['log8430'] # database name
'''
# Test entry to test the DB itself
receipt = {
    "items": [
        {
        "name": "Potato", "price": "$50.00"
        }
    ]
}
db.receipts.insert_one(receipt)
'''

# INITIALIZE FLASK
app = Flask(__name__)

# INITIALIZE SPARK
MONGODB_SPARK_URL = sc.get_mongo_spark_url()

spark = SparkSession \
            .builder \
            .appName("log8430-server") \
            .master("local") \
            .config("spark.mongodb.input.uri", MONGODB_SPARK_URL) \
            .config("spark.mongodb.output.uri", MONGODB_SPARK_URL) \
            .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.2.5") \
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

        # TODO: Test
        db.receipts.insert_one(receipt)

        return jsonify(receipt)


DB_FORMAT = "com.mongodb.spark.sql.DefaultSource"

# GET DATA
def _get_dataframe():
    # Source : https://docs.mongodb.com/spark-connector/master/python/read-from-mongodb/
    df = spark.read.format(DB_FORMAT) \
        .load()
    # df.printSchema() # Testing if Spark can read from MongoDB

    return df


# GET FREQUENT ITEMS ROUTE
@app.route('/receipt/frequent', methods=['GET'])
def get_frequent():
    output = {"frequency": []}

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