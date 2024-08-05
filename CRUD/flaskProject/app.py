#Aqui podremos poner la parte logica de nuestro crud del pi
#como links a otros html , getters , sertters cookies
#incluso la conexion con la base de datos
import traceback
from datetime import datetime

#ESTE ES EL CORAZON de la applicacion web (por asi decirlo)
#Los documentos html adjuntos unicamente se utilizara el de crud, index y editar, los otros
#son "plantillas" que estan colocadas para usarse en algun momento
#Universal Crud :D


#para las librerias usamos translate para traducir los mensajes de eror que mandaran los try y catch desde sql
#colorama lo usamos para cambiar el color de las letritas de la consola
from colorama import init, Fore, Style
from googletrans import Translator
import pyodbc
from flask import Flask, render_template, request, flash, redirect, session, url_for, jsonify
import socket
import sqlite3
import io
from PIL import Image


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

    try:
        server = 'sqlserver'
        database = 'TerraForce'
        username = 'SA'
        password = '1@pOrf4vorD10$'
        print(Fore.CYAN + 'Intentando con conexion a Docker en base de datos local...' + Style.RESET_ALL)
        #conexion a la base de datos local que esta en la misma carpeta
        connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}}; '
        f'SERVER={server}; DATABASE={database}; UID={username}; PWD={password}')

        print(Fore.GREEN + 'Tamo en linea ' + Style.RESET_ALL)

        cursor = connection.cursor()
        cursor.execute("SELECT @@version;")
        row = cursor.fetchone()

        if row:
            print(f'Versión de SQL Server: {row[0]}')
        else:
            print('Hay un error chamo')

    except pyodbc.Error as e:
        print(Fore.GREEN + 'Error Gravisimo :c' + Style.RESET_ALL)


finally:
    cursor.close()


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

    if 'id_user' not in session:
        return redirect(url_for('login'))

    tipouser = session.get('tipo_user')

    if tipouser != 1:
            return redirect(url_for('errorpage'))

    cursor = connection.cursor()
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
        flash('Correo o contraseña incorrectos')
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
        flash(f'Error al cargar los datos: {str(e)}', 'error')
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
    return render_template('about.html', titulo=titulo, icon=icon)



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
    cursor.execute('''
        SELECT c.id, c.titulo, c.requisitos, c.imagen, c.usuarios_registrados, 
               c.limite_usuarios, c.fecha_inicio, c.fecha_final, t.tematica, 
               em.nombre AS empresa_nombre
        FROM Convocatorias AS c 
        INNER JOIN Estatus AS e ON c.id_estatus = e.id 
        INNER JOIN Empresas AS em ON em.id = c.id_empresa 
        INNER JOIN Tematicas AS t ON t.id = c.id_tematica
    ''')
    results = cursor.fetchall()
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
        return render_template('convocatorias.html', results = results, titulo=titulo, icon=icon, nombre=nombre, usuario_logeado=usuario_logeado, tipouser=tipouser)
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
            cursor.close()
            return render_template('crearConvo.html', titulo=titulo, icon=icon, nombre=nombre,
                                   usuario_logeado=usuario_logeado, tipouser=tipouser)
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
        cursor.close()

        return render_template('crearConvo.html', titulo=titulo, results=results, icon=icon, nombre=nombre,
                               usuario_logeado=usuario_logeado, tipouser=tipouser)
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


