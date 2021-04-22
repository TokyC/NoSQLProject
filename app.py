import streamlit as st
from pymongo import MongoClient
from elasticsearch import Elasticsearch
import json


st.title("Crypto-currency")
st.write("# My first APP \n"
         "Hello world"
         "")


@st.cache(hash_funcs={MongoClient: id})
def get_client():
    return MongoClient("mongodb://127.0.0.1/admin")


# -------------------------
# Connexion
#-------------------------

client = get_client()
db = client["crypto"]
collection = db.startup_log

es = Elasticsearch(hosts=["localhost"])
st.write(es.ping())

# index access/creation
if not es.indices.exists(index="words"):
    es.indices.create(index="words")

# -------------------------
# Display query
# -------------------------

#For print all collection
for coll in db.list_collection_names():
    st.write(coll)

testBddTweet = [st.write("Test Tweet 1: ",test, "\n") for test in db.collectionTweet.find({"author": "TIME"})]

testBddReddit =  [st.write("Test reddit :",test2, "\n") for test2 in db.collectionReddit.find({"Author": "ibelite"})]

search_param = {
    "query": {
        "terms": {
            "_id": [ 1234, 42 ] # find Ids '1234' and '42'
        }
    }
}

response = es.search(index="some_index", body=search_param)
st.write(response)
