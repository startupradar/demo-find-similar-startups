import json
import logging
from hashlib import md5
from pathlib import Path

import click
import openai
import pandas as pd
from minimalkv.fs import FilesystemStore
from sklearn.metrics.pairwise import cosine_similarity
from startupradar.transformers.core import DomainTextTransformer
from startupradar.transformers.util.api import StartupRadarAPI, MinimalKeyValueCache
from startupradar.transformers.util.input import DomainInputCleaner

import config


def read_domains_from_file(path):
    with Path(path).open() as fp:
        return [line.strip() for line in fp.readlines()]


class OpenAiEmbedder:
    # same as within get_embedding of openai package
    ENGINE_DEFAULT = "text-similarity-davinci-001"

    def __init__(self, api_key, engine=ENGINE_DEFAULT):
        # set api key
        openai.api_key = api_key

        self.engine = engine
        self.store = FilesystemStore(".openai")

    def get_embedding(self, text: str):
        md5_hex = md5(text.encode()).hexdigest()
        key = f"{self.engine}_{md5_hex}"

        try:
            logging.info(f"cache hit, returning cached embedding ({key=})")
            cache_bytes = self.store.get(key)
            cache_str = cache_bytes.decode()
            embedding = json.loads(cache_str)
        except KeyError:
            logging.info(f"cache miss, requesting api ({key=})")
            embedding = self.request_embedding(text)
            cache_str = json.dumps(embedding)
            cache_bytes = cache_str.encode()
            self.store.put(key, cache_bytes)
        return embedding

    def request_embedding(self, text):
        # replace newlines, which can negatively affect performance.
        text = text.replace("\n", " ")

        embedding = openai.Embedding.create(input=[text], engine=self.engine)
        return embedding["data"][0]["embedding"]


@click.group()
def cli():
    pass


@cli.command()
def run():
    # set up startupradar.co API wrapper with cache
    api_cache_store = FilesystemStore(".apicache")
    api_cache = MinimalKeyValueCache(api_cache_store)
    api = StartupRadarAPI(config.STARTUPRADAR_API_KEY, cache=api_cache)

    # set up embedder
    embedder = OpenAiEmbedder(config.OPENAI_API_KEY, engine=config.OPENAI_ENGINE)

    # read domains from input file and clean them
    dic = DomainInputCleaner(api)
    domains_raw = read_domains_from_file("domains.txt")
    domains = list(dic.get_unique(domains_raw))

    # use startupradar's transformer to get texts
    t = DomainTextTransformer(api)
    df_texts = t.transform(pd.Series(domains, index=domains))

    # filter short domains
    df_texts = df_texts[df_texts["text"].str.len() > 100]

    # make embeddings
    embeddings = df_texts["text"].apply(embedder.get_embedding).to_list()
    df_embeddings = pd.DataFrame(embeddings, index=df_texts.index)

    # create similarity matrix and retain domains as indexes
    df_similarity = pd.DataFrame(
        cosine_similarity(df_embeddings),
        columns=df_embeddings.index,
        index=df_embeddings.index,
    )
    df_similarity.to_csv("out/similarity_matrix.csv")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cli()
