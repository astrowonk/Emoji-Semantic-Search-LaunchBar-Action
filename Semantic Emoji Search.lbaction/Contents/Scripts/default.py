#!/usr/local/opt/miniforge3/bin/python

import json
from EmojiFinder import EmojiFinderSql
try:
    from ducklive import LiveSearch
    use_duck = True
except ImportError:
    use_duck = False
from config import gender_priority, skin_tone_priority

items = []
# Note: The first argument is the script's path

e = EmojiFinderSql()
if use_duck:
    l = LiveSearch(model_path='../Resources/minilm-v6.gguf')


def make_entry(item, skin_tone, gender):
    if not skin_tone:
        skin_tone = ''
    if not gender:
        gender = ''
    # final_item = {
    #     'icon': item[map_dict['emoji']],
    #     'title': item[map_dict['text']],
    #     'subtitle': item[map_dict['label']],
    #     'action': 'copy_emoji.py',
    #     'actionArgument': item[map_dict['emoji']],
    #     'actionReturnsItems': False
    # }
    additional_emojis = e.sql_add_variants(item['label'])
    #  print(additional_emojis)

    priority_result = []
    gender_result = []
    if skin_tone:
        priority_result = [x for x in additional_emojis if skin_tone in x]
    if gender:
        gender_result = [
            x for x in priority_result or additional_emojis
            if x.startswith(':' + gender)
        ]
    if gender_result:
        priority_result = gender_result

    if priority_result:
        priority_result = priority_result[0]
        additional_emojis.remove(priority_result)
        target = priority_result
    else:
        target = item
    if isinstance(target, str):
        target = {
            'emoji': e.new_emoji_dict(target)['emoji'],
            'text': e.new_emoji_dict(target)['text'],
            'label': target
        }
    final_item = {
        'icon': target['emoji'],
        'title': item['text'],
        'subtitle': target['label'],
        'action': 'copy_emoji.py',
        'actionArgument': target['emoji'],
        'actionReturnsItems': False
    }
    if additional_emojis:
        children = [{
            'icon': e.new_emoji_dict(item)['emoji'],
            'title': e.new_emoji_dict(item)['text'],
            'subtitle': item,
            'action': 'copy_emoji.py',
            'actionArgument': e.new_emoji_dict(item)['emoji'],
            'actionReturnsItems': False
        } for item in additional_emojis]
        final_item.update({'children': children})
    return final_item


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('search', help='some help', nargs="+")
    args = parser.parse_args()

    search = ' '.join(args.search).strip()
    res = e.top_emojis(search)
    if not res and use_duck:
        res = l.get_emoji(search)

    final_res = []
    for item in res:

        final_res.append(
            make_entry(item,
                       skin_tone=skin_tone_priority,
                       gender=gender_priority))

    print(json.dumps(final_res, indent=4))
