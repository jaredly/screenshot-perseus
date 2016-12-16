
const renderOne = module.exports = (data, parent, annotation) => {
  const node = document.createElement('div')
  node.style.position = 'relative'
  node.style.borderLeft = '1px solid #ccc'
  node.style.transform = 'scale(.75)'
  node.style.transformOrigin = 'top left'
  node.style.borderRight = '1px solid #ccc'
  parent.appendChild(node)
  const top = document.createElement('img')
  top.src = './top.png'
  top.style.width =  '375px'
  top.style.borderBottom = '1px solid #ccc'
  node.appendChild(top)

  const inner = document.createElement('div')
  inner.style.marginTop = '-5px'
  inner.style.overflow = 'auto'
  inner.style.width = '375px' // the width of an iphone 6/7
  // inner.style.height = (
    // 542 /* the available height in our mobile app on an iphone 6/7 */
    // - 48 /* the margin top of the perseus thing */
    // - 5 /* dunno why but I need to correct more */
  // ) + 'px'
  const num = document.createElement('div')
  num.innerHTML = annotation
  num.style.position = 'absolute'
  num.style.top = '5px'
  num.style.left = '90px'
  num.style.fontSize = 8
  num.style.backgroundColor = 'white'
  num.style.opacity = 1
  num.style.borderColor = '#ccc'
  num.style.borderWidth = 3
  num.style.borderStyle = 'solid'
  num.style.border = '3px solid #ccc'
  num.style.padding = '0px 3px'
  num.style.borderRadius = '5px'
  num.style.color = '#777'
  // num.style.opacity = 0.5
  num.style.whiteSpace = 'pre'

  node.appendChild(inner)
  const bottom = document.createElement('img')
  bottom.style.width =  '375px'
  bottom.style.marginBottom = '-5px'
  bottom.src = './bottom.png'
  node.appendChild(bottom)

  node.appendChild(num)

  window.perseusRenderer.renderItem(JSON.parse(data), inner, true)

  const help = document.createElement('img')
  help.style.width =  '375px'
  help.style.marginTop = '46px'
  help.src = './help.png'
  inner.appendChild(help)

  return node
}

