from re import A
from flask import *
import os
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
variableGlobalVacia = None

app = Flask(__name__)

app.secret_key = os.urandom(24)

# lista_usuarios = ["Grey","Kathlen", "Miguel", "Orlando", "Duban"]
# lista_peliculas = {
#     "Pelicula1": "Pelicula 1 - Descripcion ...",
#     "Pelicula2": "Pelicula 2 - Descripcion ...",
#     "Pelicula3": "Pelicula 3 - Descripcion ...",
#     "Pelicula4": "Pelicula 4 - Descripcion ...",
#     "Pelicula5": "Pelicula 5 - Descripcion ...",
#     "Pelicula6": "Pelicula 6 - Descripcion ...",
#     "Pelicula7": "Pelicula 7 - Descripcion ...",
#     "Pelicula8": "Pelicula 8 - Descripcion ..."
# }


@app.route("/", methods=["GET","POST"])
def principal():
    return render_template("index.html")

@app.route("/login/")
def login():
    return render_template("login.html")


@app.route("/registro", methods=["GET","POST"])
def registro():
    return render_template("register.html")

@app.route("/recuperacion", methods=["GET","POST"])
def recuperacion():
    return render_template("forgot-password.html")


@app.route('/cerrarSesion/', methods=["POST", "GET"])
def cerrarSesion():
    if "documento" in session:#aquí amarro para que él esté logueado para que pueda entrar a los contenidos, sino, no entra
        session.pop("documento", None)
        return render_template("logOut.html")
    else:
        return "La sesión ya ha sido cerrada o nunca fue abierta"


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
        variablez = generate_password_hash(contrasena)
        with sqlite3.connect("cineBD.db") as con:
            cur = con.cursor()
            cur.execute("insert into usuario(documento, nombre, apellido, telefono, sexo, correo, contrasena) values (?, ?, ?, ?, ?, ?, ?)", (documento, nombre, apellido, telefono, sexo, correo, variablez))
            con.commit()
            return render_template("login.html")
    return " ERROR !!! No se pudo guardar"

@app.route('/ingresar', methods=["GET","POST"])
def ingresar():    
    if request.method == "POST":
        documento = request.form['document']
        contrasena = request.form['passw']        
        with sqlite3.connect("cineBD.db") as con:            
            cur = con.cursor()
            variablevector = cur.execute(f"select contrasena from usuario where documento = '{documento}'").fetchone()            
            if variablevector != None:
                variableInterna = variablevector[0]
                session.clear()
                if check_password_hash(variableInterna, contrasena):
                    session["documento"] = documento
                    return render_template("cartelera.html", documento=documento)
                
                else:
                    return render_template("login.html")    
        return "Error en la conexión y proceso, revise por favor :'("                                    
    return "No pudo ingresar"


@app.before_request
def puntoLogin():
    session.get("documento")#Quiere guardar la información, puede ser cualquier cosa
    if session.get("documento") is None:
        global variableGlobalVacia#sI TIENE ALGO ASÍGNELE ALGO
        variableGlobalVacia = "log"
    else:
        variableGlobalVacia = None #SINO VACÍELA 


@app.route('/', methods=["GET" , "POST"])#Aunque se esté en la ruta principal, si no está logueado se redireccionará a el logIn
def index():
    global variableGlobalVacia
    if variableGlobalVacia is not None:
        return redirect(url_for('login'))    # me redirige a la funcion login 
    return render_template('cartelera.html')


@app.route("/cartelera/", methods=["GET", "POST"])
def cartelera():
    if 'documento' in session:
        return render_template("cartelera.html")
    else:
        return "NO HA INICIADO SESION, INICIA SESIO AQUI <a href='/login/'>Redirección</a>" 

@app.route("/perfilUser/", methods=["GET","POST"])
def perfUsuario():
    if 'documento' in session:
        return render_template("perfil_usuario.html")
    else:
        return "NO HA INICIADO SESION, INICIA SESIO AQUI <a href='/login/'>Redirección</a>" 

if __name__=='__main__':
    app.run(debug=True)