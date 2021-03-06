import pymongo
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import streamlit.components.v1 as components

# -----------------------------------------------------------------------
#                       Setup de la page
# -----------------------------------------------------------------------

st.set_page_config(layout="wide")
st.title("Agrégateur d' information sur la Cryptommonaie")
st.markdown("""
## Application
""")

# -----------------------------------------------------------------------
#                       Barre d'information
# -----------------------------------------------------------------------

extend_bar = st.beta_expander("Information")
extend_bar.markdown("""
- **Description du projet** : Dans le cadre du cours de NoSQL, nous devons scrapper des données sur internet et les valoriser.
Nous avons choisi de récupérer des données en rapport avec la cryptomonnaie pour permettre une accessibilité et une facilité d'accès à la connaissance de la cryptomonnaie.
- **Développeurs** : Quentin Pierson et Toky Cedric Andriamahefa
- **Framework** : Streamlit, Python, Scrapy, 
- **Base de données** : MongoDB
- **Source** : Cryptonaute, GoogleNews, CoinMarketCap
""")


# -----------------------------------------------------------------------
# |                      Connexion BDD Crypto                           |
# -----------------------------------------------------------------------

@st.cache(hash_funcs={pymongo.MongoClient: id})
def get_client():
    return pymongo.MongoClient("mongodb://127.0.0.1")


clientCrypto = get_client()
dbCrypto = clientCrypto["crypto"]

st.sidebar.subheader("Options:")
colle_name = st.sidebar.selectbox("Select collection: ", dbCrypto.list_collection_names())


def connexion(db_name, col_name):
    conn = get_client()
    return conn[db_name][col_name]


articles = connexion("crypto", colle_name)


def load_data():
    df2 = pd.DataFrame(list(articles.find()))
    df2.pop("_id")
    return df2


x = colle_name
if colle_name == "collectionReddit":
    x = "Reddit"
else:
    x = "Twitter"

dataArticle = load_data()


# -----------------------------------------------------------------------
#                       Connexion EMBED TWEET
# -----------------------------------------------------------------------

def afficherTweet(author, url, texte, likes, retweet, date, polarity, subjectivity):
    middle_page.markdown(f"""
    > {texte}
    >
    > - Author : {author} [{date}]({url})
    > - Likes : {likes} - Retweet {retweet}
    > - Polartié : {polarity} - Subjectivité {subjectivity} 
    >
    """)


def afficherReddit(title, Author, score, url, texte, date):
    middle_page.markdown(f"""
    > ### {title} 
    >
    > ***
    > {texte}
    > 
    > - Author : {Author} [{date}]({url}) (cliquer sur la date pour voir le tweet) 
    > - Score : {score}
    """)


slider = st.sidebar.slider("Choisissez le nombre de poste à afficher", 1, 20, 1)
# -----------------------------------------------------------------------
# |                      Connexion BDD Articles                           |
# -----------------------------------------------------------------------

client = get_client()
db = client["articles"]

# Crétation des trois colonnes
side_part = st.sidebar

# Creation des colonnes 2 et 3 tels que la colone 2 est 2 fois plus grande que la colonne 3
middle_page, right_side = st.beta_columns((2, 1))

# Partie coinMarket
dbmarket = "coinMarket"


