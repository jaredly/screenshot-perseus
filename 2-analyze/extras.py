
bytitle = defaultdict(set)
for k, v in ttree_raw.items():
  bytitle[v['title']].add(k)

child_titles = {}

for k, v in ttree_raw.items():
  child_titles[k] = [ttree_raw.get(m['_ndb_key']['pairs'][0][1], {'title': 'not found'})['title'] for m in v['child_data'] if m['_ndb_key']['pairs'][0][0] == 'Topic']

child_titles[main_math]

parentless = ([(k, v['title']) for k, v in ttree_raw.items() if k not in parents])

def analysis():
  sum([n for n, _ in by_size[:20]]) / float(len(math_items))
  num=100;
  by=1;
  bar(range(num), [sum(k for k, __ in by_size[:i * by])/float(len(math_items))
    for i in range(1, 1 + num)]);

