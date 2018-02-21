var express = require('express')
var PORT = 8080;

var app=express()
app.get('/', function(req,res)
 {
   res.sendfile('shoppingcardemo.html');
 }
);

app.get('/login', function(req, res) {
	res.sendfile('loginFacebook.html');
}
);

app.get('/cart', function(req, res) {
	res.sendfile('shoppingcar.html');
}
);

app.listen(PORT);
console.log('Running on port ' + PORT);

