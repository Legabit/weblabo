const Sequelize = require('sequelize');

module.exports = function(app) {
    var SepoMex = app.models.schema.sepomex;

    var MunicipioController = {
        index: function(req, res) {
            SepoMex.findAll({
                attributes: [Sequelize.literal('DISTINCT idmunicipio'), 'idmunicipio', 'municipio', 'estado'],
                order: ['idmunicipio']
            }).then(function(municipios) {
                res.send(municipios);
            });
        },

        viewColonias: function(req, res) {
            SepoMex.findAll({
                attributes: [Sequelize.literal('DISTINCT asentamiento'), 'asentamiento', 'cp', 'tipo', 'municipio'],
                order: ['asentamiento'],
                where: {
                    idmunicipio: parseInt(req.params.idMunicipio)
                }
            }).then(function(colonias) {
                res.send(colonias);
            });
        }
    }

    return MunicipioController;
};