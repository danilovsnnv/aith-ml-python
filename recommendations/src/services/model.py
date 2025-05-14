from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, List, Sequence, Tuple

import polars as pl
from gensim.models import Word2Vec, KeyedVectors


def load_item2vec(checkpoint_dir: str | Path = "models") -> Word2Vec:
    checkpoint_dir = Path(checkpoint_dir)

    model_path = checkpoint_dir / "item2vec.model"
    if model_path.exists():
        return Word2Vec.load(model_path)

    vec_path = checkpoint_dir / "item2vec.vec"
    if vec_path.exists():
        kv = KeyedVectors.load_word2vec_format(vec_path, binary=False)

        class _Wrapper:
            wv = kv

        return _Wrapper()

    raise FileNotFoundError(
        f"Neither '{model_path}' nor '{vec_path}' found – did you pass the right folder?"
    )


def similar_items(
    model: Word2Vec,
    item_id: Any,
    topn: int = 10,
) -> List[Tuple[str, float]]:
    key = str(item_id)
    if key not in model.wv:
        return []
    return model.wv.most_similar(key, topn=topn)


def recommend_for_items(
    model: Word2Vec,
    items: Sequence[Any],
    *,
    topn: int = 10,
    exclude_input: bool = True,
) -> List[Tuple[str, float]]:
    tokens = [str(i) for i in items if str(i) in model.wv]
    if not tokens:
        return []

    user_vec = sum(model.wv[t] for t in tokens) / len(tokens)
    sims = model.wv.similar_by_vector(user_vec, topn=topn + len(tokens))

    if exclude_input:
        sims = [(itm, score) for itm, score in sims if itm not in tokens]

    return sims[:topn]


def recommend_next(
    model: Word2Vec,
    interactions: pl.DataFrame,
    user_id: Any,
    *,
    k_recent: int = 5,
    topn: int = 10,
) -> List[Tuple[str, float]]:
    recent_items = (
        interactions.filter(pl.col("user_id") == user_id)
        .sort("timestamp")
        .select("item_id")
        .tail(k_recent)
        .to_series()
        .to_list()
    )
    return recommend_for_items(model, recent_items, topn=topn)