@app.route('/registrar_convo', methods=['POST'])
def registrar_convo():



    cursor = connection.cursor()
    tituloconv = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    requisitos = request.form.get('requisitos')
    fechainicio = request.form.get('fecha_inicio')
    fechacierre = request.form.get('fecha_cierre')
    tematicas = request.form.get('tematicas')
    vacantes = request.form.get('vacantes')
    imagen = request.files.get('imagen')



    id_user = session.get('id_user')
    tipo_user = session.get('tipo_user')

    imagenbin = None
    if imagen:
        imagenbin = imagen.read()


    if fechainicio == fechacierre :
            flash('La fecha de inicio y de termino no pueden ser iguales')
            return redirect('registro_convocatoria')

    try:
        if not id_user:
            flash('Usuario no autenticado')
            return redirect('registro_convocatoria')

        if vacantes:
            vacantes = int(vacantes)
            if vacantes < 10:
                flash('El número de vacantes mínimo es de 10')
                return redirect('registro_convocatoria')

        if tituloconv and requisitos and fechainicio and fechacierre and vacantes and tematicas and descripcion:

            image = Image.open(io.BytesIO(imagenbin))
            img_io = io.BytesIO()
            image.save(img_io, 'PNG')
            img_io.seek(0)

            cursor.execute("""
                EXEC sp_FIND_id_empresa ?
            """, id_user)
            id_empresa_row = cursor.fetchone()
            if not id_empresa_row:
                flash('No se encontró la empresa para el usuario dado')
                return redirect('registro_convocatoria')

            id_empresa = id_empresa_row[0]


            cursor.execute("""
                EXEC sp_nombre_empresa ?
            """, id_empresa)
            empresa_row = cursor.fetchone()
            if not empresa_row:
                flash('No se encontró el nombre de la empresa para el ID dado')
                return redirect('registro_convocatoria')

            empresa = empresa_row[0]

            return render_template('preview.html', tituloconv=tituloconv, requisitos=requisitos,
                                   fechainicio=fechainicio, fechacierre=fechacierre, vacantes=vacantes,
                                   imagen=imagenbin, tematicas=tematicas, empresa=empresa,tipo_user=tipo_user,descripcion=descripcion)
        else:
            flash('Por favor rellena todos los datos solicitados para el registro')
            return render_template('registro_convocatoria')

    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect('registro_convocatoria')
    finally:
        cursor.close()

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

    # Para admin
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
        cursor.close()

        return render_template('HomeEmpresa.html', titulo=titulo, results=results, icon=icon, nombre=nombre,
                               usuario_logeado=usuario_logeado, tipouser=tipouser)
    else:
        return render_template('HomeEmpresa.html', titulo=titulo, icon=icon, usuario_logeado=usuario_logeado,
                               tipouser=tipouser)
#Palas empresas
    if id and tipouser:
        usuario_logeado = True
        cursor.execute("""
        select e.nombre from usuarios as u
        join Empresas as e on u.id_empresa = e.id
        WHERE u.id=?
        """, (id,))
        nombre= cursor.fetchone()[0]
        cursor.close()

        return render_template('HomeEmpresa.html', titulo=titulo, icon=icon, nombre=nombre, usuario_logeado=usuario_logeado, tipouser=tipouser)
    else:
        return render_template('HomeEmpresa.html', titulo=titulo, icon=icon, usuario_logeado=usuario_logeado, tipouser=tipouser)


#Funcion para mostrar los usuarios registrados en una convocatoria
@app.route('/verUsuarios/<int:idconvo>', methods=['GET'])
def verUsuarios(idconvo):
    cursor = connection.cursor()
    query = '''
            SELECT p.nombre, concat(p.apellidop,' ', p.apellidom) as apellidos, u.correo 
            FROM Registros as r
            JOIN Usuarios as u ON u.id = r.id_voluntario
            JOIN Personas as p on p.id = u.id_persona
            WHERE r.id_convocatoria = ?
            '''
    cursor.execute(query, (idconvo,))
    results = cursor.fetchall()
    cursor.close()

    return render_template('verUsuarios.html', results=results)



#Funcion


#Funcion para modificar una convocatoria
@app.route('/editarConvo/<int:idconvo>', methods=['GET', 'POST'])
def editarConvo(idconvo):
    cursor = connection.cursor()
    if request.method == 'POST':
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
        SELECT c.id, c.titulo, c.requisitos, c.descripcion, c.usuarios_registrados, 
               c.limite_usuarios, c.fecha_inicio, c.fecha_final, e.nombre AS empresa_nombre, 
               es.nombre AS estatus_nombre, t.tematica
        FROM Convocatorias AS c
        JOIN Empresas AS e ON e.id = c.id_empresa
        JOIN Estatus AS es ON es.id = c.id_estatus
        JOIN Tematicas AS t ON t.id = c.id_tematica
        WHERE c.id = ?
    """, (idconvo,))

    convocatoria = cursor.fetchone()

    cursor.execute("SELECT id, tematica FROM Tematicas")
    tematicas = cursor.fetchall()

    cursor.close()
    return render_template('editarConvo.html', convocatoria=convocatoria, tematicas=tematicas)

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


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
