var express = require('express');
var PORT=8081;
var app = express();

app.use('/bootstrap', express.static(path.join(__dirname, './bootstrap')));

app.get('/',function(req,res)
	{
	res.sendfile('maps.html');
	}
);
app.listen(PORT);
console.log('running on' +PORT);