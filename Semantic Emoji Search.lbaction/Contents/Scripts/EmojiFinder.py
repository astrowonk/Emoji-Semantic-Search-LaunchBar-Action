import sqlite3

SKIN_TONE_SUFFIXES = [
    'medium-light_skin_tone',
    'light_skin_tone',
    'medium_skin_tone',
    'medium-dark_skin_tone',
    'dark_skin_tone',
]


def flatten_list(list_of_lists):
    return [y for x in list_of_lists for y in x]


class EmojiFinderSql:

    def __init__(self):
        #  print('Begin init of class')
        #self.con = sqlite3.connect(
        #    'main.db')  #change later, name should have model type in it

        #self.base_emoji_map = self.make_variant_map()

        self.map_dict = {
            i: item
            for i, item in enumerate(
                ['emoji', 'rank_of_search', 'label', 'text', 'version'])
        }

    def run_sql_to_list(self, sql, params=None):
        if params:
            return flatten_list(self.con.execute(sql, params).fetchall())
        else:
            return flatten_list(self.con.execute(sql).fetchall())

    @property
    def con(self):
        return sqlite3.connect('../Resources/all-mpnet-base-v2_main.db')

    def sql_add_variants(self, label):
        return self.run_sql_to_list(
            "select label from emoji_df where base_emoji = ? and base_emoji <> label",
            params=(label, ))

    def make_variant_map(self):
        no_variants = self.run_sql_to_list(
            'select distinct label from lookup;')
        new_dict = {}
        for non_variant in no_variants:
            the_variants = self.add_variants(non_variant)
            new_dict.update({var: non_variant for var in the_variants})
        return new_dict

    def filter_list(self, list1):
        return sorted(list(set(list1).intersection(self.all_labels)))

    def new_emoji_dict(self, label):
        # print(df.shape)
        # return df
        return dict(
            zip(['idx', 'emoji', 'label', 'version', 'text', 'base_emoji'],
                self.con.execute("Select * from emoji_df where label = ?;",
                                 (label, )).fetchone()))

    def top_emojis(self, search):
        search = search.strip().lower()
        results = self.con.execute(
            "select emoji,rank_of_search,label,text,version from combined_emoji where word = ? and version <= 14.0 and label = base_emoji order by rank_of_search;",
            (search, )).fetchall()

        results = [{
            self.map_dict[i]: res[i]
            for i in range(5)
        } for res in results]

        return results
