#Aqui podremos poner la parte logica de nuestro crud del pi
#como links a otros html , getters , sertters cookies
#incluso la conexion con la base de datos
import base64

import os

#ESTE ES EL CORAZON de la applicacion web (por asi decirlo)
#Los documentos html adjuntos unicamente se utilizara el de crud, index y editar, los otros
#son "plantillas" que estan colocadas para usarse en algun momento
#Universal Crud :D


#para las librerias usamos translate para traducir los mensajes de eror que mandaran los try y catch desde sql
#colorama lo usamos para cambiar el color de las letritas de la consola
from colorama import init, Fore, Style
from googletrans import Translator
import pyodbc
from datetime import date,datetime
from flask import Flask, render_template, request, flash, redirect, session, url_for, jsonify, send_file
import socket
import sqlite3
import io
from PIL import Image


#establece la conexion con sql server
init()

app = Flask(__name__)

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
    print(Fore.GREEN + 'Error :c, intentando con docker' + Style.RESET_ALL)

    try:
        server = 'sqlserver'  # Cambia esto a tu servidor SQL Server
        database = 'TerraForce'
        username = 'sa'  # Cambia esto a tu nombre de usuario de SQL Server
        password = '1@pOrf4vorD10$'  # Cambia esto a tu contraseña de SQL Server
        driver = '{ODBC Driver 17 for SQL Server}'  # Asegúrate de que este driver esté instalado

        if database == 'TacoLovers':
            icon = "../static/images/taco.ico"
        elif database == 'TerraForce':
            icon = "../static/images/logoterra1.ico"
        else:
            icon = "../static/images/demon.ico"

        connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        connection = pyodbc.connect(connection_string)

        titulo = database
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

    except pyodbc.Error as e:
        print(Fore.GREEN + 'Error , No se conecto con la db local ni la de docker :,c' + Style.RESET_ALL)

finally:
    cursor.close()

def espanolizar(text):
    translator = Translator()
    idioma = translator.detect(text).lang
    notengoenie = translator.translate(text, src=idioma, dest='es')
    return notengoenie.text

@app.route('/')
def index():
    cursor = connection.cursor()
    id = session.get('id_user')
    tipouser = session.get('tipo_user')
    usuario_logeado = False

    results = []
    nombre = ""

    if tipouser == 3:
        usuario_logeado = True
        cursor.execute("""
            SELECT e.nombre FROM usuarios AS u
            JOIN Empresas AS e ON u.id_empresa = e.id
            WHERE u.id = ?
        """, (id,))
        nombre = cursor.fetchone()[0]

        cursor.execute("SELECT id_empresa FROM Usuarios WHERE id = ?", (id,))
        idempresa = cursor.fetchone()[0]

        cursor.execute("""
            SELECT c.id, c.titulo, c.requisitos, c.descripcion,
                   c.usuarios_registrados, c.limite_usuarios, c.fecha_inicio,
                   c.fecha_final, e.nombre AS empresa_nombre, es.nombre AS estatus_nombre, t.tematica
            FROM Convocatorias AS c
            JOIN Empresas AS e ON e.id = c.id_empresa
            JOIN Estatus AS es ON es.id = c.id_estatus
            JOIN Tematicas AS t ON t.id = c.id_tematica
            WHERE c.id_empresa = ?
        """, (idempresa,))
        results = cursor.fetchall()

    elif id and tipouser:
        usuario_logeado = True
        cursor.execute("""
        SELECT id_persona from Usuarios where id = ? 
        """, (id,))
        id_persona = cursor.fetchone()
        id_persona = id_persona[0]
        cursor.execute("""
        select nombre from Personas where id = ?
        """, (id_persona,))
        nombre = cursor.fetchone()[0]

        query = '''
        SELECT c.id, c.titulo, c.requisitos, c.imagen, c.usuarios_registrados,
        c.limite_usuarios, c.fecha_inicio, c.fecha_final, e.nombre AS empresa_nombre
        FROM Registros as r
        JOIN Convocatorias as c ON r.id_convocatoria = c.id
        JOIN Empresas AS e on c.id_empresa = e.id
        JOIN Estatus AS es on c.id_estatus = es.id
        WHERE id_voluntario = ?;
        '''
        cursor.execute(query, (id,))
        results = cursor.fetchall()

    cursor.close()

    return render_template('index.html', results=results, titulo=titulo, icon=icon, nombre=nombre,
                           usuario_logeado=usuario_logeado, tipouser=tipouser)



@app.route('/crud', methods=['GET'])
def consultartablas():

    if 'id_user' not in session:
        return redirect(url_for('login'))

    id = session.get('id_user')
    tipouser = session.get('tipo_user')

    if tipouser in [2, 3]:
        return redirect(url_for('errorpage'))

    usuario_logeado = False

    cursor = connection.cursor()
    palabrita = ""
    tablaselect = request.args.get('tablaselect', '')
    flash("Aqui se mostraran las alertas :)")

    results = []
    nombre = ""

    try:
        if id and tipouser:
            usuario_logeado = True
            cursor.execute("""
            SELECT id_persona from Usuarios where id = ? 
            """, (id,))
            id_persona = cursor.fetchone()
            id_persona = id_persona[0]
            cursor.execute("""
            select nombre from Personas where id = ?
            """, (id_persona,))
            nombre = cursor.fetchone()[0]

            query = '''
            SELECT c.id, c.titulo, c.requisitos, c.imagen, c.usuarios_registrados,
            c.limite_usuarios, c.fecha_inicio, c.fecha_final, e.nombre AS empresa_nombre
            FROM Registros as r
            JOIN Convocatorias as c ON r.id_convocatoria = c.id
            JOIN Empresas AS e on c.id_empresa = e.id
            JOIN Estatus AS es on c.id_estatus = es.id
            WHERE id_voluntario = ?;
            '''
            cursor.execute(query, (id,))
            results = cursor.fetchall()

        # Consultar nombres de las tablas de la base de datos
        cursor.execute("""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG = ?
            ORDER BY TABLE_NAME ASC;
        """, (database,))
        tablas = [row.TABLE_NAME for row in cursor.fetchall()]

        # Obtener datos de la tabla seleccionada
        if tablaselect:
            cursor.execute(f'SELECT * FROM {tablaselect}')
            rows = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
        else:
            rows = []
            column_names = []

        return render_template('crud.html', titulo=titulo, tablas=tablas, tablaselect=tablaselect, rows=rows,
                               column_names=column_names, palabrita=palabrita, icon=icon, results=results,
                               nombre=nombre, usuario_logeado=usuario_logeado, tipouser=tipouser)
    except pyodbc.Error as e:
        error_message = f"Error al recuperar las tablas: {espanolizar(str(e))}"
        return render_template('error.html', error_message=error_message)
    finally:
        cursor.close()


