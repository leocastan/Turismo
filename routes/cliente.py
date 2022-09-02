from flask import request, Response, jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

def getAll(mongo):
    if request.method == 'GET':
        users = mongo.db.Users
        clientes = users.find({"rol": ["Cliente"]})
        data = dumps(clientes)
        return Response(data, mimetype="application/json")

def save(mongo):
    if request.method == 'POST':
        users = mongo.db.Users
        dni = request.form['dni']
        cliente_name = request.form['name']
        username = "cli" + request.form['dni']
        existing_user = users.find_one({'username': username})

        if existing_user is None:
            password = generate_password_hash(dni, "sha256", 10)
            users.insert_one({
                "dni": dni,
                "name": cliente_name,
                "username": "cli_" + dni,
                "password": password,
                "rol": ["Cliente"]
            })

            return jsonify({
                "saved": True, 
                "message": "Cliente guardado correctamente"
            })
        return jsonify({
                "saved": False,
                "error": "Ya existe un cliente con esa cédula"
            })

def delete(mongo):
    if request.method == 'POST':
        users = mongo.db.Users
        reservas = mongo.db.Reservas
        id = ObjectId(request.form["id"])
        found_reserva = reservas.find_one({"cliente": id})

        if found_reserva != None:
            return jsonify({
                "saved": False, 
                "error": "No es posible eliminar, el cliente tiene una reservacion"
            })

        users.delete_one({"_id": id})
        return jsonify({
            "saved": True, 
            "message": "Cliente eliminado"
        })

def update(mongo):
    if request.method == 'POST':
        users = mongo.db.Users
        id = ObjectId(request.form["id"])
        name = request.form["name"]
        dni = request.form["dni"]

        found_cliente = users.find_one({"dni": dni})
        print(found_cliente)
        # Veriifcamos si ya existe esa cedula
        if found_cliente != None:
            isSame = found_cliente['_id'] == id
            if isSame == False:
                return jsonify({
                    "error": "Este usuario ya existe"
                })

        password = generate_password_hash(dni, "sha256", 10)
        users.find_one_and_update(
            {
                "_id": id
            },
            {
                "$set": {
                    "name": name,
                    "dni": dni,
                    "username": "cli_"+dni,
                    "password": password
                }
            }
        )

        return jsonify({
            "updated": True, 
            "message": "Cliente actualizado correctamente"
        })


def validateAccess(mongo):
    users = mongo.db.Users
    reservas = mongo.db.Reservas
    username = request.form['username']
    password = request.form['password']
    rol_admin = "Cliente"

    login_user = users.find_one({
        'username': username, 
        "rol": [rol_admin]
    })

    if login_user == None:
         return jsonify ({
            "access": False,
            "error": "Usuario no es valido"
        })  


    passwordIsValid = check_password_hash(login_user["password"], password)
    if passwordIsValid:
        reserva = reservas.find_one({"cliente": login_user["_id"]})
        data = dumps({
            "access": True,
            "data": login_user,
            "reserva": reserva
        })
        return Response(data, mimetype="application/json")
