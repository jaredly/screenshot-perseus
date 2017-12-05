# For Exporting

# Imports n stuff

# cd ~/khan/repos/exercises-mobile-preview/scripts/

import json
import re
from collections import defaultdict

from nice_names import nice_format

print 'loading assessment data'
data = json.load(open('../1-js-process/parsed-assessment-items.json'))
print 'loading top tree'
ttree_raw = json.load(open('../0-get-data/topics.json'))
print 'loading exercises'
exercises = json.load(open('../0-get-data/exercises.json'))
print 'done loading data'

# Gist: use `math_items` for all assessment items under world of math, and `segmented_items` to get other things. `ttree_raw[key]['title']` will get you the title of a topic

def flatten(m):
  res = []
  for l in m:
    res += list(l)
  return res

## ----- TOPIC TREE STUFF ----- ##

def get_parents(nodes):
  parents = defaultdict(set)
  for k, v in nodes.items():
    for child in v['child_data']:
      type, key = child['_ndb_key']['pairs'][0]
      parents[key].add(k)
  return parents

def get_toplevels(nodes, parents, root_id):
    return [(k, nodes[k]['title']) for k in parents
                 if parents[k] == set([root_id])
                  and not nodes[k]['hide']
                  and nodes[k]['listed']]

def get_topic_paths(id):
  for parent in parents.get(id, []):
    if parent == root_id:
      yield [parent]
    for path in get_topic_paths(parent):
      yield [parent] + path

def named_topic_path(path):
  return map((lambda id: ttree_raw[id]['title']), path)

# Setup

def crawl(segmented, base, tree, at):
  if at not in tree:
    print 'unknown topic', at
    return
  for child in tree[at]['child_data']:
    p = child['_ndb_key']['pairs']
    if len(p) != 1:
      print "WHAT", p
    if p[0][0] == 'Topic':
      if p[0][1] not in tree or not tree[p[0][1]]['listed'] or tree[p[0][1]]['hide']:
        continue
      crawl(segmented, base, tree, p[0][1])
    segmented[base][p[0][0]].add(p[0][1])

# --------- The functions (more general) ------------

text_group = ('em', 'strong', 'u', 'link') #, 'inlineCode')
text_math_like = ('text', 'number', 'math', 'longmath', 'reallylongmath', 'unescapedDollar')

def merge_text_and_math(items):
  res = [items[0]]
  off = 1
  if not res[0]:
    if len(items) < 2:
      return ()
    off = 2
    res = [items[1]]
  for item in items[off:]:
    if not item:continue
    if item == res[-1]:continue
    while isinstance(item, tuple) and item[0] in text_group and len(item) == 2:
      item = item[1]

    if item in text_math_like and res[-1] in text_math_like + ('text_and_math',):
      res[-1] = 'text' # _and_math'
      continue
    res.append(item)
  return tuple(res)

def children_sig(children, widgets):
  return merge_text_and_math(tuple(typesig(child, widgets, sized=False) for child in children))

widget_counts = defaultdict(int)

def typesig(item, widgets, sized=False):
  if not isinstance(item, dict):
    print 'badd', item
    return item
  if item['type'] in ('paragraph',) + text_group:
    return (item['type'],) + children_sig(item['content'], widgets)
  if item['type'] == 'columns':
    return ('columns', children_sig(item['col1'], widgets), children_sig(item['col2'], widgets))
  if item['type'] == 'widget':
    widget = widgets[item['id']]
    if item['widgetType'] == 'radio':
      graded = 'graded' if widget.get('graded', False) else 'ungraded'
      multi = 'multi' if widget['options'].get('multipleSelect', False) else 'single'
      contents = frozenset(children_sig(child['content'], widgets) for child in widget['options']['choices'] if 'content' in child)
      return ('widget', graded, 'radio', multi, contents)
    wtype = item['widgetType']
    widget_counts[wtype] += 1
    if wtype in ('input-number', 'numeric-input'):
      wtype = 'expression'
    return ('widget', 'graded' if widget.get('graded', False) else 'ungraded', wtype)
  if item['type'] == 'text':
    if not item['content'].strip():
      return None
    return 'text'
  return item['type']

