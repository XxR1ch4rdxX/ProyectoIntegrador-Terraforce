#Aqui podremos poner la parte logica de nuestro crud del pi
#como links a otros html , getters , sertters cookies
#incluso la conexion con la base de datos

#ESTE ES EL CORAZON DE LA PAGINA WEB (por asi decirlo)

from colorama import init,Fore,Style
import pyodbc
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy


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

@app.route('/crud')
def signup():  # put application's code here
    titulo = 'TerraForce'
    try:
        cursor.execute("""
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG = ?
                ORDER BY TABLE_NAME ASC;
            """, (database,))

        tablas = [row.TABLE_NAME for row in cursor.fetchall()]
        return render_template('crud.html', titulo=titulo, tablas=tablas)

    except pyodbc.Error as e:
        error_message = f"Error al recuperar las tablas: {str(e)}"
        return render_template('error.html', error_message=error_message)



@app.route('/tablas/<nombretabla>')
def ver_tablas(nombretabla):
    return f'Seleccionaste la tabla {nombretabla}'


@app.route('/about')
def about():  # put application's code here
    titulo = 'TerraForce'
    return render_template(template_name_or_list='about.html',titulo=titulo)


#conexion con la db en SQLserver




if __name__ == '__main__':
    app.run(debug=True)

