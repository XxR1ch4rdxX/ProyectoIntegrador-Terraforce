#Aqui podremos poner la parte logica de nuestro crud del pi
#como links a otros html , getters , sertters cookies
#incluso la conexion con la base de datos

#ESTE ES EL CORAZON DE LA PAGINA WEB (por asi decirlo)
#Los documentos html adjuntos unicamente se utilizara el de crud, index y editar, los otros
#son "plantillas" que estan colocadas para usarse en algun momento
#Universal Crud :D


#para las librerias usamos translate para traducir los mensajes de eror que mandaran los try y catch desde sql
#colorama lo usamos para cambiar el color de las letritas de la consola
from colorama import init, Fore, Style
from googletrans import Translator
import pyodbc
from flask import Flask, render_template, request, flash, redirect,session, url_for, abort
from flask_mysqldb import MySQL
import socket
import sqlite3



#establece la conexion con sql server
init()

app = Flask(__name__)
app.secret_key = '123'
server = socket.gethostname()
#aqui cambiamos la base de datos , por la que tengamos en nuestro SQL SERVER
#esto quiere decir que nos servira para mas de una base de datos , en este caso es la de el pi
#por lo tanto podemos hacer altas bajas y cambios en cualquier tabla
database = 'TerraForce'  #si queremos cambiar de db , debemos cambiar el 'TU_BASEDEDATOS' y listo.
titulo = database
conn = sqlite3.connect(database)
cursor = conn.cursor()

if database == 'TacoLovers':
    icon = "../static/images/taco.ico"
elif database == 'TerraForce':
    icon = "../static/images/logoterra1.ico"
else:
    icon = "../static/images/demon.ico"

try:
    print(Fore.CYAN + 'Estableciendo la conexion con sql server ...' + Style.RESET_ALL)
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server + '; DATABASE=' + database + '; Trusted_Connection=yes;')
    print(Fore.GREEN + 'Tamo en linea ' + Style.RESET_ALL)
    cursor = connection.cursor()
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    if row:
        print(f'Versión de SQL Server: {row[0]}')
    else:
        print('Hay un error chamo')
except pyodbc.Error as e:
    print(Fore.GREEN + 'Error :c' + Style.RESET_ALL)

def espanolizar(text):
    translator = Translator()
    idioma = translator.detect(text).lang
    notengoenie = translator.translate(text, src=idioma, dest='es')
    return notengoenie.text

@app.route('/')
def index():
    return render_template('index.html', titulo=titulo, icon=icon)

@app.route('/crud', methods=['GET'])
def consultartablas():
    palabrita = ""
    tablaselect = request.args.get('tablaselect', '')
    flash("Aqui se mostraran las alertas :)")
    try:
        #con esta consulta obtenemos el nombre de las tablas de la db
        cursor.execute("""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG = ?
            ORDER BY TABLE_NAME ASC;
        """, (database,))
        tablas = [row.TABLE_NAME for row in cursor.fetchall()]
        #con esta consulta obtenemos valores de las tablas y los guardamos en variables para usarlas qui y en el html con jinja
        if tablaselect:
            cursor.execute('SELECT * FROM ' + tablaselect)
            rows = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
        else:
            rows = []
            column_names = []
        return render_template('crud.html', titulo=titulo, tablas=tablas, tablaselect=tablaselect, rows=rows, column_names=column_names, palabrita=palabrita, icon=icon)
    except pyodbc.Error as e:
        error_message = f"Error al recuperar las tablas: {espanolizar(str(e))}"
        return render_template('error.html', error_message=error_message)

@app.route('/remove', methods=['GET'])
#con este metodo borramos campos , obteniendo el id con el boton de el campo solicitado
def remove():
    registro_id = request.args.get('id')
    tablaname = request.args.get('tablaselect')
    if registro_id and tablaname:
        try:
            cursor.execute(f"DELETE FROM {tablaname} WHERE id = ?", (registro_id,))
            connection.commit()
            flash(f'Se ha eliminado el registro con ID {registro_id} de la tabla {tablaname} correctamente. :D')
        except pyodbc.Error as e:
            error_message = f"Error al eliminar el registro: {espanolizar(str(e))}"
            flash(error_message, 'error' + " :c")
    return redirect('crud')

