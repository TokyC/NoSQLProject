from functools import wraps

import streamlit as st
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from nltk.stem.snowball import SnowballStemmer

st.set_option('deprecation.showPyplotGlobalUse', False)

# Setup de la page
st.set_page_config(layout="wide")
st.title("Agrégateur d' information sur la Cryptommonaie")
st.markdown("""
## Application
""")

# La bare d'information
extend_bar = st.beta_expander("Information")
extend_bar.markdown("""
- **Description du projet** : Dans le cadre du cours de NoSQL, nous devons scrapper des données sur internet et les valoriser.
Nous avons choisit de récupérer des données en rapport avec la cryptomonnaie pour permettre une accessibilité et une facilité d'accès à la connaissance de la cryptomonnaie.
- **Développeurs** : Quentin Pierson et Toky Cedric Andriamahefa
- **Framework** : Streamlit, Python, Scrapy, 
- **Base de données** : MongoDB
- **Source** : Cryptonaute, GoogleNews, CoinMarketCap
""")


# -------------------------
# Connexion
# -------------------------

@st.cache(hash_funcs={pymongo.MongoClient: id})
def get_client():
    return pymongo.MongoClient("mongodb://127.0.0.1/crypto")


client = get_client()
db = client["crypto"]

st.sidebar.subheader("MongoDB:")
coll_name = st.sidebar.selectbox("Select collection: ", db.list_collection_names())


def connexion(db_name, col_name):
    conn = get_client()
    return conn[db_name][col_name]


articles = connexion("crypto", coll_name)


def load_data():
    df2 = pd.DataFrame(list(articles.find()))
    return df2


st.markdown(" ## Load Database ")
dataArticle = load_data()
st.write(dataArticle)


@st.cache(allow_output_mutation=True)
def load_mongo_data_tweet():
    df = pd.DataFrame(list(db.collectionTweet.find()))
    return df


dataTweet = load_mongo_data_tweet()
# st.write("Showing data for Twitter: ")
# st.write(dataTweet)


fig, ax = plt.subplots()
dataTweet = dataTweet[:20]
ax = sns.barplot(x=dataTweet.likes, y=dataTweet.author, orient='h')
# ax = dataTweet[:10].plot.barh(x='author', y='likes')
plt.plot()
plt.show()
st.pyplot()

st.markdown("## Display of the most present words  ")
df = dataTweet["tweets"]

list_of_all_sentences = [sentence for sentence in df]

lines = []
for sentence in list_of_all_sentences:
    words = sentence.split()
    for w in words:
        lines.append(w)

# Removing Punctuation
lines = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in lines]
lines2 = []
listWordBanned = ["the", "to", "for", "on", "just", 'how', "is", "a", "you", "Am", "Im", "I", "i", "and", "that", "of",
                  "in", "this", "it", "be", "not", "have", "my", "we", "beautiful", "what", "no", "as", "host", "me",
                  "with", "like", "your", "at", "do", "if", "too", "can", "know", "people", "about", "RT", "most",
                  "are"]
for word in lines:
    if word != '' and word not in listWordBanned:
        lines2.append(word)

# This is stemming the words to their root
# The Snowball Stemmer requires that you pass a language parameter
s_stemmer = SnowballStemmer(language='english')
stem = []
for word in lines2:
    stem.append(s_stemmer.stem(word))

df = pd.DataFrame(stem)
df = df[0].value_counts()

df = df[:15]
plt.figure(figsize=(10, 5))
sns.barplot(df.values, df.index, alpha=0.8)
plt.title('Top Words Overall')
plt.ylabel('Word from Tweet', fontsize=12)
plt.xlabel('Count of Words', fontsize=12)
plt.show()
st.pyplot()

# Display query
# -------------------------

# For print all collection
for coll in db.list_collection_names():
    st.write(coll)

testBddTweet = [st.write("Test Tweet : ", test, "\n") for test in db.collectionTweet.find({"author": "Jesse"})]

testBddReddit = [st.write("Test reddit :", test2, "\n") for test2 in db.collectionReddit.find({"Author": "ibelite"})]

# st.write(db.collectionTweet.find()[100])
