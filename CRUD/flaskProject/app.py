#Aqui podremos poner la parte logica de nuestro crud del pi
#como links a otros html , getters , sertters cookies
#incluso la conexion con la base de datos

#ESTE ES EL CORAZON DE LA PAGINA WEB (por asi decirlo)

from colorama import init,Fore,Style
import pyodbc
from flask import Flask,render_template,request



init()


app = Flask(__name__)
server='PCerda'
database='TerraForce'
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
    titulo = 'TerraForce'

    return render_template(template_name_or_list='index.html',titulo=titulo )



@app.route('/crud',methods=['GET'])
def consultartablas():  # put application's code here
    titulo = 'TerraForce'
    tablaselect = request.args.get('tablaselect','')

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
                               ,rows=rows,column_names=column_names),tablaselect

    except pyodbc.Error as e:
        error_message = f"Error al recuperar las tablas: {str(e)}"
        return render_template('error.html', error_message=error_message)

@app.route('/remove', methods=['GET'])
def remove():
    registro_id = request.args.get('id')
    tabla=request.args.get('tabla')
    if registro_id:
        try:
            cursor.execute('DELETE FROM ' + tabla + ' WHERE TABLE_NAME = ?', (registro_id,))
            connection.commit()
        except:
            return 'error'
    return render_template('crud.html')

@app.route('/edit', methods=['GET'])
def edit():

    registro_id = request.args.get('id')
    return registro_id

@app.route('/about')
def about():  # put application's code here
    titulo = 'TerraForce'
    return render_template(template_name_or_list='about.html',titulo=titulo)


#conexion con la db en SQLserver




if __name__ == '__main__':
    app.run(debug=True)

