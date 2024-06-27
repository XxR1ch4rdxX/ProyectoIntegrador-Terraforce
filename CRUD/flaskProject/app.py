#Aqui podremos poner la parte logica de nuestro crud del pi
#como links a otros html , getters , sertters cookies
#incluso la conexion con la base de datos

#ESTE ES EL CORAZON DE LA PAGINA WEB (por asi decirlo)

from flask import Flask,render_template
import pyodbc

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    titulo = 'TerraForce'
    return render_template(template_name_or_list='index.html',titulo=titulo)

@app.route('/signup')
def signup():  # put application's code here
    titulo = 'TerraForce'
    return render_template(template_name_or_list='signup.html',titulo=titulo)

@app.route('/about')
def about():  # put application's code here
    titulo = 'TerraForce'
    return render_template(template_name_or_list='about.html',titulo=titulo)


#conexion con la db en SQLserver

#try:
#    connection = pyodbc.connect('DRIVER={SQL server}; SERVER=PCerda')


if __name__ == '__main__':
    app.run(debug=True)

