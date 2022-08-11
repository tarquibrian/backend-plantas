from genericpath import exists
import imp
from importlib.util import resolve_name
from os import getcwd
from asyncio.log import logger
from pydoc import cli
from statistics import variance
from time import monotonic
from tkinter.messagebox import RETRY
from urllib import response
from flask import Flask, flash, jsonify, request, Blueprint
from flask_pymongo import PyMongo, ObjectId
from flask_pymongo import pymongo
from flask_cors import CORS
from pkg_resources import ResolutionError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from responses.response_json import response_json
from routes.files import routes_files

app = Flask(__name__)
# app.config['MONGO_URI']='mongodb://127.0.0.1/Plantas_medicinalesDB'
# mongo = PyMongo(app)

CONNECTION = 'mongodb+srv://yoselin:123@cluster0.sfj6m.mongodb.net/test'

client = pymongo.MongoClient(CONNECTION)
mongo = client.get_database('Plantas_MedicinalesDB')

db = mongo.Administrador

cors = CORS(app)
# BASE DE DATOS
# db = mongo.db.Administrador

app.register_blueprint(routes_files)


@app.route('/Administrador-login', methods=['POST'])
def validateUser():
    print(request.json)
    # if key doesn't exist, returns None
    email = request.json['email']
    contrasena = request.json['contrasena']

    result = db.find_one({"email": email})
    if result is None:
        return jsonify({"Error": "no autorizado"}), 401

    if not check_password_hash(result['contrasena'], contrasena):
        return jsonify({"error": "contrasena incorrecta"}), 401

    response = jsonify({'email': email, 'constrasenaaaa': contrasena})
    response.headers.add('Access-Control-Allow-Origin', '*')
    # if key doesn't exist, returns a 400, bad request error
    return response
    # return jsonify(contrasena)

# Vamos a tener una ruta para poder crear usuarios


@app.route('/Administrador', methods=['POST'])
def createUsers():
    # print(json.loads(request.data))
    print(request.json)

    encriptado = generate_password_hash(request.json['contrasena'])

    id = db.insert_one(
        {'nombre': request.json['nombre'], 'email': request.json['email'], 'contrasena': encriptado})

    return jsonify(str(id.inserted_id))  # muestra el id de un usuario


# Vamos a tener una ruta para obtener usuarios
@app.route('/Administrador', methods=['GET'])
def getUsers():
    Administrador = []
    for doc in db.find():  # vamos ir anadiendo por cada documento e la lista
        Administrador.append({
            '_id': str(ObjectId(doc['_id'])),  # nos va a mostrar el id en str
            'nombre': doc['nombre'],
            'email': doc['email'],
            'contrasena': doc['contrasena']
        })

    return jsonify(Administrador)

# Vamos a tener una ruta para crear usuarios


@app.route('/Administrado/<id>', methods=['GET'])
def getUser(id):
    # va a retorar un administrador
    Administrado = db.find_one({'_id': ObjectId(id)})
    # print(Administrado)
    return jsonify({
        '_id': str(ObjectId(Administrado['_id'])),
        'nombre': Administrado['nombre'],
        'email': Administrado['email'],
        'contrasena': Administrado['contrasena']
    })

# Vamos a tener una ruta para crear usuarios


@app.route('/Administrador/<id>', methods=['DELETE'])
def deleteUsers(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'usuario eliminado'})

# Vamos a tener una ruta para crear usuarios


@app.route('/Administrador/<id>', methods=['PUT'])
def updateUsers(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'nombre': request.json['nombre'],
        'email': request.json['email'],
        'contrasena': request.json['contrasena']
    }})
    return jsonify({'msg': 'usuario actualizado'})


################################################################################################################
# PLANTAS

# db1 = mongo.db.Plantas_medicinales
db1 = mongo.Plantas_medicinales


# Vamos a tener una ruta para poder crear usuarios
@app.route('/Plantas_medicinales', methods=['POST'])
def createPlantas_medicinales():
    print(request.json)
    id = db1.insert_one({
        'nombre_cientifico': request.json['nombre_cientifico'],
        'nombre_planta': request.json['nombre_planta'],
        'propiedades': request.json['propiedades'],
        'descripcion': request.json['descripcion'],
        'conocimiento_ancestral': request.json['conocimiento_ancestral'],
        'imagen': request.json['imagen'],
        'latitud': request.json['latitud'],
        'longitud': request.json['longitud']
    })

    return jsonify(str(id.inserted_id))  # muestra el id de un usuario


# Vamos a tener una ruta para obtener usuarios
@app.route('/Plantas_medicinales', methods=['GET'])
def getPlantas_medicinales():
    Plantas_medicinales = []
    for doc in db1.find():  # vamos ir anadiendo por cada documento e la lista
        Plantas_medicinales.append({
            '_id': str(ObjectId(doc['_id'])),  # nos va a mostrar el id en str
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


# Vamos a tener una ruta para crear usuarios
@app.route('/Plantas_medicinale/<id>', methods=['GET'])
def getPlantas_medicinale(id):
    # va a retorar un administrador
    Plantas_medicinale = db1.find_one({'_id': ObjectId(id)})
    # print(Administrado)
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

# Vamos a tener una ruta para crear usuarios
@app.route('/Plantas_medicinales/<id>', methods=['DELETE'])
def deletePlantas_medicinales(id):
    db1.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'dato eliminado'})


# Vamos a tener una ruta para crear usuarios
@app.route('/Plantas_medicinales/<id>', methods=['PUT'])
def updatePlantas_medicinales(id):
    db1.update_one({'_id': ObjectId(id)}, {'$set': {
        'nombre_cientifico': request.json['nombre_cientifico'],
        'nombre_planta': request.json['nombre_planta'],
        'propiedades': request.json['propiedades'],
        'descripcion': request.json['descripcion'],
        'conocimiento_ancestral': request.json['conocimiento_ancestral'],
        'imagen': request.json['imagen'],
        'latitud': request.json['latitud'],
        'longitud': request.json['longitud']
    }})
    # return jsonify({'msg': 'dato actualizado'})
    response = jsonify({'hola': 'hola'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run(debug=True)
