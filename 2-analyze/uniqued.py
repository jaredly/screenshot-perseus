
def unique_ish_items(items):
  res = []
  rep = {}
  found = set()
  for item in items:
    tpl = re.sub(r'[\d\.]+', '_num_', json.loads(item['item_data'])['question']['content'])
    tpl = re.sub(r'\s+', '_space_', tpl)
    if tpl not in found:
      found.add(tpl)
      rep[tpl] = item
      item['represents'] = 1
      res.append(item)
    else:
      rep[tpl]['represents'] += 1
  print len(items), len(res)
  return res

sample = []
for count, excount, format in by_size[:10]:
  uniq = unique_ish_items(mapping[format])
  nex = num_exercises(mapping[format])
  print nex
  sample.append({
      'readable': nice_format(format),
      'count': count,
      'excount': nex,
      'items': [uniq[0], uniq[-1], uniq[len(uniq) // 2], uniq[len(uniq) // 4], uniq[len(uniq) * 3 // 4]],
    })

json.dump(sample, open('./2-analyze/wtypes/sample-top-20-percent.json', 'w'))


for i in range(5):
  json.dump(unique_ish_items(mapping[by_size[i][1]]), open('./2-analyze/wtypes/top-{}.json'.format(i), 'w'))

for i in range(5, 10):
  json.dump(unique_ish_items(mapping[by_size[i][1]]), open('./2-analyze/wtypes/top-{}.json'.format(i), 'w'))

# json.dump(unique_ish_items(mapping[by_size[0][1]]), open('./2-analyze/wtypes/math-expression.json', 'w'))

# json.dump(unique_ish_items(mapping[by_size[1][1]]), open('./2-analyze/wtypes/boldmathtext-expression.json', 'w'))

# json.dump(unique_ish_items(mapping[by_size[2][1]]), open('./2-analyze/wtypes/boldmathtext-radio.json', 'w'))
