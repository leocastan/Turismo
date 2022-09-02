import { resetValues, validateField, validateFieldsObject } from "./formValidator.js"
import { getModal } from "./modal.js"

let form = document.querySelector("form")
let body = document.querySelector("body")
let {reserva, hospedaje, cliente, limit}  = form
let {modal, showModal, hideModal} = getModal()
let formModal = modal.querySelector('form')
let {
    hospedaje_update, 
    reserva_update,
    limit_update,
    cliente_update
} = formModal

loadHospedajes()
loadLimit()
loadClientes()
loadTable()

let validator = {
    reserva: false,
    hospedaje: false,
    cliente: false,
    limit: false,
}

let errors = {
    reserva: "Seleccione un lugar",
    hospedaje: "Seleccione tipo de hspedaje",
    cliente: "Seleccione el cliente",
    limit: "Seleccione numero de personas"
}

let data = {
    reserva: "",
    hospedaje: "",
    cliente: "",
    limit: ""
}

let validatorUpdate = {
    reserva_update: false,
    hospedaje_update: false,
    cliente_update: false,
    limit_update: false,
}

let errorsUpdate = {
    reserva_update: "Seleccione un lugar",
    hospedaje_update: "Seleccione tipo de hospedaje",
    cliente_update: "Seleccione el cliente",
    limit_update: "Seleccione numero de personas"
}

let dataUpdate = {
    id_reserva: "",
    reserva_update: "",
    hospedaje_update: "",
    cliente_update: "",
    limit_update: 0,
    students: 0
}

reserva.onchange = (e) => {
    const objectValidator = {
        element: e.target,
        field: "reserva",
        values: data,
        selector: ".error-reserva",
        validator,
        errors
    }
    validateField(objectValidator) 
}

hospedaje.onchange = (e) => {
    const objectValidator = {
        element: e.target,
        field: "hospedaje",
        values: data,
        selector: ".error-hospedaje",
        validator,
        errors
    }
    validateField(objectValidator) 
}

cliente.onchange = (e) => {
    const objectValidator = {
        element: e.target,
        field: "cliente",
        values: data,
        selector: ".error-cliente",
        validator,
        errors
    }
    validateField(objectValidator) 
}

limit.onchange = (e) => {
    const objectValidator = {
        element: e.target,
        field: "limit",
        values: data,
        selector: ".error-limit",
        validator,
        errors
    }
    validateField(objectValidator) 
}

reserva_update.onchange = (e) => {
    const objectValidator = {
        element: e.target,
        field: "reserva_update",
        values: dataUpdate,
        selector: ".error-reserva-update",
        validator: validatorUpdate,
        errors: errorsUpdate
    }
    validateField(objectValidator) 
}

hospedaje_update.onchange = (e) => {
    const objectValidator = {
        element: e.target,
        field: "hospedaje_update",
        values: dataUpdate,
        selector: ".error-hospedaje-update",
        validator: validatorUpdate,
        errors: errorsUpdate
    }
    validateField(objectValidator) 
}

cliente_update.onchange = (e) => {
    const objectValidator = {
        element: e.target,
        field: "cliente_update",
        values: dataUpdate,
        selector: ".error-cliente-update",
        validator: validatorUpdate,
        errors: errorsUpdate
    }
    validateField(objectValidator) 
}

limit_update.onchange = (e) => {
    const objectValidator = {
        element: e.target,
        field: "limit_update",
        values: dataUpdate,
        selector: ".error-limit-update",
        validator: validatorUpdate,
        errors: errorsUpdate
    }
    validateField(objectValidator) 
}

form.addEventListener("submit", async(e) => {
    e.preventDefault()
    if(validateFieldsObject(data)) {
        const route = "/save-reserva"
        $.post(route, data, (result) => {
            if(result.saved) {
                return Swal.fire("Listo!!", result.message, "success")
                .then(ok => {
                        form.reset()
                        resetValues(data)
                        loadTable()
                })
            } else {
                Swal.fire("Atención!!", result.error, "warning")
                }
            })

    } else {
        Swal.fire("Atención", "Debe haber seleccionado todos los campos", "warning")
    }
})