@app.route('/remove', methods=['GET'])
#con este metodo borramos campos , obteniendo el id con el boton de el campo solicitado
def remove():
    cursor = connection.cursor()
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
        finally:
            cursor.close()
    return redirect('crud')


@app.route('/aggreg', methods=['POST'])
#lo mismo que el de borrar pero en ves de borrar , agrega campos, dependiendo la tabla donde se ubique
def aggreg():
    cursor = connection.cursor()
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
        finally:
            cursor.close()
    else:
        flash("No has introducido algun valor para los registros :c")
        return redirect('crud')

@app.route('/edit', methods=['GET'])

def editar():
    cursor = connection.cursor()
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
    cursor = connection.cursor()
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
        flash('Registro actualizado correctamente',valores)
        return redirect('crud')
    except pyodbc.Error as e:
        flash(f"Error al actualizar registro :c {espanolizar(str(e))}",valores)
    finally:
        cursor.close()

    return redirect('crud')



#template /registro
@app.route('/registro')
def registro():
    return render_template('registro.html', titulo=titulo, icon=icon)


#metodo para guardar los registros de usuarios en la DB
@app.route('/guardar_registro', methods=['GET', 'POST'])
def sRegistro():
    if request.method == 'POST':
        cursor = connection.cursor()
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
        finally:
            cursor.close()
        return redirect(url_for('registro'))


#template -login
@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html', titulo=titulo, icon=icon)
#function login
@app.route('/ingresar',methods=['GET','POST'])
def ingresar():
    cursor = connection.cursor()
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('contrasena')


    query='''
        SELECT id from Usuarios
        where correo=? and passwrd=?
            '''

    cursor.execute(query, (correo, password))
    id = cursor.fetchone()


    if id:
        id_user = id[0]
        cursor.execute("""
                SELECT id_tipouser from Usuarios
                where id = ?
                """,(id_user,))
        tipo_user = cursor.fetchone()

        if tipo_user:
            tipo_user = tipo_user[0]
            session['tipo_user']=tipo_user
            session['id_user']=id_user

            if tipo_user == 3:
                #Primero se cierra el cursor y luego te redirige
                cursor.close()
                return redirect(url_for('HomeEmpresa'))
            else:
                cursor.close()
                return redirect(url_for('Home'))

    else:
        flash('Correo o contraseña incorrectos','danger')
        cursor.close()
        return render_template('login.html')


#template /singup_enterprice
@app.route('/signup_enterprice')
def signup_enterprice():
    return render_template('signup_enterprice.html', titulo=titulo, icon=icon)


#Template registro de la empresa

@app.route('/registro_enterprice')
def registro_enterprice():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, nombre FROM Estados")
        estados = cursor.fetchall()
        return render_template('registro_enterprice.html', estados=estados)
    except pyodbc.Error as e:
        flash(f'Error al cargar los datos: {str(e)}', 'error','danger')
        return redirect(url_for('index'))
    finally:
        cursor.close()

@app.route('/obtener_municipios', methods=['GET'])
def obtener_municipios():
    estado_id = request.args.get('estado_id')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, nombre FROM Municipios WHERE id_estado = ?", estado_id)
        municipios = cursor.fetchall()
        return jsonify([{'id': municipio.id, 'nombre': municipio.nombre} for municipio in municipios])
    except pyodbc.Error as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()

@app.route('/obtener_colonias', methods=['GET'])
def obtener_colonias():
    cursor = connection.cursor()
    municipio_id = request.args.get('municipio_id')
    try:
        cursor.execute("SELECT id, nombre FROM Colonias WHERE id_municipio = ?", municipio_id)
        colonias = cursor.fetchall()
        return jsonify([{'id': colonia.id, 'nombre': colonia.nombre} for colonia in colonias])
    except pyodbc.Error as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()

@app.route('/obtener_calles', methods=['GET'])
def obtener_calles():
    cursor = connection.cursor()
    colonia_id = request.args.get('colonia_id')
    try:
        cursor.execute("SELECT id, nombre FROM Calles WHERE id_colonia = ?", colonia_id)
        calles = cursor.fetchall()
        return jsonify([{'id': calle.id, 'nombre': calle.nombre} for calle in calles])
    except pyodbc.Error as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()




