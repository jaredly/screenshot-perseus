const webpack = require('webpack')
const path = require('path')

module.exports = {
    entry: './src',
    output: {
        path: "./public",
        publicPath: "/",
        filename: "build.js",
        libraryTarget: 'var',
        library: 'perseusRenderer',
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': `"${process.env.NODE_ENV}"`,
        }),
    ],

    externals: {
      jquery: 'jQuery',
      underscore: '_',
      react: 'React',
      'react-dom': 'var React.__internalReactDOM',
      "react-addons-create-fragment":
          "var React.__internalAddons.createFragment",
      "react-addons-pure-render-mixin":
          "var React.__internalAddons.PureRenderMixin",
      "react-addons-css-transition-group":
          "var React.__internalAddons.CSSTransitionGroup",
    },

    module: {
        loaders: [
            {
                test: /\.json$/,
                loader: "json-loader",
            },
            {
                test: /\.jsx?$/,
                include: [
                    path.join(__dirname, "src/"),
                    path.join(__dirname, "perseus/src/"),
                    // TODO(kevinb) figure out a better way to package this
                    path.join(__dirname, "perseus/math-input/"),
                    path.join(__dirname, "perseus/react-components/"),
                    path.join(__dirname, "node_modules/react-components/"),
                ],
                // https://github.com/webpack/webpack/issues/119
                loader: path.join(__dirname, "perseus/node/jsx-loader.js"),
            },
            {
                test: /\.jison$/, loader: "jison-loader",
            },
        ],
    },
};
