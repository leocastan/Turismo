let storeKey = "session-admin"

let storeKeyClientes = "session-cliente"
let views = {
    cliente: "../static/views/cliente.html", 
    reserva: "../static/views/reserva.html"
}



let sessionCliente = {
    id: "",
    name: "",
    reserva: ""
}

export { 
    views, 
    storeKey, 
    storeKeyClientes, 
    sessionCliente
 }