@app.route('/aggreg', methods=['POST'])
#lo mismo que el de borrar pero en ves de borrar , agrega campos, dependiendo la tabla donde se ubique
def aggreg():
    tabla = request.form.get('tablaselect')
    if not tabla:
        flash('No hay tablas seleccionadas :(')
        return redirect('crud')
    cursor.execute(f"SELECT * FROM {tabla} WHERE 1=0")
    column_names = [column[0] for column in cursor.description]
    valores = [request.form.get(nombre) for nombre in column_names[1:]]
    if len(column_names[1:]) != len(valores):
        flash('Error: La cantidad de valores no coincide con la cantidad de columnas.')
        return redirect('crud')
    if any(valores):
        try:
            insert_query = f"INSERT INTO {tabla} ({', '.join(column_names[1:])}) VALUES ({', '.join(['?'] * len(column_names[1:]))})"
            cursor.execute(insert_query, valores)
            connection.commit()
            flash('Registro exitoso')
            return redirect('crud')
        except pyodbc.Error as e:
            flash(f"Error al insertar registro :c {espanolizar(str(e))}")
            return redirect('crud')
    else:
        flash("No has introducido algun valor para los registros :c")
        return redirect('crud')

@app.route('/edit', methods=['GET'])

def editar():
    id = request.args.get('id')
    tabla = request.args.get('tablaselect')
    cursor.execute(f"SELECT * FROM {tabla} WHERE 1=0")
    cursor.execute(f"SELECT * FROM {tabla} WHERE id = ?", (id,))
    campo = cursor.fetchone()
    if campo:
        column_names = [description[0] for description in cursor.description]
        campod = {column_names[i]: campo[i] for i in range(len(column_names))}
    return render_template('editar.html', campod=campod, tablaselect=tabla)

@app.route('/update', methods=['POST'])
#este metodo fue el mas complicado , requiere obtener el id de el campo que estas solicitando mediante html
#para despues buscar esa id y darnos los datos de ese registo y mostrarlos como datos "editables" o texto
#en imputs de html , para que el usuario los edite segun el quiera
#de hecho lo hice 2 veces , pero ya no lo quite porque podria fallar el programa
def update():
    tabla = request.form.get('tablaselect')
    registro_id = request.form.get('id')
    cursor.execute(f"SELECT * FROM {tabla} WHERE id = ?", (registro_id,))
    column_names = [column[0] for column in cursor.description]
    valores = [request.form.get(nombre) for nombre in column_names]
    #aqui uniremos o obtendremos los datos de tabla en un formato editable guardandolo en un arreglo me parece, 
    #ya que si los obtenemos asi como salen, saldran  algo parecido a esto: ("id",1,"id_persona",1,"nombre",pablo) 
    #y queremos que se vea asi: (1,1,pablo) obviamente en diferentes campos para que el usuariio sepa que columna esta editando.
    update_query = f"UPDATE {tabla} SET {', '.join([f'{column_names[i]} = ?' for i in range(1, len(column_names))])} WHERE id = ?"
    valores.append(registro_id)
    try:
        #en esta parte le decimos que "omita" de alguina forma el 1 valor del arreglo ya que el valor 1 de todas las tablas es el id
        # y si el usuario edita el id, en primera va arrojar error asi que lo mejor seria quitarlo (pero no supe xd) o inhabilitarlo
        #como aqui.
        cursor.execute(update_query, valores[1:])
        connection.commit()
        flash('Registro actualizado correctamente')
        flash(valores)
        return redirect('crud')
    except pyodbc.Error as e:
        flash(f"Error al actualizar registro :c {espanolizar(str(e))}")
    flash(valores)
    return redirect('crud')




#template /registro
@app.route('/registro')
def registro():
    return render_template('registro.html', titulo=titulo, icon=icon)


