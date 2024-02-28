from flask import *
import mysql.connector
#Instancia
app = Flask (__name__)
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password="",
    database = "Agenda"

)

cursor = db.cursor()
#Para ejecutar
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    Nombres = request.form['p_Nombre'],
    Apellidos = request.form['p_Apellido'],
    Email = request.form['p_Email'],
    Direccion = request.form['p_Dirección'],
    Telefono = request.form['p_Telefono'],
    Usuario= request.form['p_Usuario'],
    Contrasena = request.form['p_Contrasena'],
 #insertar datos a la tabla persona
    
    cursor.execute("INSERT INTO Persona(p_Nombre, p_Apellido, p_Email, p_Dirección, p_Telefono, p_Usuario, p_Contraseña)VALUES(%s,%s,%s,%s,%s,%s,%s)",(Nombres, Apellidos, Email, Direccion, Telefono, Usuario, Contrasena))
    db.commit()
   
    return redirect(url_for('/registrar'))

   


if __name__ == '__main__':
    app.add_url_rule('/', view_func=index)
    app.run(debug = True, port=5005)
#Rutas
