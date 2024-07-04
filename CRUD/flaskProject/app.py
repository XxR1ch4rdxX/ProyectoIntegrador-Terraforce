#Aqui podremos poner la parte logica de nuestro crud del pi
#como links a otros html , getters , sertters cookies
#incluso la conexion con la base de datos

#ESTE ES EL CORAZON DE LA PAGINA WEB (por asi decirlo)

from colorama import init,Fore,Style
import pyodbc
from flask import Flask, render_template, request, flash, redirect
import socket



init()


app = Flask(__name__)
app.secret_key='123'
server=socket.gethostname()
database='TacoLovers'
titulo = database

if database== 'TacoLovers':
    icon= "../static/images/taco.ico"

elif database== 'TerraForce':
    icon= "../static/images/socios.ico"

else:
    icon= "../static/images/demon.ico"


try:
    print(Fore.CYAN+'Estableciendo la conexion con sql server ...'+Style.RESET_ALL)
    connection = pyodbc.connect('DRIVER={SQL Server}; SERVER='+server+'; DATABASE='+database+'; Trusted_Connection=yes;')
    print(Fore.GREEN+'Tamo en linea '+Style.RESET_ALL)
    cursor = connection.cursor()
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    if row:
        print(f'Versión de SQL Server: {row[0]}')

    else:
        print('Hay un error chamo')

except pyodbc.Error as e:
    print(Fore.GREEN+'Error :c'+Style.RESET_ALL)





@app.route('/')
def index():  # put application's code here


    return render_template(template_name_or_list='index.html',titulo=titulo,icon=icon )



@app.route('/crud',methods=['GET'])
def consultartablas():  # put application's code here
    palabrita = ""

    tablaselect = request.args.get('tablaselect','')
    flash("Aqui se mostraran las alertas :)")
    try:
        cursor.execute("""
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG = ?
                ORDER BY TABLE_NAME ASC;
            """, (database,))
        tablas = [row.TABLE_NAME for row in cursor.fetchall()]

        if tablaselect:
            cursor.execute('SELECT * FROM ' + tablaselect)
            rows = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
        else:
            rows = []
            column_names = []


        return render_template('crud.html', titulo=titulo, tablas=tablas,tablaselect=tablaselect
                               ,rows=rows,column_names=column_names,palabrita=palabrita,icon=icon )

    except pyodbc.Error as e:
        error_message = f"Error al recuperar las tablas: {str(e)}"
        return render_template('error.html', error_message=error_message)

@app.route('/remove', methods=['GET'])
def remove():

    registro_id = request.args.get('id')
    tablaname = request.args.get('tablaselect')
    if registro_id and tablaname:
        try:
         cursor.execute(f"DELETE FROM {tablaname} WHERE id = ?", (registro_id,))
         connection.commit()
         flash(f'Se ha eliminado el registro con ID {registro_id} de la tabla {tablaname} correctamente. :D')
        except pyodbc.Error as e:
            error_message = f"Error al eliminar el registro: {str(e)}"
            flash(error_message, 'error'+"   :c")
    return redirect('crud')



@app.route('/edit', methods=['GET'])
def edit():

    registro_id = request.args.get('id')
    tabla = request.args.get('tablaselect')

    cursor.execute('alter table'+tabla+'')
    return render_template('crud.html')

@app.route('/agg', methods=['GET'])
def agg():
    tabla = request.args.get('tablaselect')
    cursor.execute('select * from '+tabla)
    redirect('formulario')


@app.route('/about')
def about():  # put application's code here
    titulo = 'TerraForce'
    return render_template(template_name_or_list='about.html',titulo=titulo,icon=icon )







if __name__ == '__main__':
    app.run(debug=True)

