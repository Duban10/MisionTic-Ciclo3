from flask import Flask, app, request,render_template, sessions
import os
import sqlite3

app = Flask(__name__)

app.secret_key = os.urandom(24)

lista_usuarios = ["Grey","Kathlen", "Miguel", "Orlando", "Duban"]
lista_peliculas = {
    "Pelicula1": "Pelicula 1 - Descripcion ...",
    "Pelicula2": "Pelicula 2 - Descripcion ...",
    "Pelicula3": "Pelicula 3 - Descripcion ...",
    "Pelicula4": "Pelicula 4 - Descripcion ...",
    "Pelicula5": "Pelicula 5 - Descripcion ...",
    "Pelicula6": "Pelicula 6 - Descripcion ...",
    "Pelicula7": "Pelicula 7 - Descripcion ...",
    "Pelicula8": "Pelicula 8 - Descripcion ..."
}


@app.route("/", methods=["GET","POST"])
def principal():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login/<id_usuario>", methods=["GET","POST"])
def login2(id_usuario):
    if id_usuario in lista_usuarios:
        return render_template("cartelera.html")
    else:
        return f"El usuario {id_usuario} no existe"
            
@app.route("/login/cartelera")
@app.route("/cartelera", methods=["GET"])
def cartelera():
    return render_template("cartelera.html")


@app.route("/registro", methods=["GET","POST"])
def registro():
    return render_template("register.html")

@app.route("/recuperacion", methods=["GET","POST"])
def recuperacion():
    return render_template("forgot-password.html")

@app.route("/perfilUser/")
@app.route("/login/perfilUser")
def perfUsuario():
    return render_template("perfil_usuario.html")

@app.route("/buscar", methods=["GET"])
def buscar():
    return render_template("buscar.html")
    # if id_pelicula in lista_peliculas:
    #     return lista_peliculas[id_pelicula]
    # else:
    #     return f"LA PELICULA {id_pelicula} NO SE ENCONTRO"
@app.route("/login/detalle")
def func():
    return render_template("detalle_cartelera.html")


@app.route('/guardar', methods=["POST"])
def guardar():    
    if request.method == "POST":
        documento = request.form['documento']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        telefono = request.form['telefono']
        sexo = request.form['sexo']
        with sqlite3.connect("cineBD.db") as con:
            cur = con.cursor()
            cur.execute("insert into usuario(documento, nombre, apellido, telefono, sexo, correo, contrasena) values (?, ?, ?, ?, ?, ?, ?)", (documento, nombre, apellido, telefono, sexo, correo, contrasena))
            con.commit()
            return render_template("login.html")
    return "No se pudo guardar"

@app.route('/ingresar', methods=["GET","POST"])
def ingresar():    
    if request.method == "POST":
        documento = request.form['document']
        contrasena = request.form['passw']
        with sqlite3.connect("cineBD.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from usuario where documento = ? AND contrasena = ?", [documento,contrasena])
            row = cur.fetchone()
            if row is None:
                # return render_template("login.html")
                return "USUARIO Y/O CONTRASEÑA INCORRECTA"
            return render_template("cartelera.html", row = row)                       
    return "No pudo ingresar"

if __name__=='__main__':
    app.run(debug=True)