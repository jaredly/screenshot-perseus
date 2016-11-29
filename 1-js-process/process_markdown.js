
console.log('start')
const parse = require('./node-perseus').PerseusMarkdown.parse
console.log('loaded perseus')

const data = require('./small_items.json')
console.log('loaded data')
var x = '['
const out = require('fs').createWriteStream('./parsed.json')
out.write('[')

const walk = obj => {
  if (!obj) return
  if (Array.isArray(obj)) {
    obj.forEach(walk)
  } else if ('object' === typeof obj) {
    for (var name in obj) {
      if (name === 'content') {
        obj[name] = parse(obj[name])
      } else {
        walk(obj[name])
      }
    }
  }
}

const writeDatom = (datum, i) => {
  datum.item_data.question.content = parse(datum.item_data.question.content)
  walk(datum.item_data.question.widgets)
  datum.item_data.hints.forEach(hint => {
    walk(hint.widgets)
    hint.content = parse(hint.content)
  })
  out.write(JSON.stringify(datum))
  if (i < data.length - 1) out.write(',')
}
data.forEach(writeDatom)
console.log('writing')

out.end(']')
out.on('finish', () => {
  console.log('Finished writing')
})
// require('fs').writeFileSync('./parsed.json', x.slice(0, -1)+']')

