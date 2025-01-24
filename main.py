# Imports
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)

app.secret_key = "IcTpaep8SbYEotENW3LXQxbkNDSSZUlH" # Clave para cifrar contraseñas

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flasklogin'

mysql = MySQL(app)


# Iniciar sesión
@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ""
    # Si las solicitudes POST "usuario" y "contraseña" existen: 
    if request.method == 'POST' and 'usuario' in request.form and 'contraseña' in request.form:
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        # Cifra contraseña
        hash = contraseña + app.secret_key
        hash = hashlib.sha1(hash.encode())
        contraseña = hash.hexdigest()

        # Revisa que la cuenta exista con MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    # Conexión a la base de datos
        cursor.execute('SELECT * FROM cuentas WHERE usuario = %s AND contraseña = %s', (usuario, contraseña))   # Consulta SQL
        cuenta = cursor.fetchone()

        if cuenta != None : # Si ha encontrado la cuenta (no es None):
            session['sesiónIniciada'] = True
            session['id'] = cuenta['id']
            session['usuario'] = cuenta['usuario']
            msg += 'Credenciales correctas.'
            return redirect(url_for('inicio'))
        else:
            msg += 'Credenciales incorrectas.'

    return render_template('login.html', msg=msg)

# Cerrar sesión
@app.route('/logout/')
def logout():
    session.pop('sesiónIniciada', None)
    session.pop('id', None)
    session.pop('usuario', None)
    return redirect(url_for('login'))

# Registro
@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    msg = ""
    # Si las solicitudes POST "usuario", "contraseña" y "email" existen: 
    if request.method == 'POST' and 'usuario' in request.form and 'contraseña' in request.form and 'email' in request.form:
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        email = request.form['email']
    
     # Revisa que la cuenta exista con MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    # Conexión a la base de datos
        cursor.execute('SELECT * FROM cuentas WHERE usuario = %s', (usuario,))   # Consulta SQL
        cuenta = cursor.fetchone()

        if cuenta: # Si ha encontrado la cuenta (no es None):
            msg = "La cuenta ya existe."
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):    # Formato de correo electrónico
            msg = "Correo inválido."
        elif not re.match(r'[A-Za-z0-9]+', usuario):       # Formato de nombre de usuario (letras y números)
            msg = "Nombre de usuario solo puede contener letras y números."
        elif not usuario or not contraseña or not email:
            msg = "Hay uno o más campos vacíos."
        else:   # Si el formulario pasa todas las validaciones: 
            # Cifra la contraseña
            hash = contraseña + app.secret_key
            hash = hashlib.sha1(hash.encode())
            contraseña = hash.hexdigest()
            #  Añade los valores a la base de datos
            cursor.execute("INSERT INTO cuentas VALUES (NULL, %s,%s,%s)", (usuario,contraseña,email))
            mysql.connection.commit()
            msg = 'Registro correcto.'

    elif request.method == 'POST':
        msg = "Formulario vacío."

    return render_template('registro.html', msg=msg)

@app.route('/')
def inicio():
    # Si la sesión está iniciada:
    if 'sesiónIniciada' in session:
        return render_template("inicio.html", usuario=session['usuario'])
    
    # Vuelve a la página de inicio de sesión
    return redirect(url_for('login'))

@app.route('/perfil/')
def perfil():
    # Si la sesión está iniciada:
    if 'sesiónIniciada' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuentas WHERE id = %s', (session['id'],))
        cuenta = cursor.fetchone()
        return render_template('perfil.html', cuenta = cuenta)
    # Vuelve a la página de inicio de sesión
    return redirect(url_for('login'))   

if __name__ == '__main__':
    app.run(debug=True)
