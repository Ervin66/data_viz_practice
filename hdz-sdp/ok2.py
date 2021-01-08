import requests
import pandas as pd
import re
import json
from psaw import PushshiftAPI
import matplotlib.pyplot as plt
import seaborn as sns


class Fetch():
    """docstring for Fetch"""

    def __init__(self):
        self.query = "hdz"
        self.after = 371
        # self.url = f"https://api.pushshift.io/reddit/comment/search/?q={self.query}&subreddit=croatia&fields=body,author,created_utc&before=6d&after={self.after}&size=500"
        # self.json = requests.get(self.url).json()
        # # print(self.json["data"])
        # print(len(self.json["data"]))

    def loop_through(self, query):
        api = PushshiftAPI()
        gen = api.search_comments(q="HDZ",
                                  subreddit='croatia',
                                  filter=["author"],
                                  after="372d",
                                  before="7d")
        cache = []
        for c in gen:
            cache.append(c)
            if len(cache) > 20:
                break
        self.df = pd.DataFrame([comment.d_ for comment in gen])
        self.df.to_csv(f"{query}.csv")
        print(self.df)

    def count_and_sort(self, csv):
        self.df = pd.read_csv(csv)
        print(self.df)
        count_table = self.df.groupby(
            ["author"])["created"].count().reset_index()
        count_table.sort_values(
            "created", ascending=False)[:16].to_csv("freq_sorted" + csv)
        print(count_table.sort_values("created", ascending=False))
        # count_table.to_csv("count"+csv)

    def plot(self, freq_table):
        sns.set()
        self.df = pd.read_csv(freq_table, usecols=["author", "created"])
        print(self.df)
        # self.df = self.df.sort_values("created")
        plt.figure(figsize=(16,9))
        sns.barplot(y=self.df["author"],
                    x=self.df["created"],
                    palette='Reds_r',
                    edgecolor="black")
        plt.title("Top 15 korisnika koji su spomenuli 'sdp' u komentarima za 2020. godinu")
        plt.xlabel("Broj komentara")
        plt.ylabel("Korisnik")
        plt.show()


a = Fetch()

a.loop_through("HDZ")