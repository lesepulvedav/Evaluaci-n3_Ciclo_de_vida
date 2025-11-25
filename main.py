from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Tienda de Lácteos")

# --- MODELOS ---
class Lacteo(BaseModel):
    id: int
    nombre: str
    tipo: str
    precio: float

# --- BASE DE DATOS SIMULADA ---
inventario = [
    Lacteo(id=1, nombre="Leche Entera Colun", tipo="Leche", precio=1500),
    Lacteo(id=2, nombre="Queso Gouda 250g", tipo="Queso", precio=4500),
    Lacteo(id=3, nombre="Yogurt Griego", tipo="Yogurt", precio=890),
]

# --- INTERFAZ GRÁFICA (HTML) ---
html_content = """
<!DOCTYPE html>
<html>
    <head>
        <title>Tienda de Lácteos</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
            h1 { color: #333; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }
            th { background-color: #4CAF50; color: white; }
            tr:hover { background-color: #f5f5f5; }
            .form-group { margin-bottom: 15px; }
            input, select { padding: 8px; width: 100%; box-sizing: border-box; margin-top: 5px; }
            button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; width: 100%; font-size: 16px; }
            button:hover { background-color: #45a049; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🥛 Gestión de Tienda de Lácteos</h1>
            
            <h3>Agregar Producto Nuevo</h3>
            <div class="form-group">
                <input type="number" id="id" placeholder="ID del producto">
                <input type="text" id="nombre" placeholder="Nombre (Ej: Queso Azul)">
                <select id="tipo">
                    <option value="Leche">Leche</option>
                    <option value="Queso">Queso</option>
                    <option value="Yogurt">Yogurt</option>
                    <option value="Mantequilla">Mantequilla</option>
                </select>
                <input type="number" id="precio" placeholder="Precio ($)">
                <button onclick="agregarProducto()">Agregar al Inventario</button>
            </div>

            <h3>Inventario Actual</h3>
            <table id="tablaProductos">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Tipo</th>
                        <th>Precio</th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            </table>
        </div>

        <script>
            async function cargarProductos() {
                const response = await fetch('/productos');
                const productos = await response.json();
                const tbody = document.querySelector('#tablaProductos tbody');
                tbody.innerHTML = '';
                productos.forEach(p => {
                    tbody.innerHTML += `<tr>
                        <td>${p.id}</td>
                        <td>${p.nombre}</td>
                        <td>${p.tipo}</td>
                        <td>$${p.precio}</td>
                    </tr>`;
                });
            }

            async function agregarProducto() {
                const id = document.getElementById('id').value;
                const nombre = document.getElementById('nombre').value;
                const tipo = document.getElementById('tipo').value;
                const precio = document.getElementById('precio').value;

                const response = await fetch('/productos', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ id: id, nombre: nombre, tipo: tipo, precio: precio })
                });

                if (response.ok) {
                    alert("Producto agregado!");
                    cargarProductos();
                } else {
                    alert("Error: Revisa que el ID no esté repetido.");
                }
            }

            window.onload = cargarProductos;
        </script>
    </body>
</html>
"""

# --- RUTAS DE LA API ---

@app.get("/", response_class=HTMLResponse)
def pagina_principal():
    return html_content

@app.get("/productos", response_model=List[Lacteo])
def obtener_productos():
    return inventario

@app.post("/productos", response_model=Lacteo)
def crear_producto(producto: Lacteo):
    for p in inventario:
        if p.id == producto.id:
            raise HTTPException(status_code=400, detail="ID ya existe")
    inventario.append(producto)
    return producto
