from flask import Flask, app, request,render_template

app = Flask(__name__)


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


@app.route("/login/<id_usuario>", methods=["GET","POST"])
def login(id_usuario):
    if id_usuario in lista_usuarios:
        return render_template("cartelera.html")
    else:
        return f"El usuario {id_usuario} no existe"
    

@app.route("/cartelera", methods=["GET"])
def cartelera():
    return render_template("cartelera.html")

@app.route("/registro", methods=["GET","POST"])
def registro():
    return render_template("register.html")

@app.route("/recuperacion", methods=["GET","POST"])
def recuperacion():
    return render_template("forgot-password.html")

@app.route("/perfilUser", methods=["GET","POST"])
def perfUsuario():
    return render_template("perfil_usuario.html")

@app.route("/buscar/<id_pelicula>", methods=["GET"])
def buscar(id_pelicula):
    if id_pelicula in lista_peliculas:
        return lista_peliculas[id_pelicula]
    else:
        return f"LA PELICULA {id_pelicula} NO SE ENCONTRO"


if __name__=='__main__':
    app.run(debug=True)