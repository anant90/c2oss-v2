var webpack = require('webpack');

module.exports = {
	entry: './src/js/App.js',
	output: {
		path: "../c2oss-v2",
		filename: 'static/c2oss-v2/bundle.js'
	},
	module: {
		loaders: [
			{
				test: /\.jsx?$/,
				exclude: /(node_modules)/,
				loader: 'babel'
			},
			{ test: /\.png$/,
				loader: "file-loader?name=static/[name]-[hash].[ext]"
			},
			{ test: /\.(ttf|eot|svg)$/,
				loader: "file-loader?name=static/[name]-[hash].[ext]"
			}
		]
	},
	plugins: [
		new webpack.ProvidePlugin({
			'fetch': 'imports?this=>global!exports?global.fetch!whatwg-fetch'
		})
	]
};
