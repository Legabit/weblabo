module.exports = function(app) {
    var estadosCtrl = app.controllers.EstadosCtrl;
    var municipiosCtrl = app.controllers.MunicipiosCtrl;

    app.get('/api/estados', estadosCtrl.index);
    app.get('/api/estados/municipios/:idEstado', estadosCtrl.viewMunicipios);
    app.get('/api/estados/colonias/:idEstado', estadosCtrl.viewColonias);
    app.get('/api/municipios', municipiosCtrl.index);
    app.get('/api/municipios/:idMunicipio', municipiosCtrl.viewColonias);
    app.get('/', function(req, res) {
        res.json({message: "Sepomex Rest API"});
    });
};