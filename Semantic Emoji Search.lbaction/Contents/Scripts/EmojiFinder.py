import sqlite3
#import emoji

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
        self.all_labels = self.run_sql_to_list(
            'select distinct label from emoji;')
        self.base_emoji_map = self.make_variant_map()
        self.emoji_dict = {
            label: {
                'emoji': emoji,
                'text': text
            }
            for label, emoji, text in self.con.execute(
                "select label,emoji,text from emoji;").fetchall()
        }

    def run_sql_to_list(self, sql):
        return flatten_list(self.con.execute(sql).fetchall())

    def add_variants(self, base_label):
        #print(base_label)
        base_search = base_label[1:-1]
        if base_search in SKIN_TONE_SUFFIXES:
            return []
        for prefix in ['person_', 'man_', 'woman_']:
            if base_search.startswith(prefix):
                base_search = base_search.replace(prefix, '')
                # print(f'new base {base_search}')
                break
        variants = [f":{base_search}_{x}:" for x in SKIN_TONE_SUFFIXES]
        #print(variants)
        man_variants = [':man_' + base[1:]
                        for base in variants] + [f':man_{base_search}:']
        woman_variants = [':woman_' + base[1:]
                          for base in variants] + [f':woman_{base_search}:']
        person_variants = [':person_' + base[1:]
                           for base in variants] + [f':person_{base_search}:']
        return self.filter_list(variants) + self.filter_list(
            woman_variants) + self.filter_list(
                man_variants) + self.filter_list(person_variants)

    @property
    def con(self):
        return sqlite3.connect('../Resources/main.db')

    def make_variant_map(self):
        no_variants = self.run_sql_to_list(
            'select distinct word from lookup_emoji;')
        new_dict = {}
        for non_variant in no_variants:
            the_variants = self.add_variants(non_variant)
            new_dict.update({var: non_variant for var in the_variants})
        return new_dict

    def filter_list(self, list1):
        return sorted(list(set(list1).intersection(self.all_labels)))

    def top_emojis(self, search):
        search = search.strip().lower()
        results = self.con.execute(
            "select emoji,rank_of_search,label,text,version from combined where word = (?) and version <= 14.0 order by rank_of_search;",
            (search, )).fetchall()
        return results
