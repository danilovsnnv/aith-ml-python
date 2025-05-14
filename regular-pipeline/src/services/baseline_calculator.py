import asyncio
import os
import polars as pl

async def calculate_top_recommendations():
    """
    Baseline calculator, calculates most rated items based on interactions history.
    """
    while True:
        if os.path.exists('../data/interactions.csv'):
            print('calculating top recommendations')
            interactions = pl.read_csv('../data/interactions.csv')
            top_items = (
                interactions
                .sort('timestamp')
                .unique(['user_id', 'item_id', 'action'], keep='last')
                .filter(pl.col('action') == 'like')
                .groupby('item_id')
                .count()
                .sort('count', descending=True)
                .head(100)
            )['item_id'].to_list()

            top_items = [str(item_id) for item_id in top_items]

            # redis_connection.json().set('top_items', '.', top_items)
        await asyncio.sleep(10)