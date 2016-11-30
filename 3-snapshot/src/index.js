const wc = require('electron').remote.getCurrentWebContents()
const fs = require('fs')
const path = require('path')
window.alert = n => console.log('ALERTED', n)

const renderOne = (data, parent, annotation) => {
  const node = document.createElement('div')
  node.style.position = 'relative'
  parent.appendChild(node)
  const inner = document.createElement('div')
  const num = document.createElement('div')
  num.innerHTML = annotation
  num.style.position = 'absolute'
  num.style.right = '10px'
  num.style.bottom = 0
  num.style.color = '#777'
  num.style.opacity = 0.5

  node.appendChild(inner)
  node.appendChild(num)

  window.perseusRenderer.renderItem(JSON.parse(data), inner, true)
  return node
}

const shootOne = (node, dest, done) => {
  const box = node.getBoundingClientRect()
  wc.capturePage({
    x: Math.floor(box.left),
    y: Math.floor(box.top),
    width: Math.ceil(box.width),
    height: Math.ceil(box.height),
  }, image => {
    fs.writeFileSync(dest, image.toPNG())
    console.log('wrote to', dest)
    done()
  })
}

window.perseusRenderer.ready.then(() => {
})

/*
const dests = {
  'n-1': 'math-expression',
  'n-2': 'boldmathtext-expression',
  'n-3': 'boldmathtext-radio',
}
*/

  /*
  // let node = document.getElementById('perseus-container')
  // window.perseusRenderer.renderItem(JSON.parse(items[0].item_data), node, true)
  // const batch = 5
    // window.perseusRenderer.renderItem(JSON.parse(items[num].item_data), node, true)
  const next = num => {
    // if (num < items.length) setTimeout(() => next(num + 1), 10)
  }
  next(0)
  */
