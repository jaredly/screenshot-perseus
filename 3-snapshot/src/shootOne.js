const wc = require('electron').remote.getCurrentWebContents()
const fs = require('fs')

const shootOne = module.exports = (node, dest, done) => {
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

