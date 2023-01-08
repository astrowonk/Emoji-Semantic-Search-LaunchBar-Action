#!/usr/bin/env python3
# #
# LaunchBar Action Script
#
import argparse
import json
from EmojiFinder import EmojiFinderSql

items = []

parser = argparse.ArgumentParser()
parser.add_argument('search')
# Note: The first argument is the script's path

args = parser.parse_args()

e = EmojiFinderSql()

res = e.top_emojis(args.search)
map_dict = {
    item: i
    for i, item in enumerate(
        ['emoji', 'rank_of_search', 'label', 'text', 'version'])
}

final_res = []
for item in res:
    final_item = {
        'icon': item[map_dict['emoji']],
        'title': item[map_dict['text']],
        'subtitle': item[map_dict['label']],
        'action': 'copy.py',
        'actionArgument': item[map_dict['emoji']],
        'actionReturnsItems': False
    }

    variants = e.add_variants(final_item['subtitle'])
    if variants:
        children = [{
            'icon': e.emoji_dict[item]['emoji'],
            'title': e.emoji_dict[item]['text'],
            'subtitle': item,
            'action': 'copy.py',
            'actionArgument': e.emoji_dict[item]['emoji'],
            'actionReturnsItems': False
        } for item in variants]
        final_item.update({'children': children})

    final_res.append(final_item)

print(json.dumps(final_res, indent=4))
