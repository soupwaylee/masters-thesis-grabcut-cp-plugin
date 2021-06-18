const deps = require('./package.json').dependencies

module.exports = {
  publicPath: '/frontends/grabcut',

  chainWebpack: (config) => {
    config.optimization.delete('splitChunks')
    /* module federation plugin import */
    config
      .plugin('module-federation-plugin')
      .use(require('webpack').container.ModuleFederationPlugin, [{
        name: "plugin",
        filename: "remoteEntry.js",
        remotes: {},
        exposes: {},
        shared: {
          "vue": {
            eager: true,
            singleton: true,
            requiredVersion: deps.vue,
          }
        }
    }])
  },
  devServer: {
    port: 8080,
    hot: true,
    disableHostCheck: true,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
      "Access-Control-Allow-Headers":
        "X-Requested-With, content-type, Authorization",
    }
  }
}
