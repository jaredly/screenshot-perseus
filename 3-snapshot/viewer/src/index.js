/**
 * Load up assessment items
 */

require('../perseus/src/perseus-env')

window.Khan = {
    Util: KhanUtil,
    error: function() {},
    query: {debug: ""},
    imageBase: "/images/",
};

const Perseus = window.Perseus = require('../perseus/src/editor-perseus.js');
// const React = window.React = require('react')
// const ReactDOM = window.ReactDOM = require('react-dom')
const ReactDOM = require('react-dom')

module.exports = {
  renderItem: require('./render-item'),
  ready: Perseus.init({
    skipMathJax: false,
    loadExtraWidgets: true
  }).then(function() {
      console.log('perseus is ready')
  }, function(err) {
      console.error(err); // @Nolint
  })
}

