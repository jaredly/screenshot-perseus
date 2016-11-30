const renderBatch = (items, dest, start, size, wait, done) => {
  const parent = document.createElement('div')
  // parent.style.display = 'inline-block'
  parent.style.margin = '0 auto'
  // parent.style.border = '1px solid black'
  document.body.appendChild(parent)
  for (var i=0; i<size && start + i < items.length; i++) {
    const representing = items[start + i].represents
    const annotation = `${representing} : ${start + i}`
    renderOne(items[start + i].item_data, parent, annotation)
  }

  setTimeout(() => {
    shootOne(parent, dest, () => {
      document.body.removeChild(parent)
      done()
    })
  }, wait)
}

const topStart = 0
const topEnd = 10
const allItems = {}
for (var i=topStart; i<topEnd; i++) {
  allItems[i] = require(`../../2-analyze/wtypes/top-${i}.json`)
}

const setThingsUp = () => {
  const wait = 1000

  window.sample = () => {
      let node = document.getElementById('perseus-container')
      for (var i=topStart; i<topEnd; i++) {
        renderOne(allItems[i][0].item_data, node, i)
      }
  }

  window.runAll = (sizes) => {
    clearone()
    const runOne = (at) => {
      const index = topStart + at;
      if (index >= topEnd) {
        console.log('finished')
        return
      }
      setup(index)
      gostart(sizes[at], () => runOne(at + 1))
    }
    runOne(0)
  }

  window.setup = topN => {
    const items = allItems[topN] // require(`../../2-analyze/wtypes/top-${topN}.json`)
    console.log('items', items.length)
    const destDir = 'top-' + topN

    const one = (num, batch, done) => {
      const dest = path.join(__dirname, `${destDir}/shot-${num}.png`)
      renderBatch(items, dest, num * batch, batch, wait, done)
    }

    const next = (num, batch, done) => {
      if (num * batch >= items.length) return (console.log('done'), done && done())
      one(num, batch, () => next(num + 1, batch, done))
    }

    window.gostart = (batch=5, done=null) => next(0, batch, done)
    window.goredo = (num, batch=5) => one(num, batch, () => console.log('done'))
    window.justone = num => {
      let node = document.getElementById('perseus-container')
      renderOne(items[num].item_data, node, num)
    }

  }

  window.clearone = () => {
    let node = document.getElementById('perseus-container')
    node.innerHTML = ''
  }
}

