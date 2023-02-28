const express = require('express');

const PORT = process.env.PORT || 3000;
const app = express();

app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));

app.use((req, res, next) => {
  res.locals.path = req.path;
  next();
});

app.listen(PORT);

app.get('/', (req, res) => {
  res.render('login');
});
