const Sequelize = require('sequelize');

module.exports = function(app) {
    var SepoMex = app.models.schema.sepomex;

    var EstadosController = {
        index: function(req, res) {
            SepoMex.findAll({
                attributes: [Sequelize.literal('DISTINCT idestado'), 'idestado', 'estado'],
                order: ['idestado']
            }).then(function(estados) {
                res.send(estados);
            });
        },

        viewMunicipios: function(req, res) {
            SepoMex.findAll({
                attributes: [Sequelize.literal('DISTINCT idmunicipio'), 'idmunicipio', 'municipio'],
                order: ['idmunicipio'],
                where: {
                    idestado: parseInt(req.params.idEstado)
                }
            }).then(function(municipios) {
                res.send(municipios);
            });
        },

        viewColonias: function(req, res) {
            SepoMex.findAll({
                attributes: [Sequelize.literal('DISTINCT asentamiento'), 'asentamiento', 'cp', 'tipo', 'municipio'],
                where: {
                    idestado: parseInt(req.params.idEstado)
                }
            }).then(function(municipios) {
                res.send(municipios);
            });
        },
    }

    return EstadosController;
};