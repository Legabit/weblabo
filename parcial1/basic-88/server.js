var express = require('express');
var path =  require('path');

var PORT = 8082;

var app=express()

app.use('/styles', express.static(path.join(__dirname, './styles')));
app.use('/scripts', express.static(path.join(__dirname, './scripts')));
app.use('/images', express.static(path.join(__dirname, './images')));

app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.get('/store', function (req, res) {
    res.sendFile(path.join(__dirname + '/store.html'));
});

app.listen(PORT);

console.log('Running on port ' + PORT);