def organize_by_structure(data):
  counts = defaultdict(int)
  mapping = defaultdict(list)
  for datom in data:
    sig = tuple(typesig(m, datom['parsed_item_data']['question'].get('widgets', {}))
        for m in datom['parsed_item_data']['question']['content'])
    counts[sig] += 1
    mapping[sig].append(datom)
  return counts, mapping

def unfreeze(what):
  if isinstance(what, (list, tuple, set, frozenset)):
    return map(unfreeze, what)
  if isinstance(what, dict):
    return {k: unfreeze(v) for k, v in what.items()}
  return what

def summary(k, mapping):
  item = mapping[k][0]
  exid = exid_for_items[item['content_id']]
  return {
      'widgets': unfreeze(k),
      'count': len(mapping[k]),
      'readable': nice_format(k),
      'first_item': item,
      'paths': map(named_topic_path, get_topic_paths(exid)),
      'exid': exid,
      'exname': exercises[exid]['pretty_display_name']
  }

# getting info about a specific configuration
# theone = mapping[by_size[17][2]][16]['content_id']
# exercises[exid_for_items[theone]]['pretty_display_name']
# map(named_topic_path, get_topic_paths(exid_for_items[theone]))

# clipboard.copy(mapping[by_size[1][1]][0]['item_data'])
# import clipboard


# ------- Mapping exercises to assesment items ---------

root_id = u'x00000000'
parents = get_parents(ttree_raw)
top_levels = get_toplevels(ttree_raw, parents, root_id)
segmented = {k: defaultdict(set) for k, _ in top_levels}
tuple(crawl(segmented, k, ttree_raw, k) for k in segmented)
# How many of each thing do the top level topics contain?
print [(ttree_raw[t]['title'], [(k, len(v)) for k, v in segmented[t].items()]) for t in segmented]

items_for_exercises = {k:
        flatten((item['id'] for item in pt['items'])
            for pt in exercises[k]['problem_types'])
                for k in exercises}

exid_for_items = {}
for exid, iids in items_for_exercises.items():
  for id in iids:
    exid_for_items[id] = exid

segmented_items = {k:
        set(flatten(items_for_exercises[e]
            for e in segmented[k]['Exercise']
                if e in items_for_exercises
                    and not exercises[e]['hide']
                    and exercises[e]['listed']
                    and not exercises[e]['do_not_publish']))
        for k in segmented}

# --------  Running the stuff --------

print "Running"

main_math = u'x7a488390'

math_items = segmented_items[main_math]
math_exercises = list(segmented[main_math]['Exercise'])
print len(math_items), 'math items'
math_data = [m for m in data if m['content_id'] in math_items]
layouts, mapping = organize_by_structure(math_data)
by_size = sorted((v, k) for k, v in layouts.items())[::-1]
print len(by_size), 'math layouts'

perc = lambda num: '%0.2f%%' % (sum(k for k, _ in (by_size[:num])) /float(len(math_items)) * 100)
print 1,5,10,20,30
print ' '.join([perc(1), perc(5), perc(10), perc(20), perc(30)])

print sum(m for m, _ in by_size[:200])/float(len(math_items))

json.dump([summary(k, mapping) for _, k in by_size[:200]],
    open('../2-analyze/wtypes/math-top-200.json', 'w'))
json.dump([summary(k, mapping) for _, k in by_size],
    open('../2-analyze/wtypes/math-configs.json', 'w'))

all_items = flatten(segmented_items[k] for k in segmented_items)
all_exercises = flatten(list(segmented[k]['Exercise']) for k in segmented)
print len(all_items), 'all items'
all_data = [m for m in data if m['content_id'] in all_items]
all_layouts, all_mapping = organize_by_structure(all_data)
all_by_size = sorted((v, k) for k, v in all_layouts.items())[::-1]
print len(all_by_size), 'all layouts'

perc = lambda num: '%0.4f%%' % (sum(k for k, _ in (all_by_size[:num])) /float(len(all_items)) * 100)
print 1,5,10,20,30
print ' '.join([perc(1), perc(5), perc(10), perc(20), perc(30)])

print sum(m for m, _ in all_by_size[:200])/float(len(all_items))

json.dump([summary(k, all_mapping) for _, k in all_by_size[:200]],
    open('../2-analyze/wtypes/all-top-200.json', 'w'))
json.dump([summary(k, all_mapping) for _, k in all_by_size],
    open('../2-analyze/wtypes/all-configs.json', 'w'))



