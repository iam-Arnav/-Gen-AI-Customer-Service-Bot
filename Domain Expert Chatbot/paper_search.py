import pandas as pd

df = pd.read_csv("knowledge/cs_arxiv.csv")


def search_papers(keyword, limit=10):

    keyword = keyword.lower()

    mask = (
        df["title"].str.lower().str.contains(keyword, na=False)
        |
        df["content"].str.lower().str.contains(keyword, na=False)
    )

    return df[mask].head(limit)