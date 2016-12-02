
const Perseus = require('../perseus/src/editor-perseus.js');
const ReactDOM = require('react-dom')
const ItemRenderer = require('../perseus/src/server-item-renderer.jsx');
const ApiClassNames = require("../perseus/src/perseus-api.jsx").ClassNames;

const renderItem = module.exports = (item, node, isMobile) => {
  const className = isMobile ?
    "framework-perseus " + ApiClassNames.MOBILE :
    "framework-perseus";
  const rendererComponent = <div className={className}>
    <ItemRenderer
      item={item}
      problemNum={1}
      hintsVisible={0}
      apiOptions={{
        getAnotherHint: () => {
        },
        isMobile: isMobile,
        customKeypad: isMobile,
        setDrawingAreaAvailable: () => {
        }
      }}
  />
  </div>;
  ReactDOM.render(rendererComponent, node);
}