# Chargement des données de coinmarket cap avec reformatage des données
def load_market_data():
    df_markets = pd.DataFrame(list(db[dbmarket].find()))
    df_markets.pop("_id")

    for i in range(len(df_markets['percent_change_24h'])):
        df_markets['percent_change_24h'][i] = float(df_markets['percent_change_24h'][i][0])
        if df_markets['type_24'][i][0] == "icon-Caret-down":
            df_markets['percent_change_24h'][i] = df_markets['percent_change_24h'][i] * (-1)

    for i in range(len(df_markets['percent_change_7d'])):
        df_markets['percent_change_7d'][i] = float(df_markets['percent_change_7d'][i][0])
        if df_markets['type_7'][i][0] == 'icon-Caret-down':
            df_markets['percent_change_7d'][i] = df_markets['percent_change_7d'][i] * (-1)

    df_markets.pop("type_7")
    df_markets.pop("type_24")

    df_markets.columns = ['Nom', 'Symbole', 'Prix ($)', 'Variation en 24h', 'Variation en 7j', 'Market Cap ($)',
                          'Volume en 24h ($)']

    df_markets['Nom'] = df_markets['Nom'].astype(str)
    df_markets['Symbole'] = df_markets['Symbole'].astype(str)

    for i in range(len(df_markets['Nom'])):
        df_markets['Nom'][i] = df_markets['Nom'][i][2:len(df_markets['Nom'][i]) - 2]

    for i in range(len(df_markets['Symbole'])):
        df_markets['Symbole'][i] = df_markets['Symbole'][i][2:len(df_markets['Symbole'][i]) - 2]

    for i in range(len(df_markets['Prix ($)'])):
        df_markets['Prix ($)'][i] = df_markets['Prix ($)'][i][0][1::].replace(',', '')

    for i in range(len(df_markets['Market Cap ($)'])):
        df_markets['Market Cap ($)'][i] = df_markets['Market Cap ($)'][i][0][1::].replace(",", "")

    for i in range(len(df_markets['Volume en 24h ($)'])):
        df_markets['Volume en 24h ($)'][i] = df_markets['Volume en 24h ($)'][i][0][1::].replace(",", "")

    df_markets['Prix ($)'] = df_markets['Prix ($)'].astype(float)
    df_markets['Variation en 24h'] = df_markets['Variation en 24h'].astype(float)
    df_markets['Variation en 7j'] = df_markets['Variation en 7j'].astype(float)
    df_markets['Market Cap ($)'] = df_markets['Market Cap ($)'].astype(float)
    df_markets['Volume en 24h ($)'] = df_markets['Volume en 24h ($)'].astype(float)

    return df_markets


df_market = load_market_data()

crypto_ordre = sorted(df_market['Symbole'])

# ** Partie de droite **
# partie 1 du side_part
side_part.header('Paramètres : ')
type_of_cryptocurrency = side_part.selectbox('Choisissez le type de cryptommonaie : ', crypto_ordre)
side_part.write("Vous avez choisis : " + type_of_cryptocurrency)

# partie 2 du side_part
# On load les datas depuis la collection séléctionnée
# coll_name = side_part.selectbox("Choisissez la collection: ", db.list_collection_names())


# def load_mongo_data():
#   df = pd.DataFrame(list(db[coll_name].find()))
#  df.pop("_id")

#   return df


# article = load_mongo_data()

# Partie 3
crypto_selected = side_part.multiselect('Cryptomonnaie ', crypto_ordre, )
c_selected = crypto_selected
if not crypto_selected:
    c_selected = ['BTC']

df_crypto_selected = df_market[(df_market['Symbole'].isin(c_selected))]

interval_pourcentage = side_part.selectbox('La période de la variation', ['7j', '24h'])
type_variation = {"7j": 'Variation en 7j', "24h": 'Variation en 24h'}
choix_variation = type_variation[interval_pourcentage]

# Partie 4
res_slider = side_part.slider("Choisissez le nombre d'articles à afficher", 1, 50, 1)


# Partie centrale
# 1
def getPrix(symbole):
    for i in range(len(df_market['Prix ($)'])):
        if df_market['Symbole'][i] == symbole:
            return df_market['Prix ($)'][i]


right_side.markdown("![Alt Text](https://media.giphy.com/media/9FQ89bO3TipLASwmRs/giphy.gif)")

middle_page.markdown(f"""
# Prix du {type_of_cryptocurrency}
""")
middle_page.markdown(f"""
# {getPrix(type_of_cryptocurrency)} $
""")

# 2
middle_page.markdown("""
### Le prix des Cryptos séléctionnées
""")
middle_page.write('Dimension : ' + str(df_crypto_selected.shape[0]) + 'ligne(s) et ' + str(
    df_crypto_selected.shape[1]) + 'colonne(s)')
