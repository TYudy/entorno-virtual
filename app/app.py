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
<<<<<<< HEAD


        cursor.execute("SELECT * FROM persona WHERE p_Usuario = %s OR p_Email = %s", (Usuario, Email))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash("El usuario o correo electrónico ya existe.", "error")
            return redirect(url_for("registrar registrar_usuario"))
        
=======
    
>>>>>>> 6fbed9edc9499c9c546fd55b883f1c51e4700de0
 #insertar datos a la tabla persona
    
        cursor.execute("INSERT INTO persona(P_Nombre, p_Apellido, p_Email, p_Direccion, p_Telefono, p_Usuario, p_Contraseña)VALUES(%s,%s,%s,%s,%s,%s,%s)",(Nombres, Apellidos, Email, Direccion, Telefono, Usuario, Contrasena))
        db.commit()
<<<<<<< HEAD
        
=======
        flash('usuario creado correctamente','Sucess')
>>>>>>> 6fbed9edc9499c9c546fd55b883f1c51e4700de0
        return redirect(url_for('registrar_usuario'))
   


    return render_template("Registrar.html")

@app.route("/editar/<int:id>", methods=["POST", "GET"])
def editar_usuario(id):
    cursor = db.cursor()
    if request.method == "POST":
        nombreper = request.form.get("nombre")
        apellidoper = request.form.get("apellido")
        emailper = request.form.get("email")
        dirreccionper = request.form.get("direccion")
        telefonoper = request.form.get("telefono")
        usuarioper = request.form.get("usuario")
        contraper = request.form.get("contra")

        sql = "update persona set p_nombre=%s, p_Apellido=%s,p_Email=%s,p_Direccion=%s, p_Telefono=%s,p_Usuario=%s, p_contraseña=%s where ID_Persona=%s"
        cursor.execute(
            sql,
            (
                nombreper,
                apellidoper,
                emailper,
                dirreccionper,
                telefonoper,
                usuarioper,
                contraper,
                id,
            ),
        )
        db.commit()

        return redirect(url_for("lista"))

    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM persona WHERE ID_Persona =%s", (id,))
        data = cursor.fetchall()
        return render_template("Editar.html", usuario=data[0])


@app.route("/eliminar/<int:id>", methods=["GET"])
def eliminar_usuario(id):
    cursor = db.cursor()
    if request.method == "GET":
        cursor.execute(  "delete from  persona where ID_Persona=%s" , (id,))
        db.commit()
        return redirect(url_for("lista"))
    

   






if __name__ == '__main__':
    app.add_url_rule('/', view_func=lista)
    app.run(debug = True, port=5000)
#Rutas
    