#--------------------------------------------------------------------------------------------------
#Funcion para registrar la empresa en la DB (NO ESTA TERMINADO)
@app.route('/empresaGuardarRegistro', methods=['GET', 'POST'])
def empresaGuardarRegistro():
    if request.method == 'POST':

        cursor = connection.cursor()
        name = request.form.get('nombre')
        rfc = request.form.get('RFC')
        email = request.form.get('correo')
        telefono = request.form.get('telefono')
        passw = request.form.get('contrasena')
        testpassw = request.form.get('confirmar_contrasena')
        estado = request.form.get('estado')
        municipio = request.form.get('municipio')
        colonia = request.form.get('colonia')
        calle = request.form.get('calle')

        if passw != testpassw:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('registro_enterprice'))

        try:
            # Verificar si el correo ya existe
            cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE correo = ?", email)
            email_count = cursor.fetchone()[0]

            if email_count > 0:
                flash('El correo electrónico ya está registrado', 'error')
                return redirect(url_for('registro_enterprice'))

            # Verificar si el RFC ya existe
            cursor.execute("SELECT COUNT(*) FROM Empresas WHERE RFC = ?", rfc)
            rfc_count = cursor.fetchone()[0]

            if rfc_count > 0:
                flash('El RFC ya está registrado', 'error')
                return redirect(url_for('registro_enterprice'))

            # Ejecutar el procedimiento almacenado para insertar el nuevo usuario
            cursor.execute("EXEC sp_ingresarEmpresa @nombre= ?, @RFC= ?, @correo= ?, @password= ?, @fone= ?, @estado= ?, @municipio=?, @colonia= ?, @calle= ?;",
                           name, rfc, email, passw, telefono, estado, municipio, colonia, calle)

            connection.commit()
            flash('Registro exitoso', 'success')
        except pyodbc.Error as e:
            flash(f'Error en el registro: {str(e)}', 'error')
            return redirect(url_for('registro_enterprice'))
        finally:
            cursor.close()

        return redirect(url_for('registro_enterprice'))

    return render_template('registro_enterprice.html')


#Fin de la funcion


#--------------------------------------------------------------------------------------------------





#template - about
@app.route('/about')
def about():
    cursor = connection.cursor()
    id = session.get('id_user')
    tipouser = session.get('tipo_user')
    usuario_logeado = False

    results = []
    nombre = ""

    if tipouser == 3:
        usuario_logeado = True
        cursor.execute("""
            SELECT e.nombre FROM usuarios AS u
            JOIN Empresas AS e ON u.id_empresa = e.id
            WHERE u.id = ?
        """, (id,))
        nombre = cursor.fetchone()[0]

        cursor.execute("SELECT id_empresa FROM Usuarios WHERE id = ?", (id,))
        idempresa = cursor.fetchone()[0]

        cursor.execute("""
            SELECT c.id, c.titulo, c.requisitos, c.descripcion,
                   c.usuarios_registrados, c.limite_usuarios, c.fecha_inicio,
                   c.fecha_final, e.nombre AS empresa_nombre, es.nombre AS estatus_nombre, t.tematica
            FROM Convocatorias AS c
            JOIN Empresas AS e ON e.id = c.id_empresa
            JOIN Estatus AS es ON es.id = c.id_estatus
            JOIN Tematicas AS t ON t.id = c.id_tematica
            WHERE c.id_empresa = ?
        """, (idempresa,))
        results = cursor.fetchall()

    elif id and tipouser:
        usuario_logeado = True
        cursor.execute("""
        SELECT id_persona from Usuarios where id = ? 
        """, (id,))
        id_persona = cursor.fetchone()
        id_persona = id_persona[0]
        cursor.execute("""
        select nombre from Personas where id = ?
        """, (id_persona,))
        nombre = cursor.fetchone()[0]

        query = '''
        SELECT c.id, c.titulo, c.requisitos, c.imagen, c.usuarios_registrados,
        c.limite_usuarios, c.fecha_inicio, c.fecha_final, e.nombre AS empresa_nombre
        FROM Registros as r
        JOIN Convocatorias as c ON r.id_convocatoria = c.id
        JOIN Empresas AS e on c.id_empresa = e.id
        JOIN Estatus AS es on c.id_estatus = es.id
        WHERE id_voluntario = ?;
        '''
        cursor.execute(query, (id,))
        results = cursor.fetchall()

    cursor.close()

    return render_template('about.html', results=results, titulo=titulo, icon=icon, nombre=nombre,
                           usuario_logeado=usuario_logeado, tipouser=tipouser)



@app.route('/usermd', methods=['GET'])
def userhome():
    if 'id_user' in session:
        id = session.get('id_user')
        tipouser = session.get('tipo_user')
        usuario_logeado = False
        query = '''
        SELECT u.id, u.correo, u.passwrd, p.nombre, p.apellidop, p.apellidom
            FROM Usuarios as u
            JOIN Personas as p on u.id_persona = p.id
            WHERE u.id = ?
        '''

        cursor = connection.cursor()
        cursor.execute(query, (id,))
        user = cursor.fetchone()
        user_id = user[0]
        user_correo = user[1]
        user_pass = user[2]
        user_name = user[3]
        user_apellidop = user[4]
        user_apellidom = user[5]

        userdata = {
            'id': user_id,
            'correo': user_correo,
            'pass': user_pass,
            'name': user_name,
            'apellidop': user_apellidop,
            'apellidom': user_apellidom,
        }

        if tipouser == 3:
            cursor.close()
            return redirect(url_for('Home'))

        if id and tipouser:
            usuario_logeado = True
            cursor.execute("""
            SELECT id_persona from Usuarios where id = ? 
            """, (id,))
            id_persona = cursor.fetchone()
            id_persona = id_persona[0]
            cursor.execute("""
            select nombre from Personas where id = ?
            """, (id_persona,))
            nombre = cursor.fetchone()[0]
            cursor.close()
            return render_template('usermd.html', titulo=titulo, icon=icon, nombre=nombre,
                                   usuario_logeado=usuario_logeado, tipouser=tipouser, userdata=userdata)
        else:
            cursor.close()
            return render_template('usermd.html', titulo=titulo, icon=icon, usuario_logeado=usuario_logeado)
    return "No user in session", 401











