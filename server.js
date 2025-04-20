const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');
const app = express();

app.use('/api', createProxyMiddleware({ target: 'http://localhost:5000', changeOrigin: true }));
app.use(express.static(path.join(__dirname)));
app.get('*', (req, res) => res.sendFile(path.join(__dirname, 'index.html')));

app.listen(3000, () => console.log('Frontend running on http://localhost:3000'));