formModal.addEventListener("submit", async(e) => {
    e.preventDefault()
    if(validateFieldsObject(dataUpdate)) {
        const route = "/update-reserva"
        $.post(route, dataUpdate, (result) => {
            if(result.updated) {
                return Swal.fire("Listo!!", result.message, "success")
                .then(ok => {
                        formModal.reset()
                        resetValues(dataUpdate)
                        loadTable()
                        hideModal()
                })
            } else {
                Swal.fire("Atención!!", result.error, "warning")
                }
            })

    } else {
        Swal.fire("Atención", "Debe seleccionar todos los campos", "warning")
    }
})

async function loadClientes() {
    const route = "/get-clientes"
    const optDefault = `
        <option value="">
            Seleccione el cliente
        </option>
    `
    cliente.innerHTML = optDefault
    cliente_update.innerHTML = optDefault

    let response = await fetch(route)
    let result = await response.json()
    
    if(result.length> 0) {
        result.forEach(data => {
            let opt = `
                <option value="${data._id.$oid}">
                    ${data.name}
                </option>
            `
            cliente.innerHTML += opt
            cliente_update.innerHTML += opt
        }); 
    }
}

//Hospedaje
function loadHospedajes() {
    let total = ["Economica", "Cabaña_Familiar", "Cabaña_Termal"]
    total.forEach(letter => {
        hospedaje.innerHTML += `
            <option value=${letter}>
                ${letter}
            </option>
        `
        hospedaje_update.innerHTML += `
            <option value=${letter}>
                ${letter}
            </option>
        `
    })
}

//Reserva limit
function loadLimit() {
    let total = 10
    for (let i = 1; i <= total; i++) {
        const opt = `
            <option value=${i}>
                ${i}
            </option>
        `
        limit.innerHTML += opt
        limit_update.innerHTML += opt

    }
}

function loadTable() {
    const tbody = document.querySelector('tbody')
    const route = "/get-reservas"
    tbody.innerHTML = ""
    $.get(route, (result) => {
        if(result.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td class="text-center" colspan="6">
                        No existen reservas
                    </td>
                </tr>
            `
        } else {
            result.forEach((data, index) => {
                let id = data._id.$oid
                let totalStudents = data.students.length
                let available = data.limit  - totalStudents
                let clienteName = data.cliente[0].name
                let clienteID = data.cliente[0]._id.$oid
                let row = `
                    <tr>
                        <th class="text-center">${index + 1}</th>
                        <td class="text-center">${data.reserva}</td>
                        <td class="text-center">${data.hospedaje}</td>
                        <td class="text-center" data-id="${clienteID}">
                            ${clienteName}
                        </td>
                        <td class="text-center">${data.limit}</td>
                        <td class="text-center">${data.limit}</td>
                        <td class="text-center">
                            <button class="btn btn-primary" data-update="${id}">
                                Editar
                            </button>
                            <button class="btn btn-danger" data-delete="${id}">
                                Borrar
                            </button>
                        </td>
                    </tr>
                `
                tbody.innerHTML += row
            })
        }
    })
}

function deleteReserva(id) {
    const route = "/delete-reserva"
    $.post(route, {id}, (result) => {
        if(result.deleted) {
            return Swal.fire("Listo!!", result.message, "success")
            .then(ok => {
                loadTable()
            })
        } else {
            Swal.fire("Atención!!", result.error, "warning")
        }
    })
}

body.onclick = async (e) => {
    let element = e.target
    let updateID = element.dataset.update
    let deleteID = element.dataset.delete

    if( updateID ) {
        let row = element.parentNode.parentNode
        let tds = row.querySelectorAll('td')
        let reserva = tds[0].innerHTML
        let hospedaje = tds[1].innerHTML
        let cliente = tds[2].dataset.id
        let limit = tds[3].innerHTML
        let students = tds[3].innerHTML //limit //- tds[4].innerHTML
        dataUpdate.id_reserva = updateID
        dataUpdate.students = limit
        let data = {
            reserva_update: reserva,
            hospedaje_update: hospedaje,
            cliente_update: cliente,
            limit_update: limit,
        }

        dataUpdate = { ...dataUpdate, ... data }
        showModal(data)
    }

    if (deleteID) {
        deleteReserva(deleteID)
    }

} 

