const express = require('express');
const load = require('express-load');
const bodyParser = require('body-parser');

const app = express();
const router = express.Router();
const port = process.env.PORT || 8081;

// Middlewares
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

load('models/schema.js')
    .then('controllers')
    .then('routes.js')
    .into(app);

var sequelize = app.models.schema.sequelize;

sequelize.sync().done(function() {
    app.listen(port, function() {
        console.log("Listening on port %s", port);
    })
})

module.exports = app;