#metodo para guardar los registros de usuarios en la DB
@app.route('/guardar_registro', methods=['GET', 'POST'])
def sRegistro():
    if request.method == 'POST':
        name = request.form.get('nombre')
        lnamep = request.form.get('apellidosp')
        lnamem = request.form.get('apellidosm')
        email = request.form.get('correo')
        passw = request.form.get('contrasena')
        testpassw = request.form.get('confirmar_contrasena')

        if passw != testpassw:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('registro.html', name=name, lnamep=lnamep,
                                   lnamem=lnamem, email=email)

        try:
            # Verificar si el correo ya existe
            cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE correo = ?", email)
            count = cursor.fetchone()[0]

            if count > 0:
                flash('El correo electrónico ya está registrado', 'error')
                return redirect(url_for('registro'))

            # Ejecutar el procedimiento almacenado para insertar el nuevo usuario
            cursor.execute("EXEC sp_ingresarUsuario @nombre=?, @apellidop=?, @apellidom=?, @correo=?, @password=?",
                           name, lnamep, lnamem, email, passw)
            connection.commit()
            flash('Registro exitoso', 'success')
        except pyodbc.Error as e:
            flash(f'Error en el registro: {str(e)}', 'error')

        return redirect(url_for('registro'))


#template -login
@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html', titulo=titulo, icon=icon)
#function login
@app.route('/ingresar',methods=['GET','POST'])
def ingresar():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('contrasena')

    query='''
        SELECT id_tipouser from Usuarios
        where correo=? and passwrd=?
            '''

    cursor.execute(query, (correo, password))

    ingresouser = cursor.fetchone()



    if ingresouser:
        tipouser = ingresouser[0]
        return render_template('home.html',tipouser=tipouser)

    else:

        flash ('Correo o contraseña incorrectos')


    return redirect('login')


#template /singup_enterprice
@app.route('/signup_enterprice')
def signup_enterprice():
    return render_template('signup_enterprice.html', titulo=titulo, icon=icon)




#Template registro de la empresa
@app.route('/registro_enterprice')
def registro_enterprice():
    return render_template('registro_enterprice.html', titulo=titulo, icon=icon)

#Funcion para registrar la empresa en la DB (NO ESTA TERMINADO)
@app.route('/empresaGuardarRegistro', methods=['GET', 'POST'])
def empresaGuardarRegistro():
    if request.method == 'POST':
        name = request.form.get('nombre')
        lnamep = request.form.get('apellidosp')
        lnamem = request.form.get('apellidosm')
        email = request.form.get('correo')
        passw = request.form.get('contrasena')
        testpassw = request.form.get('confirmar_contrasena')

        if passw != testpassw:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('registro'))

        try:
            # Verificar si el correo ya existe
            cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE correo = ?", email)
            count = cursor.fetchone()[0]

            if count > 0:
                flash('El correo electrónico ya está registrado', 'error')
                return redirect(url_for('registro'))

            # Ejecutar el procedimiento almacenado para insertar el nuevo usuario
            cursor.execute("EXEC sp_ingresarUsuario @nombre=?, @apellidop=?, @apellidom=?, @correo=?, @password=?",
                           name, lnamep, lnamem, email, passw)
            connection.commit()
            flash('Registro exitoso', 'success')
        except pyodbc.Error as e:
            flash(f'Error en el registro: {str(e)}', 'error')
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('registro'))


#Fin de la funcion








#template - about
@app.route('/about')
def about():
    return render_template('about.html', titulo=titulo, icon=icon)

#template - Home
@app.route('/Home')
def Home():
    return render_template('Home.html', titulo=titulo, icon=icon)

@app.route('/Convocatorias')
def Convocatorias():
    return render_template('convocatorias.html', titulo=titulo, icon=icon)

@app.route('/registro_convocatoria')
def registro_convocatoria():
    return render_template('registro_convocatorias.html', titulo=titulo, icon=icon)

if __name__ == '__main__':
    app.run(debug=True)
