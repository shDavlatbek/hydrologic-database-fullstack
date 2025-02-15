// vue.config.js
module.exports = {
  devServer: {
    port: 8199,
    host: '0.0.0.0',
    allowedHosts: [
      'hydrologic-database.uz',
      '.hydrologic-database.uz',
      'localhost'
    ],
    client: {
      webSocketURL: {
        hostname: 'localhost',
        port: 8199
      }
    }
  },
  
  // Optional: Configure public path if needed
  publicPath: process.env.NODE_ENV === 'production'
    ? 'https://hydrologic-database.uz/'
    : '/'
}