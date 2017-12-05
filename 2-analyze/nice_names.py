
def nice_names(sig):
  if sig == 'math':
    return 'Math'
  if sig == 'reallylongmath':
    return 'Long math'
  if sig == 'text':
    return 'Text'
  if sig == 'text_and_numbers':
    return 'Text w/ numbers'
  if sig == 'text_and_math':
    return 'Text w/ inline math'
  if sig == 'blockMath':
    return 'Math block'

  if sig == 'newline':
    return 'newline'
  if sig == 'blockQuote':
    return 'Block quote'
  if sig == 'heading':
    return 'Heading'
  if sig == 'br':
    return 'Line break'
  if sig == 'table':
    return 'Table' # TODO better table handling
  if sig == 'image':
    return 'Image'

  if sig == 'longBlockMath':
    return 'Long math block'
  if sig == 'blockNumber':
    return 'Block number'
  if sig == 'number':
    return 'A number'
  if sig == 'list':
      # TODO better list handling
    return 'A list'
  if not isinstance(sig, tuple):
    print sig
    return sig
    # fail
  if sig[0] == 'inlineCode':
    return 'Code({})'.format(' + '.join(nice_names(sub) for sub in sig[1:]))
  if sig[0] == 'link':
    return 'Hyperlink({})'.format(' + '.join(nice_names(sub) for sub in sig[1:]))
  if sig[0] == 'u':
    return 'Underlined({})'.format(' + '.join(nice_names(sub) for sub in sig[1:]))
  if sig[0] == 'em':
    return 'Italics({})'.format(' + '.join(nice_names(sub) for sub in sig[1:]))
  if sig[0] == 'strong':
    return 'Bold({})'.format(' + '.join(nice_names(sub) for sub in sig[1:]))
  if sig[0] == 'paragraph':
    return ' + '.join(nice_names(sub) for sub in sig[1:])
  if sig[0] == 'widget' and sig[2] == 'radio':
    return ('Radio' if sig[3] == 'single' else 'MultiChoice') + '({})'.format(' and '.join(' + '.join(nice_names(sub) for sub in one) for one in sig[4]))
  if sig[0] == 'widget':
    return sig[2].title() + ' widget'
  if sig[0] == 'columns':
    return 'Columns({} and {})'.format(nice_names(sig[1]), nice_names(sig[2]))
  print 'umm', sig
  return sig[0]
  # fail

def nice_format(format):
  single = not isinstance(format[0], tuple) or format[0][0] != 'paragraph'
  if single:
    return ' + '.join(nice_names(sub) for sub in format)
  sections = []
  for toplevel in format:
    sections.append(nice_names(toplevel))
  return '\n'.join(sections)


if 0:
  nice_names(by_size[0][1][0])

  for i, (count, excount, format) in enumerate(by_size[:20]):
    single = not isinstance(format[0], tuple) or format[0][0] != 'paragraph'
    print '--', i, '({} items, {} exes)'.format(count, excount), '--', '1 section' if single else '{} section{}'.format(len(format), 's' if len(format) > 1 else '')
    print nice_format(format)
    print

  for i, (count, excount, format) in enumerate(by_size[1000:1020]):
    single = not isinstance(format[0], tuple) or format[0][0] != 'paragraph'
    print '--', i, '({} items, {} exes)'.format(count, excount), '--', '1 section' if single else '{} section{}'.format(len(format), 's' if len(format) > 1 else '')
    print nice_format(format)
    print

