import json
full = json.load(open('./assessment_items.json'))
small = []
for m in full:
    del m['tags']
    del m['created_by']
    del m['key']
    # m['item_data'] = json.loads(m['item_data'])
    small.append({
        'item_data': json.loads(m['item_data']),
        'name': m['name'],
        'content_id': m['content_id'],
    })
json.dump(small, open('./small_items.json', 'w'))
