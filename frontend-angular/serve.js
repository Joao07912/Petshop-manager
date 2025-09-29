const express = require('express');
const path = require('path');
const app = express();

// Servir arquivos estáticos
app.use(express.static(path.join(__dirname, 'src')));

// Rota principal
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'src', 'index.html'));
});

const PORT = 4200;
app.listen(PORT, () => {
  console.log(`Frontend rodando em http://localhost:${PORT}`);
});