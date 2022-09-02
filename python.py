from flask import Flask, render_template, session
from flask_pymongo import PyMongo
import routes.login as login
import routes.reserva as reserva
import routes.cliente as cliente


app = Flask(__name__, template_folder='templates')

#################### MONGO DB #################### 
# Conexion con la Base de datos
app.config['MONGO_DBNAME'] = 'Turismo'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Turismo'
mongo = PyMongo(app)

#################### LOGIN 2 #################### 
# Login del Admin
@app.route('/')
def show_main_pane():
    return render_template('/logAdmin.html')

# Valida el ingreso del Admin
@app.route('/login-admin', methods=['POST'])
def validate_access_admin():
    return login.validateAccess(mongo)


#################### PANLE PRINCIPAL 1 ####################
# Muestra el panel de control
@app.route('/control-panel', methods=['GET'])
def controlPane():
    return render_template('/regData.html')


#################### CLIENTE  4#################### 
# Register un cliente
@app.route('/save-cliente', methods=['POST'])
def save_cliente():
    return cliente.save(mongo)

# Despliega todos los clientes
@app.route('/get-clientes', methods=['GET'])
def get_clientes():
   return cliente.getAll(mongo)

# Actualiza el cliente 
@app.route('/update-cliente', methods=['POST'])
def update_cliente():
    return cliente.update(mongo)

# Elimina un cliente 
@app.route('/delete-cliente', methods=['POST'])
def delete_cliente():
    return cliente.delete(mongo)


#################### RESERVA 4 ####################
# Guarda la reserva --------------------------
@app.route('/save-reserva', methods=['POST'])
def save_reserva():
    return reserva.save(mongo)

# Despliega todos las reservas
@app.route('/get-reservas', methods=['GET'])
def get_reservas():
    return reserva.getAll(mongo)

# Actualiza una reserva
@app.route('/update-reserva', methods=['POST'])
def udpate_reserva():
    return reserva.update(mongo)

# Elimina la reserva
@app.route('/delete-reserva', methods=['POST'])
def delete_reserva():
    return reserva.delete(mongo)


#################### CERRAR SESION 1 #################### 
@app.route('/login')
def CerrarSesion():
    session.pop('username', None)
    return render_template('/logAdmin.html')


#################### MAIN DEL PROGRAMA 1 #################### 
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