#template - Home
@app.route('/Home')
def Home():
    #Esto para que, si no estas logueado, te mande al login en vez de al Home
    if 'id_user' not in session:
        return redirect(url_for('login'))

    cursor = connection.cursor()
    id = session.get('id_user')
    tipouser = session.get('tipo_user')
    usuario_logeado = False

    if tipouser == 3:
        cursor.close()
        return redirect(url_for('HomeEmpresa'))

    if id and tipouser:
        usuario_logeado = True
        cursor.execute("""
        SELECT id_persona from Usuarios where id = ? 
        """, (id,))
        id_persona = cursor.fetchone()
        id_persona = id_persona[0]
        cursor.execute("""
        select nombre from Personas where id = ?
        """, (id_persona,))
        nombre = cursor.fetchone()[0]

        query = '''
        SELECT c.id, c.titulo, c.requisitos, c.imagen, c.usuarios_registrados,
        c.limite_usuarios, c.fecha_inicio, c.fecha_final, e.nombre AS empresa_nombre
        FROM Registros as r
        JOIN Convocatorias as c ON r.id_convocatoria = c.id
        JOIN Empresas AS e on c.id_empresa = e.id
        JOIN Estatus AS es on c.id_estatus = es.id
        WHERE id_voluntario = ?;
        '''
        cursor.execute(query, (id))
        results = cursor.fetchall()
        ids = [row[0] for row in results]

        # Recuperar las imágenes para cada ID
        imagenes = {}
        for convocatoria_id in ids:
            cursor.execute("""
                       SELECT imagen, mime_type FROM Convocatorias 
                       WHERE id = ?
                   """, (convocatoria_id,))
            img = cursor.fetchone()

            if img:
                imagen, mime_type = img
                if imagen:
                    img_base64 = base64.b64encode(imagen).decode('utf-8')
                    imagenes[convocatoria_id] = {
                        'img_base64': img_base64,
                        'mime_type': mime_type
                    }

        cursor.close()

        print("Convocatorias:", results)
        print("IDs de Convocatorias:", ids)
        print("Imágenes:", imagenes)





        return render_template('Home.html', titulo=titulo, results=results, icon=icon, nombre=nombre,
                               usuario_logeado=usuario_logeado, tipouser=tipouser, imagenes=imagenes)

        cursor.close()


        return render_template('Home.html', results = results, titulo=titulo, icon=icon, nombre=nombre, usuario_logeado=usuario_logeado, tipouser=tipouser)
    else:
        cursor.close()
        return render_template('Home.html', titulo=titulo, icon=icon, usuario_logeado=usuario_logeado)



#Funcion para borrar una convocatoria
@app.route('/registrarse_convo/<int:idconvo>', methods=['GET'])
def registrarse_convo(idconvo):
    if 'id_user' in session:
        cursor = connection.cursor()
        try:
            cursor.execute('EXEC sp_RegistroConvoUser @iduser = ?, @idconvo = ?', (session['id_user'], idconvo))
            connection.commit()

            # Captura y procesa los mensajes de PRINT
            messages = []
            while cursor.messages:
                message = cursor.messages.pop(0)
                messages.append(message[1])

            # Verifica los mensajes y muestra flash adecuado
            if any('El usuario ya está registrado en esta convocatoria' in msg for msg in messages):
                flash('El usuario ya está registrado en esta convocatoria.', 'danger')
            elif any('No es posible registrar más usuarios en esta convocatoria' in msg for msg in messages):
                flash('No es posible registrar más usuarios en esta convocatoria.', 'danger')
            else:
                flash('Registro exitoso', 'success')
                for message in messages:
                    flash(message, 'info')

        except Exception as e:
            error_message = str(e)
            flash('Ocurrió un error al intentar registrarse: ' + error_message, 'danger')
        finally:
            cursor.close()
        return redirect(url_for('Convocatorias'))
    else:
        flash('Debes iniciar sesión para registrarte', 'danger')
        return redirect(url_for('login'))



@app.route('/verempre')
def verempre():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM V_DetallesEmpresa')
    results = cursor.fetchall()

    # Esto para que, si no estas logueado, te mande al login en vez de al Home
    if 'id_user' not in session:
        return redirect(url_for('login'))

    cursor = connection.cursor()
    id = session.get('id_user')
    tipouser = session.get('tipo_user')
    usuario_logeado = False

    if tipouser == 3:
        cursor.close()
        return redirect(url_for('HomeEmpresa'))

    if id and tipouser:
        usuario_logeado = True
        cursor.execute("""
           SELECT id_persona from Usuarios where id = ? 
           """, (id,))
        id_persona = cursor.fetchone()
        id_persona = id_persona[0]
        cursor.execute("""
           select nombre from Personas where id = ?
           """, (id_persona,))
        nombre = cursor.fetchone()[0]

        cursor.close()

    return render_template('UsuariosREG.html',titulo=titulo, results=results, icon=icon, nombre=nombre,
                               usuario_logeado=usuario_logeado, tipouser=tipouser)
    cursor.close()




