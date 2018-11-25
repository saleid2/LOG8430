from flask import Flask, request, abort, jsonify
import json, pyspark, re, server_config as sc
from pyspark.mllib.fpm import FPGrowth
from pyspark.sql import SparkSession
from pyspark.sql import functions as PysparkF
# Source: https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
from pprint import pprint
from pymongo import MongoClient

# Source: https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, 0)

# CONNECTION TO MONGODB
MONGODB_URL = sc.get_mongo_url()
client = MongoClient(MONGODB_URL)
db = client['log8430'] # database name
'''
# Test entry to test the DB itself
receipt = {
    "items": [
        {
        "name": "Potato", "price": 5.0
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
            .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.2.5") \
            .getOrCreate()

# DEFAULT ROUTE
@app.route('/')
def get_hello():
    pprint("HELLO WORLD")
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
        db.receipts.insert_one(receipt)
        return JSONEncoder().encode(receipt)


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
    df = _get_dataframe()
    # https://spark.apache.org/docs/latest/mllib-frequent-pattern-mining.html
    transactions = df.groupBy("_id") \
            .agg(PysparkF.collect_list("items.name").alias("product_name")) \
            .rdd \
            .flatMap(lambda x: x.product_name)
    transactions.collect()

    model = FPGrowth.train(transactions, minSupport=0.2, numPartitions=10)
    result = model.freqItemsets().collect()

    stripped_result = []

    for fi in result:
        words, freq = re.search(r'FreqItemset\(items=\[(.*)\], freq=(\d*)\)', "%s" % fi).groups()
        stripped_result.append({'words':words, 'freq': int(freq})

    # Sample code below works.

    '''
    sc = SparkContext.getOrCreate(spark.conf)
    data = sc.textFile("sample_fpgrowth.txt")
    transactions = data.map(lambda line: line.strip().split(' '))
    model = FPGrowth.train(transactions, minSupport=0.2, numPartitions=10)
    result = model.freqItemsets().collect()
    for fi in result:
        print(fi)
    '''

    return json.dump(stripped_result)   # TODO: Definitely needs to be tester


if __name__ == '__main__':
    app.run(debug=False)