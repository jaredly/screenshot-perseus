const renderOne = require('./renderOne')
const shootOne = require('./shootOne')

const renderNShoot = module.exports = (configs, wait, done) => {
  const parent = document.getElementById('perseus-container')

  const one = n => {
    if (n >= configs.length) return done()
    const node = renderOne(configs[n].item.item_data, parent, configs[n].annotation)
    setTimeout(() => {
      shootOne(node, configs[n].dest, () => {
        parent.removeChild(node)
        one(n + 1)
      })
    }, wait)
  }

  one(0)
}

