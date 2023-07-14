function guardar() {
    let n = document.getElementById("tipo").value
    let p = parseFloat(document.getElementById("talle").value)
    let i = document.getElementById("imagen").value

    // {
    //     "imagen": "https://picsum.photos/200/300?grayscale",
    //     "nombre": "MICROONDAS",
    //     "precio": 50000,
    //     "stock": 10
    //   }

    let producto = {
        tipo: n,
        talle: p,
        imagen: i
    }
    console.log(producto);
    let url = 'http://127.0.0.1:5000/productos'
    var options = {
        body: JSON.stringify(producto),
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'accept': "application/json"},
    }
    fetch(url, options)
        .then(function () {
            console.log("creado")
            alert("Grabado")
            // Devuelve el href (URL) de la página actual
            window.location.href = "./buzos.html";  
            // Handle response we get from the API
        })
        .catch(err => {
            //this.errored = true
            alert("Error al grabar" )
            console.error(err);
        })
}

