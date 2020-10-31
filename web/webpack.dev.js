const common = require('./webpack.common.js');
const path = require('path');
const { merge } = require('webpack-merge');

module.exports = merge(common, {
  mode: 'development',
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'app.js',
  },
  resolve: {
    modules: ['node_modules'],
    alias: {
      'react-dom': '@hot-loader/react-dom',
    },
    extensions: ['.ts', '.tsx', '.js', '.jsx'],
  },
  devServer: {
    historyApiFallback: true,
    contentBase: './dist',
  },
  devtool: 'eval-source-map',
});
