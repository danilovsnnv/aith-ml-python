from __future__ import annotations

import asyncio

import polars as pl
from gensim.models import Word2Vec
from pathlib import Path

class ModelTrainer:
    def __init__(self, filepath, update_time = 10):
        self.filepath = filepath
        self.update_time = update_time

    async def train_model(self):
        while True:
            await asyncio.sleep(self.update_time)
            df = pl.read_csv(self.filepath, has_header=True)
            self._train_item2vec(df)

    @staticmethod
    def _train_item2vec(
        df: pl.DataFrame,
        vector_size: int = 64,
        window: int = 5,
        min_count: int = 1,
        workers: int = 4,
        epochs: int = 10,
        checkpoint_dir: str | Path = '../data',
    ):
        if isinstance(checkpoint_dir, str):
            checkpoint_dir = Path(checkpoint_dir)

        liked = (
            df.filter(pl.col('actions') == 'like').sort('timestamp')
        )

        sequences = (
            liked
            .groupby('user_id')
            .agg(pl.col('item_id'))
            .get_column('item_id')
            .to_list()
        )

        sentences = [[str(it) for it in seq] for seq in sequences]

        model = Word2Vec(
            sentences=sentences,
            vector_size=vector_size,
            window=window,
            min_count=min_count,
            workers=workers,
            epochs=epochs,
            sg=1,
            negative=10,
        )

        checkpoint_dir = Path(checkpoint_dir)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        model.save(checkpoint_dir / 'item2vec.model')
        model.wv.save_word2vec_format(
            checkpoint_dir / 'item2vec.vec', binary=False
        )

        return model