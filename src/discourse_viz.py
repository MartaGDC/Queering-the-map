import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_context('poster')
sns.set(rc={'figure.figsize': (16., 9.)})
sns.set_style('whitegrid')
from wordcloud import WordCloud
from nltk.corpus import stopwords


df = pd.read_csv("data/total_df.csv", index_col="Unnamed: 0")
top_countries = pd.DataFrame(df["country_code"].value_counts().head(10))

def graph_web_use():
    '''
    Web use by top countries use.
    '''
    plt.figure()
    plt.figure(figsize=(7, 4))
    sns.barplot(data = top_countries, x = "country_code", y = "count")
    plt.title("Countries commenting more in the web")
    plt.xlabel("Country codes" )
    plt.ylabel("")
    plt.savefig('images/Top_countries_use.png')

def graph_language():
    '''English vs the rest'''
    plt.figure()
    num_en = df.language[df["language"]=="en"].value_counts()["en"]
    num_not_en = df.shape[0]-num_en
    data = [num_not_en, num_en]
    labels = [ 'Other', 'English']
    plt.figure(figsize=(6, 4))
    colors = sns.color_palette("Paired")[2:5]
    plt.pie(data, labels = labels, colors=colors, autopct='%.0f%%')
    plt.title("Languages used in the comments")
    plt.savefig("images/Lang_english.png")

def graphs_sentiment():
    '''Sentiment, sentiment without neutral sentiment, sentiment without neutral sentiment and outliers'''
    plt.figure()
    plt.figure(figsize=(6, 4))
    sns.histplot(df["sentiment"])
    plt.title("Distribution of sentiment")
    plt.xlabel("Sentiment")
    plt.ylabel("")
    plt.savefig("images/Sentiment.png")

    plt.figure()
    plt.figure(figsize=(6, 4))
    sns.histplot(df["sentiment"][df["sentiment"] !=0])
    plt.title("Distribution of sentiment\n(without neutral sentiment)")
    plt.xlabel("Sentiment")
    plt.ylabel("")
    plt.savefig("images/Sentiment_no_neutral.png")

    plt.figure()
    Q1_sens = df["sentiment"][df["sentiment"]!=0].quantile(0.25)
    Q3_sens = df["sentiment"][df["sentiment"]!=0].quantile(0.75)
    IQR = Q3_sens - Q1_sens
    outlier_inf_sens = Q1_sens - 1.5 * IQR
    plt.figure(figsize=(6, 4))
    sns.histplot(df["sentiment"][(df["sentiment"] !=0) & (df["sentiment"]>outlier_inf_sens)])
    plt.title("Distribution of sentiment\n(without neutral sentiment and outliers)")
    plt.xlabel("Sentiment")
    plt.ylabel("")
    plt.savefig("images/Sentiment_no_neutral_no_outliers.png")

def graphs_characters():
    '''Characters, characters without outliers'''
    plt.figure()
    plt.figure(figsize=(10, 4))
    sns.histplot(df["characters"])
    plt.title("Length of the texts");
    plt.savefig('images/Characters.png')

    plt.figure()
    Q1_char = df["characters"].quantile(0.25)
    Q3_char = df["characters"].quantile(0.75)
    IQR = Q3_char - Q1_char
    outlier_sup_char = Q3_char + 1.5 * IQR
    plt.figure(figsize=(10, 4))
    sns.histplot(df["characters"][df["characters"]<=outlier_sup_char])
    plt.title("Length of the texts\n(without outliers)");
    plt.savefig('images/Characters_no_outliers.png')

def graphs_emotionality():
    '''Emotionality, emotionality without outliers'''
    plt.figure()
    plt.figure(figsize=(6, 4))
    sns.histplot(df["emotionality"])
    plt.title("Distribution of emotionality");
    plt.savefig('images/Emotionality.png')
    
    plt.figure()
    Q1_emo = df["emotionality"].quantile(0.25)
    Q3_emo = df["emotionality"].quantile(0.75)
    IQR = Q3_emo - Q1_emo
    outlier_sup_emo = Q3_emo + 1.5 * IQR
    plt.figure(figsize=(10, 4))
    sns.histplot(df["emotionality"][df["emotionality"]<=outlier_sup_emo])
    plt.title("Emotionality of the texts\n(without outliers)")
    plt.savefig('images/Emotionality_no_outliers.png')

def wordCloud_world():
    '''WordCloud for the world, language english'''
    lines = df["comment"][df["language"]=="en"]
    comments = " ".join(lines)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(comments)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    wordcloud.to_file('images/GlobalCloud.png')