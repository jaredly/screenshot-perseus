
def touched_exercises(items):
  exids = set()
  for item in items:
    exids.add(exid_for_items[item['content_id']])
  return exids

def exes_touched_by(which):
  alls = set()
  for a, k in which:
    alls = alls.union(touched_exercises(mapping[k]))
  return alls

def exes_filled_by(which):
  touched = exes_touched_by(which)
  allis = set()
  for a, b, k in which:
    allis = allis.union([i['content_id'] for i in mapping[k]])
  filled = set()
  for ex in touched:
    if ex not in items_for_exercises:
      print 'um', ex
      continue
    if len(set(items_for_exercises[ex]).difference(allis)) == 0:
      filled.add(ex)
  return filled

len(exes_filled_by(by_size[:300])) / float(len(math_exercises))

len(exes_filled_by(by_size[:20]))

