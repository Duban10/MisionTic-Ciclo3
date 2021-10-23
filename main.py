from re import A
from flask import *
import os
import sqlite3
from werkzeug.exceptions import MethodNotAllowed
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

@app.route("/loginADM/")
def loginADM():
    return render_template("loginADM.html")


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
    

@app.route('/ingresarADM', methods=["GET","POST"])
def ingresarADM():    
    if request.method == "POST":
        documento = request.form['document']
        contrasena = request.form['passw']        
        with sqlite3.connect("cineBD.db") as con:            
            cur = con.cursor()
            variablevector = cur.execute(f"select * from administrador where documento = '{documento}'").fetchone()            
            if variablevector != None:
                contraInterna = variablevector[5]
                docInterno = variablevector[0]
                session.clear()
            # if check_password_hash(variableInterna, contrasena):
                if contraInterna == "123" and docInterno == 10:            
                    session["documento"] = documento
                    return render_template("indexADM.html", documento=documento)
                    
            # else:
            #     return render_template("login.html")    
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

@app.route('/modif/', methods=["POST"])
def actualizar():
    if 'documento' in session:      
        if request.method == "POST":
            print("LLEGO")
            documento = request.form['cedula']
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            telefono = request.form['telefono']
            correo = request.form['correo']       
            with sqlite3.connect("cineBD.db") as conn:#Manejador de contexto ->conexion
                cur = conn.cursor()#manipula la db
                #se va a usar el PreparedStatement
                #Acciones
                cur.execute("UPDATE usuario SET nombre = ?, apellido = ?, telefono = ?, correo = ? WHERE documento = ?;", [nombre, apellido, telefono, correo, documento])
                conn.commit()#Confirmación de inserción de datos :)
                flash('Contacto Actualizado Correctamente')
                return redirect(url_for('perfUsuario'))
        return "No se pudo actualizar T_T"
    else:
        return "NO HA INICIADO SESION, INICIA SESIO AQUI <a href='/login/'>Redirección</a>" 


@app.route("/formulario/")
def formulario():
    if 'documento' in session:
        return render_template("formulario.html")
    else:
        return "NO HA INICIADO SESION, INICIA SESIO AQUI <a href='/loginADM/'>Redirección</a>" 
       


@app.route("/formUpdate/")
def formUpdate():
    if 'documento' in session:
        return render_template("formUpdate.html")
    else:
        return "NO HA INICIADO SESION, INICIA SESIO AQUI <a href='/loginADM/'>Redirección</a>" 



@app.route("/formDelete/")
def formDelete():
    if 'documento' in session:
        return render_template("formDelete.html")
    else:
        return "NO HA INICIADO SESION, INICIA SESIO AQUI <a href='/loginADM/'>Redirección</a>" 


@app.route('/actualizarpelicula/', methods=["GET","POST"])
def actualizarPelicula():    
    if 'documento' in session:
        if request.method == "POST":
            ident = request.form['idPelicula']
            nombre = request.form['nombre']
            duracion = request.form['duracion']
            genero = request.form['genero']       
            descripcion = request.form['descripcion'] 
            with sqlite3.connect("cineBD.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE pelicula SET nombre = ?, duracion = ?, genero = ?, descripcion = ? WHERE idpelicula = ?; ", [nombre, duracion, genero, descripcion, ident])
                con.commit()
                #return "PELICULA GUARDADA EXITOSAMENTE"
                flash('Pelicula Actualizada Correctamente')
                return redirect(url_for('formUpdate'))
        return " ERROR !!! No se pudo guardar"
    else:
        return "NO HA INICIADO SESION, INICIA SESIO AQUI <a href='/formulario/'>Redirección</a>" 

@app.route('/formulario/crearpelicula/', methods=["GET","POST"])
def crearPelicula():    
    if 'documento' in session:
        if request.method == "POST":
            ident = request.form['idPelicula']
            nombre = request.form['nombre']
            duracion = request.form['duracion']
            genero = request.form['genero']       
            descripcion = request.form['descripcion'] 
            with sqlite3.connect("cineBD.db") as con:
                cur = con.cursor()
                cur.execute("insert into pelicula(idpelicula, nombre, duracion, genero, descripcion) values (?, ?, ?, ?, ?)", (ident, nombre, duracion, genero, descripcion))
                con.commit()
                #return "PELICULA GUARDADA EXITOSAMENTE"
                flash('Pelicula Creada Correctamente')
                return redirect(url_for('formulario'))
        return " ERROR !!! No se pudo guardar"
    else:
        return "NO HA INICIADO SESION, INICIA SESIO AQUI <a href='/formulario/'>Redirección</a>" 

@app.route('/eliminarpelicula/', methods=["GET","POST"])
def eliminarPelicula():    
    if 'documento' in session:
        if request.method == "POST":
            idpel = request.form['idPelicula']
            with sqlite3.connect("cineBD.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("delete from pelicula where idpelicula = ?", [idpel])
                if con.total_changes > 0:                
                    #return "PELICULA GUARDADA EXITOSAMENTE"
                    flash('Pelicula Borrada Correctamente')
                    return redirect(url_for('formDelete'))
                else:
                    flash('NO ENCONTRO NINGUNA PELICULA CON ESE ID')
                    return render_template("formulario.html")
        return " ERROR !!! No se pudo guardar"
    else:
        return "NO HA INICIADO SESION, INICIA SESIO AQUI <a href='/formulario/'>Redirección</a>" 

if __name__=='__main__':
    app.run(debug=True)