@app.route('/verusers')
def veruserreg():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM V_DetallesUsuario')
    results = cursor.fetchall()

    # Esto para que, si no estas logueado, te mande al login en vez de al Home
    if 'id_user' not in session:
        return redirect(url_for('login'))

    cursor = connection.cursor()
    id = session.get('id_user')
    tipouser = session.get('tipo_user')
    usuario_logeado = False

    if tipouser == 3:
        cursor.close()
        return redirect(url_for('HomeEmpresa'))

    if id and tipouser:
        usuario_logeado = True
        cursor.execute("""
           SELECT id_persona from Usuarios where id = ? 
           """, (id,))
        id_persona = cursor.fetchone()
        id_persona = id_persona[0]
        cursor.execute("""
           select nombre from Personas where id = ?
           """, (id_persona,))
        nombre = cursor.fetchone()[0]

        cursor.close()

    return render_template('UsuariosREG.html',titulo=titulo, results=results, icon=icon, nombre=nombre,
                               usuario_logeado=usuario_logeado, tipouser=tipouser)
    cursor.close()



    #Funcion para salirse de una convocatoria
@app.route('/borrarConvo/<int:idconvo>', methods=['GET'])
def borrarConvo(idconvo):
    if 'id_user' in session:
        cursor = connection.cursor()
        try:
            cursor.execute('EXEC sp_borrarRegistroUser @iduser = ?, @idconvo = ?;', (session['id_user'], idconvo))
            connection.commit()
            flash('Saliste de la convocatoria', 'success')
        except Exception as e:
            error_message = str(e)
            flash('Ocurrió un error al intentar borrar la convocatoria: ' + error_message, 'danger')
        finally:
            cursor.close()
        return redirect(url_for('Home'))
    else:
        flash('Debes iniciar sesión para borrar una convocatoria', 'danger')
        return redirect(url_for('login'))



