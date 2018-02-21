var express = require('express');
var PORT=8081;
var app = express();
app.get('/',function(req,res)
	{
	res.sendfile('images.html');
	}
);
app.listen(PORT);
console.log('running on' +PORT);