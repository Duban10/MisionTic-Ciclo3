from random import random

from re import A
from flask import *
import os

import sqlite3
from werkzeug.exceptions import MethodNotAllowed
from werkzeug.security import check_password_hash, generate_password_hash
variableGlobalVacia = None

app = Flask(__name__)

app.secret_key = os.urandom(24)



@app.route("/", methods=["GET","POST"])
def principal():
    return render_template("login.html")



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
        variablez = generate_password_hash(contrasena)
        monto= 1000000
        cuenta="1234567890"
        with sqlite3.connect("cineBD.db") as con:
            cur = con.cursor()
            cur.execute("insert into usuario(documento, nombre, apellido, correo, cuenta, monto, contrasena) values (?, ?, ?, ?, ?, ?, ?)", (documento, nombre, apellido, correo, cuenta, monto, variablez))
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
                    return render_template("transacciones.html", documento=documento)
                
                else:
                    return render_template("login.html")    
        return "Usuario o Contraseña Incorrecta Intente de Nuevo"                                    
    return "No pudo ingresar"
    



if __name__=='__main__':
    app.run(debug=True)