middle_page.write(df_crypto_selected)

# 3
middle_page.markdown("""
### Tableau de la variation du prix
""")
df_variation = pd.concat(
    [df_crypto_selected.Symbole, df_crypto_selected['Variation en 24h'], df_crypto_selected['Variation en 7j']], axis=1)
df_variation = df_variation.set_index('Symbole')
middle_page.dataframe(df_variation)
df_variation['positif_variation_24'] = df_variation['Variation en 24h'] > 0
df_variation['positif_variation_7'] = df_variation['Variation en 7j'] > 0

# 4
middle_page.markdown("""
### Graph des prix
""")
df_price = pd.concat([df_crypto_selected.Symbole, df_crypto_selected['Prix ($)']], axis=1)
df_price = df_price.set_index('Symbole')

plt.figure(figsize=(15, 5))
plt.subplots_adjust(top=1, bottom=0)
df_price['Prix ($)'].plot(kind='barh', color='b')
middle_page.pyplot(plt)

# -----------------------------------------------------------------------
#                           Afficher data
# -----------------------------------------------------------------------
middle_page.markdown("---")
middle_page.title(f"Affichage des {x} ")

if colle_name == "collectionReddit":
    for i in range(slider):
        title = dataArticle['Title'][i]
        Author = dataArticle['Author'][i]
        text = dataArticle['Body'][i]
        score = dataArticle['Score'][i]
        date = dataArticle['timestamp'][i]
        url = dataArticle['Url'][i]
        afficherReddit(title, Author, score, url, text, date)
else:
    for i in range(slider):
        author = dataArticle['author'][i]
        text = dataArticle['tweets'][i]
        likes = dataArticle['likes'][i]
        retweet = dataArticle['retweet'][i]
        date = dataArticle['times'][i]
        polarity = dataArticle['Polarity'][i]
        subjectivity = dataArticle['Subjectivity'][i]
        url = dataArticle['url'][i]
        afficherTweet(author, url, text, likes, retweet, date, polarity, subjectivity)

# -----------------------------------------------------------------------
#                           Affichage des articles
# -----------------------------------------------------------------------
middle_page.markdown("---")
middle_page.title('Articles du jour')
google_collection_name = 'googleNews'


def load_google_article():
    df_gArticles = pd.DataFrame(list(db[google_collection_name].find()))
    df_gArticles.pop('_id')
    return df_gArticles


def afficherArticle(title, texte, media, full_articles):
    middle_page.markdown(f"""
        ### [{title}]({full_articles})
    """)
    middle_page.markdown(f"""       
         >-{texte}.. ***{media}***
    """)


df_Garticles = load_google_article()

for i in range(res_slider):
    titre = df_Garticles['title'][i]
    text = df_Garticles['texte'][i]
    med = df_Garticles['media'][i]
    full_ref = df_Garticles['full_article_ref'][i]
    afficherArticle(titre[0], text[0], med[0], full_ref)

# middle_page.dataframe(df_Garticles)

# *** Rightside ***
right_side.markdown("""
### Bar plot du % de variation du Prix
""")

if interval_pourcentage == '7j':
    right_side.markdown("""
    *7 derniers jours*
    """)
    plt.figure(figsize=(6, 6))
    plt.subplots_adjust(top=1, bottom=0)
    df_variation['Variation en 7j'].plot(kind='barh',
                                         color=df_variation.positif_variation_7.map({True: 'g', False: 'r'}))
    right_side.pyplot(plt)
else:
    right_side.markdown("""
    *dernière 24h*
    """)
    plt.figure(figsize=(6, 6))
    plt.subplots_adjust(top=1, bottom=0)
    df_variation['Variation en 24h'].plot(kind='barh',
                                          color=df_variation.positif_variation_24.map({True: 'g', False: 'r'}))
    right_side.pyplot(plt)
