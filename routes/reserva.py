from flask import request, jsonify, Response
from bson.objectid import ObjectId
from bson.json_util import dumps

def save(mongo): 
    if request.method == 'POST':
        reservas = mongo.db.Reservas
        reserva = request.form['reserva']
        cliente_id = ObjectId(request.form['cliente'])
        hospedaje = request.form['hospedaje']
        limit = request.form['limit']

        found_reserva = reservas.find_one({
            "reserva": reserva,
            "hospedaje": hospedaje
        })

        if found_reserva != None:
            return jsonify({
                "saved": False,
                "error": "Ese paquete ya está reservado"
            })

        found_cliente = reservas.find_one({
            "cliente": cliente_id
        })


        if found_cliente != None:
            return jsonify({
                "saved": False,
                "error": "Este cliente ya tiene una reserva"
            })
        
        reservas.insert_one({
            "reserva": reserva,
            "hospedaje": hospedaje,
            "cliente": cliente_id,
            "limit": limit
        })
        
        return jsonify({
            "saved": True, 
            "message": "Reserva guardada correctamente"
        })

def getAll(mongo):
    if request.method == 'GET':
        reservas = mongo.db.Reservas
        data = dumps(reservas.aggregate([
        { 
            "$lookup": {
                    "from": "Users", 
                    "foreignField": "_id",
                    "localField": "cliente",
                    "as": "cliente"
                }
        },
        { 
            "$lookup": {
                "from": "Users", 
                "foreignField": "reserva",
                "localField": "id",
                "as": "students"
            }
        }])
        )
        return Response(data, mimetype="application/json")

def delete(mongo):
    reservas = mongo.db.Reservas
    users = mongo.db.Users
    id = ObjectId(request.form["id"])

    found_user = users.find_one({"reserva": id})
    if found_user != None:
        return jsonify({
            "error": "No es posible eliminar esta reserva. Tiene clientes registrados"
        })

    reservas.delete_one({"_id": id})
    return jsonify({
        "deleted": True,
        "message": "La reserva ha sido eliminada"
    })

def update(mongo):
    if request.method == "POST":
        reservas = mongo.db.Reserva
        id = ObjectId(request.form["id_reserva"])
        cliente = ObjectId(request.form["cliente_update"])
        reserva = request.form["reserva_update"]
        hospedaje = request.form["hospedaje_update"]
        limit = request.form["limit_update"]

        # Verificar que no exista
        found_reserva = reservas.find_one({
            "name": reserva,
            "hospedaje": hospedaje
        })

        if found_reserva != None:
            print(dumps(found_reserva))
            # Verificamos si no es el mismo
            isSame = found_reserva["_id"] == id
            if isSame == False:
                return jsonify({
                    "error": "La reserva ya existe"
                })

        # Verifys the cliente isnt assigned
        found_cliente = reservas.find_one({"cliente": cliente})
        if found_cliente != None:
            # Verificamos si no es el mismo
            isSame = found_cliente["_id"] == id
            if isSame == False:
                return jsonify({
                    "error": "El cliente ya tiene una reservacion"
                })

        reservas.find_one_and_update(
            {
                "_id": ObjectId(id) 
            },
            {
                "$set": {
                    "reserva": reserva,
                    "hospedaje": hospedaje,
                    "cliente": cliente,
                    "limit": limit
                }
            }
        )

        return jsonify({
            "updated": True,
            "message": "La reserva ha sido actualizada"
        })
        
        
