import duckdb
import llama_cpp
from functools import lru_cache


class LiveSearch:

    def __init__(self, model_path) -> None:
        self.model = llama_cpp.Llama(model_path=model_path,
                                     embedding=True,
                                     verbose=False)

        self.con = duckdb.connect('../Resources/vectors.db', read_only=True)
        self.model
        self.map_dict = {
            i: item
            for i, item in enumerate([
                'emoji',
                'label',
                'version',
                'text',
            ])
        }

    def get_emoji(self, text):
        arr = self.model.create_embedding(text)['data'][0]['embedding']

        results = self.con.sql(
            f"select  emoji, label, version, text from array_table a left join emoji_df e on a.id = e.idx where label = base_emoji order by array_cosine_similarity(arr,{arr}::DOUBLE[384]) desc limit 20;"
        ).fetchall()

        results = [{
            self.map_dict[i]: res[i]
            for i in range(4)
        } for res in results]
        return results
