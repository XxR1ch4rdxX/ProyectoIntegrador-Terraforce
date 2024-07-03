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

try:
    print(Fore.CYAN+'Estableciendo la conexion con sql server ...'+Style.RESET_ALL)
    connection = pyodbc.connect('DRIVER={SQL Server}; SERVER=PCerda; DATABASE=TerraForce; Trusted_Connection=yes;')
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
    return render_template(template_name_or_list='index.html',titulo=titulo)

@app.route('/crud')
def signup():  # put application's code here
    titulo = 'TerraForce'
    return render_template(template_name_or_list='signup.html',titulo=titulo)

@app.route('/about')
def about():  # put application's code here
    titulo = 'TerraForce'
    return render_template(template_name_or_list='about.html',titulo=titulo)


#conexion con la db en SQLserver




if __name__ == '__main__':
    app.run(debug=True)

