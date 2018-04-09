module.exports = function(sequelize, DataType) {
    var Sepomex = sequelize.define('sepomex', {
        idestado: DataType.INTEGER,
        estado: DataType.STRING,
        idmunicipio: DataType.INTEGER,
        municipio: DataType.STRING,
        ciudad: DataType.STRING,
        zona: DataType.STRING,
        cp: DataType.INTEGER,
        asentamiento: DataType.STRING,
        tipo: DataType.STRING
    }, {
        tableName: 'sepomex'
    });

    return Sepomex;
}