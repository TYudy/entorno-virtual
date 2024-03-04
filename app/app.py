from flask import Flask , flash, render_template,request,redirect,url_for
import mysql.connector
#Instancia
app = Flask (__name__)
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password="",
    database = "agenda"

)

cursor = db.cursor()
#Para ejecutar
@app.route('/')



def lista():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM persona')
    usuario = cursor.fetchall()
    return render_template('index.html', persona = usuario)

@app.route('/registrar', methods=['GET','POST'])
def registrar_usuario():
    if request.method == 'POST':
        Nombres = request.form.get('p_Nombre')
        Apellidos = request.form.get('p_Apellido')
        Email = request.form.get('p_Email')
        Direccion = request.form.get('p_Direccion')
        Telefono = request.form.get('p_Telefono')
        Usuario= request.form.get('p_Usuario')
        Contrasena = request.form.get('p_Contrasena')
    
 #insertar datos a la tabla persona
    
        cursor.execute("INSERT INTO persona(P_Nombre, p_Apellido, p_Email, p_Direccion, p_Telefono, p_Usuario, p_Contraseña)VALUES(%s,%s,%s,%s,%s,%s,%s)",(Nombres, Apellidos, Email, Direccion, Telefono, Usuario, Contrasena))
        db.commit()
        flash('usuario creado correctamente','Sucess')
        return redirect(url_for('registrar_usuario'))
        
    return render_template("Registrar.html")

@app.route('/editar', methods=['PUT','POST'])
def registrar_usuario():
    if request.method == 'PUT':
        Nombres = request.form.put('p_Nombre')
        Apellidos = request.form.put('p_Apellido')
        Email = request.form.put('p_Email')
        Direccion = request.form.put('p_Direccion')
        Telefono = request.form.put('p_Telefono')
        Usuario= request.form.put('p_Usuario')
        
        
 #insertar datos a la tabla persona
    
        cursor.execute("update persona (P_Nombre, p_Apellido, p_Email, p_Direccion, p_Telefono, p_Usuario, p_Contraseña)VALUES(%s,%s,%s,%s,%s,%s,%s)",(Nombres, Apellidos, Email, Direccion, Telefono, Usuario, Contrasena))


if __name__ == '__main__':
    app.add_url_rule('/', view_func=lista)
    app.run(debug = True, port=5000)
#Rutas
    

