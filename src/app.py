from asyncio.log import logger
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://127.0.0.1/Plantas_medicinalesDB'
mongo = PyMongo(app)


cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#BASE DE DATOS
db = mongo.db.Administrador

@app.route('/Administrador-login', methods=['POST']) #Vamos a tener una ruta para poder crear usuarios
def validateUser():
    
    # if key doesn't exist, returns None
    email = request.json['email']
    contrasena = request.json['contrasena']
    result = db.find_one({"email": email})
    if result is None:
        return jsonify({"Error": "no autorizado"}), 401

    if not check_password_hash(result['contrasena'], contrasena):
        return jsonify({"error": "contrasena incorrecta"}), 401

    
    # if key doesn't exist, returns a 400, bad request error
    return jsonify({'email': email, 'constrasenaaaa': contrasena}), 200
    # return jsonify(contrasena)


@app.route('/Administrador', methods=['POST']) #Vamos a tener una ruta para poder crear usuarios
def createUsers():
    # print(json.loads(request.data))
    print(request.json)

    encriptado = generate_password_hash(request.json['contrasena'])

    id = db.insert_one(
        {'nombre': request.json['nombre'], 'email': request.json['email'], 'contrasena': encriptado})
    
    return jsonify(str(id.inserted_id)) #muestra el id de un usuario


@app.route('/Administrador', methods=['GET']) #Vamos a tener una ruta para obtener usuarios
def getUsers():
    Administrador = []
    for doc in db.find():#vamos ir anadiendo por cada documento e la lista
        Administrador.append({
            '_id': str(ObjectId(doc['_id'])), #nos va a mostrar el id en str
            'nombre': doc['nombre'],
            'email': doc['email'],
            'contrasena': doc['contrasena']
        })

    return jsonify(Administrador)


@app.route('/Administrado/<id>', methods=['GET']) #Vamos a tener una ruta para crear usuarios
def getUser(id):
    Administrado = db.find_one({'_id': ObjectId(id)})#va a retorar un administrador
    #print(Administrado)
    return jsonify({
        '_id': str(ObjectId(Administrado['_id'])),
        'nombre': Administrado['nombre'],
        'email': Administrado['email'],
        'contrasena': Administrado['contrasena']
    })

@app.route('/Administrador/<id>', methods=['DELETE']) #Vamos a tener una ruta para crear usuarios
def deleteUsers(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'usuario eliminado'})

@app.route('/Administrador/<id>', methods=['PUT']) #Vamos a tener una ruta para crear usuarios
def updateUsers(id):
    db.update_one({'_id': ObjectId(id)}, {'$set':{
        'nombre': request.json['nombre'],
        'email': request.json['email'],
        'contrasena': request.json['contrasena']
    }})
    return jsonify({'msg': 'usuario actualizado'})


################################################################################################################
#PLANTAS

db1 = mongo.db.Plantas_medicinales

@app.route('/Plantas_medicinales', methods=['POST']) #Vamos a tener una ruta para poder crear usuarios
def createPlantas_medicinales():
    print(request.json)
    id = db1.insert_one({
            'nombre_cientifico': request.json['nombre_cientifico'],
            'nombre_planta': request.json['nombre_planta'],
            'propiedades': request.json['propiedades'],
            'descripcion': request.json['descripcion'],
            'conocimiento_ancestral': request.json['conocimiento_ancestral'],
            'imagen': request.files['imagen'],
            'latitud': request.json['latitud'],
            'longitud': request.json['longitud']
        })
    return jsonify(str(id.inserted_id)) #muestra el id de un usuario

@app.route('/Plantas_medicinales', methods=['GET']) #Vamos a tener una ruta para obtener usuarios
def getPlantas_medicinales():
    Plantas_medicinales = []
    for doc in db1.find():#vamos ir anadiendo por cada documento e la lista
        Plantas_medicinales.append({
            '_id': str(ObjectId(doc['_id'])), #nos va a mostrar el id en str
            'nombre_cientifico': doc['nombre_cientifico'],
            'nombre_planta': doc['nombre_planta'],
            'propiedades': doc['propiedades'],
            'descripcion': doc['descripcion'],
            'conocimiento_ancestral': doc['conocimiento_ancestral'],
            'imagen': doc['imagen'],
            'latitud': doc['latitud'],
            'longitud': doc['longitud']
        })

    return jsonify(Plantas_medicinales)


@app.route('/Plantas_medicinale/<id>', methods=['GET']) #Vamos a tener una ruta para crear usuarios
def getPlantas_medicinale(id):
    Plantas_medicinale = db1.find_one({'_id': ObjectId(id)})#va a retorar un administrador
    #print(Administrado)
    return jsonify({
        '_id': str(ObjectId(Plantas_medicinale['_id'])),
        'nombre_cientifico': Plantas_medicinale['nombre_cientifico'],
        'nombre_planta': Plantas_medicinale['nombre_planta'],
        'propiedades': Plantas_medicinale['propiedades'],
        'descripcion': Plantas_medicinale['descripcion'],
        'conocimiento_ancestral': Plantas_medicinale['conocimiento_ancestral'],
        'imagen': Plantas_medicinale['imagen'],
        'latitud': Plantas_medicinale['latitud'],
        'longitud': Plantas_medicinale['longitud']


    })

@app.route('/Plantas_medicinales/<id>', methods=['DELETE']) #Vamos a tener una ruta para crear usuarios
def deletePlantas_medicinales(id):
    db1.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'dato eliminado'})

@app.route('/Plantas_medicinales/<id>', methods=['PUT']) #Vamos a tener una ruta para crear usuarios
def updatePlantas_medicinales(id):
    db1.update_one({'_id': ObjectId(id)}, {'$set':{
        'nombre_cientifico': request.json['nombre_cientifico'],
        'nombre_planta': request.json['nombre_planta'],
        'propiedades': request.json['propiedades'],
        'descripcion': request.json['descripcion'],
        'conocimiento_ancestral': request.json['conocimiento_ancestral'],
        'imagen': request.files['imagen'],
        'latitud': request.json['latitud'],
        'longitud': request.json['longitud']

    }})
    return jsonify({'msg': 'dato actualizado'})


if __name__ == "__main__":
    app.run(debug=True)