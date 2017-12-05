const path = require('path')
window.alert = n => console.log('ALERTED', n)

const renderNShoot = require('./renderNShoot')
const renderOne = require('./renderOne')
const shootOne = require('./shootOne')
const base = path.join(__dirname, '..', 'data', 'samples')

const pad = (num, size) => {
  let t = num + '';
  while (t.length < size) {
    t = '0' + t
  }
  return t
}

const shootDescription = (sample, si, done) => {
  const dest = path.join(base, `sample-${pad(si, 2)}-desc.png`)
  const annotation = `${si}: ${sample.count} items\n${sample.readable}\n`
  const node = document.createElement('div')
  node.innerHTML = annotation
  node.style.whiteSpace = 'pre'
  node.style.display = 'inline-block'
  node.style.boxSizing = 'border-box'
  node.style.border = '1px solid #ccc'
  node.style.padding = '10px'
  document.body.appendChild(node)
  setTimeout(() => {
    shootOne(node, dest, () => {
      document.body.removeChild(node)
      done()
    })
  }, 100)
}

const testRender = window.testRender = (item, annotation) => {
  const parent = document.getElementById('perseus-container')
  parent.innerHTML = ''
  renderOne(item.item_data, parent, annotation || '')
}

const clearTestRender = window.clearTestRender = () => {
  const parent = document.getElementById('perseus-container')
  parent.innerHTML = ''
}

if (false) {
window.perseusRenderer.ready.then(() => {
  // const samples = window.samples = require('../../2-analyze/wtypes/sample-top-20-percent.json')
  const samples = window.samples = require('../../2-analyze/wtypes/all-configs.json')

  const configs = []

  window.shootDescriptions = () => {
    const next = n => {
      if (n >= samples.length) return console.log('done')
      shootDescription(samples[n], n, () => next(n + 1))
    }
    next(0)
  }

  window.addAllSections = (start=0) => {
    for (var i=start; i<samples.length; i++) {
      addSection(i)
    }
  }

  window.addSection = si => {
    const sample = samples[si]
    configs.push({
      annotation: `${si}\n${sample.readable}`,
      dest: path.join(base, `all-sample-${pad(si, 4)}.png`),
      item: sample.first_item,
    })
    /*
    sample.items.forEach((item, ii) => {
      const annotation = `${si} - ${ii}`
      configs.push({
        annotation,
        dest: path.join(base, `sample-${pad(si, 2)}-${ii}.png`),
        item,
      })
    })
    */
  }

  /*
  samples.forEach((sample, si) => {
    sample.items.forEach((item, ii) => {
      let annotation = `${si} - ${ii}`
      annotation = (ii == 0 ? sample.readable + `\n${sample.count} items\n` : '') + annotation
      configs.push({
        annotation,
        dest: path.join(base, `sample-${pad(si, 2)}-${ii}.png`),
        item,
      })
    })
  })
  */

  window.justOne = si => {
    const sample = samples[si]
    const config = {
      annotation: `${si}\n${sample.readable}`,
      dest: path.join(base, `all-sample-${pad(si, 4)}.png`),
      item: sample.first_item,
    }
    const parent = document.getElementById('perseus-container')
    renderOne(config.item.item_data, parent, config.annotation)
  }

  window.go = () => {
    renderNShoot(configs.slice(), 500, () => {
      console.log('DONE')
    })
    configs.splice(0, configs.length)
  }
})

}


window.perseusRenderer.ready.then(() => {
  // const samples = window.samples = require('../../2-analyze/wtypes/sample-top-20-percent.json')
  const items = window.items = require('../../findthis2.json')

  const configs = []

  let i = -1
  window.next = () => {
    i += 1
    const parent = document.getElementById('perseus-container')
    parent.innerHTML = ''
    console.log(items[i].content_id, i)
    renderOne(items[i].item_data, parent, `Item ${i}`)
  }

})