@app.route('/Convocatorias', methods=["GET"])
def Convocatorias():



    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM V_Convocatorias
    """)
    results = cursor.fetchall()


    ids = [row[0] for row in results]

    estatus= [row[5] for row in results]



    # Recuperar las imágenes para cada ID
    imagenes = {}
    for convocatoria_id in ids:
        cursor.execute("""
                    SELECT imagen, mime_type FROM Convocatorias 
                    WHERE id = ?
                """, (convocatoria_id,))
        img = cursor.fetchone()

        if img:
            imagen, mime_type = img
            if imagen:
                img_base64 = base64.b64encode(imagen).decode('utf-8')
                imagenes[convocatoria_id] = {
                    'img_base64': img_base64,
                    'mime_type': mime_type

                }

    cursor.close()

    #Esto para que, si no estas logueado, te mande al login en vez de al Home
    if 'id_user' not in session:
        return redirect(url_for('login'))

    cursor = connection.cursor()
    id = session.get('id_user')
    tipouser = session.get('tipo_user')
    usuario_logeado = False

    if tipouser == 3:
        cursor.close()
        return redirect(url_for('HomeEmpresa'))

    if id and tipouser:
        usuario_logeado = True
        cursor.execute("""
        SELECT id_persona from Usuarios where id = ? 
        """, (id,))
        id_persona = cursor.fetchone()
        id_persona = id_persona[0]
        cursor.execute("""
        select nombre from Personas where id = ?
        """, (id_persona,))
        nombre = cursor.fetchone()[0]



        cursor.close()

        print("Convocatorias:", results)
        print("IDs de Convocatorias:", ids)
        print("Imágenes:", imagenes)

        return render_template('convocatorias.html', titulo=titulo, results=results, icon=icon, nombre=nombre,
                               usuario_logeado=usuario_logeado, tipouser=tipouser, imagenes=imagenes,estatus=estatus)
    else:
        cursor.close()
        return render_template('convocatorias.html', results = results, titulo=titulo, icon=icon, usuario_logeado=usuario_logeado)



@app.route('/registro_convocatoria')
def registro_convocatoria():
    # Si no estás logueado, redirige al login
    if 'id_user' not in session:
        return redirect(url_for('login'))

    cursor = connection.cursor()
    id = session.get('id_user')
    tipouser = session.get('tipo_user')
    usuario_logeado = False
    titulo = "Mis Convocatorias"
    icon = url_for('static', filename='images/tlogo.png')

    if tipouser == 2:
        cursor.close()
        return redirect(url_for('errorpage'))

    # Para admin
    if tipouser == 1:
        usuario_logeado = True
        cursor.execute("SELECT id_persona FROM Usuarios WHERE id = ?", (id,))
        id_persona = cursor.fetchone()
        if id_persona:
            id_persona = id_persona[0]
            cursor.execute("SELECT nombre FROM Personas WHERE id = ?", (id_persona,))
            nombre = cursor.fetchone()[0]

            cursor.execute("""
                        SELECT tematica from Tematicas 
                        """)
            tematicas = cursor.fetchall()
            tematicas = [row[0] for row in tematicas]

            cursor.close()
            return render_template('crearConvo.html', titulo=titulo, icon=icon, nombre=nombre,
                                   usuario_logeado=usuario_logeado, tipouser=tipouser,tematicas=tematicas)



        else:
            cursor.close()
            return redirect(url_for('errorpage'))

    # Para empresas
    if id and tipouser:
        usuario_logeado = True
        cursor.execute("""
                SELECT e.nombre FROM usuarios AS u
                JOIN Empresas AS e ON u.id_empresa = e.id
                WHERE u.id = ?
            """, (id,))
        nombre = cursor.fetchone()[0]

        cursor.execute("SELECT id_empresa FROM Usuarios WHERE id = ?", (id,))
        idempresa = cursor.fetchone()[0]

        cursor.execute("""
                SELECT c.id, c.titulo, c.requisitos, c.descripcion,
                       c.usuarios_registrados, c.limite_usuarios, c.fecha_inicio,
                       c.fecha_final, e.nombre AS empresa_nombre, es.nombre AS estatus_nombre, t.tematica
                FROM Convocatorias AS c
                JOIN Empresas AS e ON e.id = c.id_empresa
                JOIN Estatus AS es ON es.id = c.id_estatus
                JOIN Tematicas AS t ON t.id = c.id_tematica
                WHERE c.id_empresa = ?
            """, (idempresa,))
        results = cursor.fetchall()


        cursor.execute("""
                               SELECT tematica from Tematicas 
                               """)
        tematicas = cursor.fetchall()
        tematicas = [row[0] for row in tematicas]

        cursor.close()

        return render_template('crearConvo.html', titulo=titulo, results=results, icon=icon, nombre=nombre,
                               usuario_logeado=usuario_logeado, tipouser=tipouser,tematicas=tematicas)
    else:
        return render_template('crearConvo.html', titulo=titulo, icon=icon, usuario_logeado=usuario_logeado,
                               tipouser=tipouser)
    # Palas empresas
    if id and tipouser:
        usuario_logeado = True
        cursor.execute("""
            select e.nombre from usuarios as u
            join Empresas as e on u.id_empresa = e.id
            WHERE u.id=?
            """, (id,))
        nombre = cursor.fetchone()[0]
        cursor.close()

        return render_template('HomeEmpresa.html', titulo=titulo, icon=icon, nombre=nombre,
                               usuario_logeado=usuario_logeado, tipouser=tipouser)
    else:
        return render_template('HomeEmpresa.html', titulo=titulo, icon=icon, usuario_logeado=usuario_logeado,
                               tipouser=tipouser)


 # def tipoimagen(nombrearch):
 #     return '.' in nombrearch and \
 #            nombrearch.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/registrar_convo', methods=['POST'])
def registrar_convo():



    cursor = connection.cursor()
    tituloconv = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    requisitos = request.form.get('requisitos')
    fechainicio = request.form.get('fecha_inicio')
    fechacierre = request.form.get('fecha_cierre')
    tematicas = request.form.get('tematicas')
    vacantes =  request.form.get('vacantes')
    imagen = request.files.get('imagen')





    id_user = session.get('id_user')
    tipo_user = session.get('tipo_user')


    if imagen:
        nombreima = imagen.filename
        nombreseparado,tipoima = os.path.splitext(nombreima)
        nombresinpunto=tipoima.lstrip('.').upper()
        if nombresinpunto=='JPG':
            nombresinpunto='JPEG'
        imagenbin = imagen.read()
        format_img=nombresinpunto

    else:
        imagenbin = None

    try:
        if not id_user:
            flash('Usuario no autenticado','danger')
            return redirect('registro_convocatoria')



        if tituloconv and requisitos and fechainicio and fechacierre and vacantes and tematicas and descripcion:

            fechainicio_d=datetime.strptime(fechainicio, '%Y-%m-%d')
            fechafin_d = datetime.strptime(fechacierre, '%Y-%m-%d')
            fechafinver = fechafin_d.date()
            fechainiciover = fechainicio_d.date()

            if fechainiciover == fechafinver:
                flash('La fecha de inicio y de termino no pueden ser iguales')
                return redirect('registro_convocatoria')

            if fechainiciover > fechafinver:
                flash('La fecha de de cierre , no puede ser anterior a la de inicio')
                return redirect('registro_convocatoria')

            if vacantes:
                vacantes = int(vacantes)
                if vacantes < 10 or vacantes < 0:
                    flash('El número de vacantes mínimo es de 10')
                    return redirect('registro_convocatoria')



            if imagenbin and format_img:

                try:
                    image = Image.open(io.BytesIO(imagenbin))
                    img_io = io.BytesIO()
                    image.save(img_io, format=format_img)
                    img_io.seek(0)
                    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
                    mime_type = f'image/{format_img.lower()}'
                    # tamanoima=len(img_base64)
                except Exception as e:
                    flash(f'Ocurrrio un error al procesar la imagen {str(e)}', 'danger')
                    return redirect('registro_convocatoria')
            else:
                img_base64=None
                mime_type = None







            cursor.execute("""
                EXEC sp_FIND_id_empresa ?
            """, id_user)
            id_empresa_row = cursor.fetchone()
            if not id_empresa_row:
                flash(f'No se encontró la empresa para el usuario dado {id_empresa_row,id_user} hola')
                return redirect('registro_convocatoria')

            id_empresa = id_empresa_row[0]


            cursor.execute("""
                EXEC sp_nombre_empresa ?
            """, id_empresa)
            empresa_row = cursor.fetchone()
            if not empresa_row:
                flash(f'No se encontró el nombre de la empresa para el ID dado {id_user,id_empresa} Hola :c','danger')
                return redirect('registro_convocatoria')

            empresa = empresa_row[0]

            return render_template('preview.html',
                                   tituloconv=tituloconv,
                                   requisitos=requisitos,
                                   fechainicio=fechainicio,
                                   fechacierre=fechacierre,
                                   vacantes=vacantes,
                                   imagen=imagenbin,
                                   tematicas=tematicas,
                                   empresa=empresa,
                                   tipo_user=tipo_user
                                   ,descripcion=descripcion,
                                   img_base64=img_base64,
                                   mime_type=mime_type,
                                   id_user=id_user,
                                   id_empresa=id_empresa,
                                   imagenbin=imagenbin,
                                   format_img=format_img)
                                   # tamanoima=tamanoima)
        else:
            flash(f'Por favor rellena todos los datos solicitados para el registro {tituloconv,requisitos,fechainicio,fechacierre,vacantes,tematicas,descripcion}','danger')
            return redirect('registro_convocatoria')

    except Exception as e:
        flash(f'Error: {str(e)}','danger')
        return redirect('registro_convocatoria')
    finally:
        cursor.close()



@app.route('/post', methods=['POST'])
def upload():
    cursor = connection.cursor()
    tituloconv = str(request.form.get('tituloconv'))
    descripcion = request.form.get('descripcion')
    requisitos = request.form.get('requisitos')
    fechainicio = request.form.get('fechainicio')
    fechacierre = request.form.get('fechacierre')
    tematicas = request.form.get('tematicas')
    vacantes = int(request.form.get('vacantes'))
    imagenbin = request.form.get('imagenbin')
    id_empresa = int(request.form.get('id_empresa'))
    format_img = request.form.get('format_img')
    format_img = f'image/{format_img.lower()}'

    if imagenbin:

        img_data = base64.b64decode(imagenbin)
    else:
        img_data = None


    cursor.execute("""
    exec sp_tematica_id ?
    """,tematicas)
    id_tematica=cursor.fetchone()[0]

    if id_tematica and tituloconv and descripcion and requisitos and fechainicio and fechacierre and vacantes and id_empresa and img_data and format_img:
        try :
            cursor.execute("""
                exec sp_post_publicacion ?,?,?,?,?,?,?,?,?,?
                """,tituloconv,descripcion,requisitos,fechainicio,id_empresa,id_tematica,
                           img_data,vacantes,fechacierre,format_img)




            flash(f'Publicacion creada :D ','succes')
            return redirect('registro_convocatoria')
        except Exception as e:
            flash(f'Error: {str(e)}','danger')
            redirect('preview')

    if id_tematica and tituloconv and descripcion and requisitos and fechainicio and fechacierre and vacantes and id_empresa :
            try:
                cursor.execute("""
                    exec sp_post_publicacion ?,?,?,?,?,?,?,?,?,?
                    """, tituloconv, descripcion, requisitos, fechainicio, id_empresa, id_tematica,
                               'Null', vacantes, fechacierre,'Null')

                flash('Publicacion creada :D, pero sin imagen', 'succes')
                return redirect('registro_convocatoria')
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')
                redirect('preview')

    else:
        flash(f'Hay algun error con un campo {tituloconv,descripcion,requisitos,fechainicio,id_empresa,id_tematica,vacantes,fechacierre,imagenbin}','error')
        return render_template('preview.html',
                               tituloconv=tituloconv,
                               requisitos=requisitos,
                               fechainicio=fechainicio,
                               fechacierre=fechacierre,
                               vacantes=vacantes,
                               tematicas=tematicas,
                               descripcion=descripcion,
                               id_empresa=id_empresa,
                               img_data=img_data
                               )

    flash('Error ?')
    return render_template('preview.html')


@app.route('/HomeEmpresa')
def HomeEmpresa():
    # Si no estás logueado, redirige al login
    if 'id_user' not in session:
        return redirect(url_for('login'))

    cursor = connection.cursor()
    id = session.get('id_user')
    tipouser = session.get('tipo_user')
    usuario_logeado = False
    titulo = "Mis Convocatorias"
    icon = url_for('static', filename='images/tlogo.png')

    if tipouser == 2:
        cursor.close()
        return redirect(url_for('errorpage'))

    if tipouser == 1:
        usuario_logeado = True
        cursor.execute("SELECT id_persona FROM Usuarios WHERE id = ?", (id,))
        id_persona = cursor.fetchone()
        if id_persona:
            id_persona = id_persona[0]
            cursor.execute("SELECT nombre FROM Personas WHERE id = ?", (id_persona,))
            nombre = cursor.fetchone()[0]
            cursor.close()
            return render_template('HomeEmpresa.html', titulo=titulo, icon=icon, nombre=nombre,
                                   usuario_logeado=usuario_logeado, tipouser=tipouser)
        else:
            cursor.close()
            return redirect(url_for('errorpage'))

    if id and tipouser:
        usuario_logeado = True
        # Recupera el nombre de la empresa
        cursor.execute("""
            SELECT e.nombre FROM usuarios AS u
            JOIN Empresas AS e ON u.id_empresa = e.id
            WHERE u.id = ?
        """, (id,))
        nombre = cursor.fetchone()[0]

        # Recupera la ID de la empresa
        cursor.execute("SELECT id_empresa FROM Usuarios WHERE id = ?", (id,))
        idempresa = cursor.fetchone()[0]

        # Recupera las convocatorias
        cursor.execute("""
            SELECT c.id, c.titulo, c.requisitos, c.descripcion,
                   c.usuarios_registrados, c.limite_usuarios, c.fecha_inicio,
                   c.fecha_final, e.nombre AS empresa_nombre, es.nombre AS estatus_nombre, t.tematica
            FROM Convocatorias AS c
            JOIN Empresas AS e ON e.id = c.id_empresa
            JOIN Estatus AS es ON es.id = c.id_estatus
            JOIN Tematicas AS t ON t.id = c.id_tematica
            WHERE c.id_empresa = ?
        """, (idempresa,))
        results = cursor.fetchall()

        ids = [row[0] for row in results]

        # Recuperar las imágenes para cada ID
        imagenes = {}
        for convocatoria_id in ids:
            cursor.execute("""
                SELECT imagen, mime_type FROM Convocatorias 
                WHERE id = ?
            """, (convocatoria_id,))
            img = cursor.fetchone()

            if img:
                imagen, mime_type = img
                if imagen:
                    img_base64 = base64.b64encode(imagen).decode('utf-8')
                    imagenes[convocatoria_id] = {
                        'img_base64': img_base64,
                        'mime_type': mime_type
                    }

        cursor.close()

        print("Convocatorias:", results)
        print("IDs de Convocatorias:", ids)
        print("Imágenes:", imagenes)

        return render_template('HomeEmpresa.html', titulo=titulo, results=results, icon=icon, nombre=nombre,
                               usuario_logeado=usuario_logeado, tipouser=tipouser,imagenes=imagenes)

    # Manejo para cuando `id` o `tipouser` no están presentes
    cursor.close()
    return render_template('HomeEmpresa.html', titulo=titulo, icon=icon, usuario_logeado=usuario_logeado,
                           tipouser=tipouser)
#Funcion para mostrar los usuarios registrados en una convocatoria
@app.route('/verUsuarios/<int:idconvo>', methods=['GET'])
def verUsuarios(idconvo):
    cursor = connection.cursor()
    query = "SELECT nombre, apellidos, correo FROM V_Usuarios_Convocatoria WHERE id_convocatoria = ?"
    cursor.execute(query, (idconvo,))
    results = cursor.fetchall()
    cursor.close()

    return render_template('verUsuarios.html', results=results,titulo=titulo,icon=icon)



#Funcion


#Funcion para modificar una convocatoria
@app.route('/editarConvo/<int:idconvo>', methods=['GET', 'POST'])
def editarConvo(idconvo):

    if 'id_user' not in session:
        return redirect(url_for('login'))


    cursor = connection.cursor()
    id = session.get('id_user')
    tipouser = session.get('tipo_user')
    usuario_logeado = False

    if tipouser == 2:
        cursor.close()
        return redirect(url_for('errorpage'))

    if request.method == 'POST':
        if id and tipouser:
            usuario_logeado = True
            # Procesamos el formulario enviado y actualizamos la base de datos
            titulo = request.form['titulo']
            requisitos = request.form['requisitos']
            fecha_inicio = request.form['fecha_inicio']
            fecha_final = request.form['fecha_final']
            limite_usuarios = request.form['limite_usuarios']
            id_tematica = request.form['id_tematica']
            descripcion = request.form['descripcion']

            cursor.execute("""
                UPDATE Convocatorias
                SET titulo = ?, requisitos = ?, fecha_inicio = ?, fecha_final = ?, 
                    limite_usuarios = ?, id_tematica = ?, descripcion = ?
                WHERE id = ?
            """, (titulo, requisitos, fecha_inicio, fecha_final, limite_usuarios, id_tematica, descripcion, idconvo))

            connection.commit()
            cursor.close()
            return redirect(url_for('Convocatorias'))

    cursor.execute("""
        SELECT * FROM V_Convocatoria_Detalle
        WHERE id = ?
    """, (idconvo,))

    convocatoria = cursor.fetchone()

    cursor.execute("SELECT id, tematica FROM Tematicas")
    tematicas = cursor.fetchall()

    cursor.close()
    return render_template('editarConvo.html', convocatoria=convocatoria, tematicas=tematicas, tipouser=tipouser, usuario_logeado=usuario_logeado)

#Funcion para cerrar sesion

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'success')
    return render_template('index.html')

@app.route('/error')
def errorpage():
    return render_template('error.html',titulo=titulo, icon=icon)





#Modificar
@app.route('/modify', methods=['GET', 'POST'])
def modify():
    if request.method == 'POST':
        if 'id_user' in session:
            id = session.get('id_user')
            correo = request.form['correo']
            passwrd = request.form['pass']
            pass_confirm = request.form['pass_confirm']
            name = request.form['name']
            apellidop = request.form['apellidop']
            apellidom = request.form['apellidom']

            if passwrd != pass_confirm:
                flash('Las contraseñas no coinciden. Intenta nuevamente.', 'danger')
                return redirect(url_for('userhome'))

            # Actualizar datos en la base de datos
            cursor = connection.cursor()
            update_user_query = '''
            UPDATE Usuarios
            SET correo = ?, passwrd = ?
            WHERE id = ?
            '''
            cursor.execute(update_user_query, (correo, passwrd, id))

            update_person_query = '''
            UPDATE Personas
            SET nombre = ?, apellidop = ?, apellidom = ?
            WHERE id = (
                SELECT id_persona
                FROM Usuarios
                WHERE id = ?
            )
            '''
            cursor.execute(update_person_query, (name, apellidop, apellidom, id))

            connection.commit()
            cursor.close()

            flash('Datos actualizados correctamente.', 'success')
            return redirect(url_for('userhome'))

        return "No user in session", 401

    else:
        # Manejo de GET
        if 'id_user' in session:
            id = session.get('id_user')
            cursor = connection.cursor()
            cursor.execute('''
                SELECT u.id, u.correo, u.passwrd, p.nombre, p.apellidop, p.apellidom
                FROM Usuarios AS u
                JOIN Personas AS p ON u.id_persona = p.id
                WHERE u.id = ?
            ''', (id,))
            user = cursor.fetchone()

            if user:
                userdata = {
                    'id': user[0],
                    'correo': user[1],
                    'pass': user[2],
                    'name': user[3],
                    'apellidop': user[4],
                    'apellidom': user[5],
                }
            else:
                userdata = {}

            if request.method == 'POST':
                password = request.form.get('pass')
                confirm_password = request.form.get('pass_confirm')

                if password != confirm_password:
                    flash('Las contraseñas no coinciden. Inténtalo de nuevo.', 'danger')
                    return redirect(url_for('modify'))

                # Aquí iría la lógica para actualizar la contraseña, por ejemplo:
                # if update_password(password):
                flash('Contraseña actualizada exitosamente', 'success')
                return redirect(url_for('modify'))

            cursor.close()
            return render_template('usermd.html', titulo=titulo, icon=icon, userdata=userdata)

        return "No user in session", 401

@app.route('/preview')
def previewver():
    render_template('preview.html',titulo=titulo, icon=icon)
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
