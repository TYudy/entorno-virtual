from flask import Flask , flash, render_template,request,redirect,url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash
import base64



#import bcrypt
#Instancia
app = Flask (__name__)
app.secret_key = 'clave_secreta'
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
    return render_template('Lista.html', persona = usuario)

@app.route('/registrar', methods=['GET','POST'])

def registrar_usuario():
    cursor = db.cursor()
    if request.method == 'POST':
        Nombres = request.form.get('p_Nombre')
        Apellidos = request.form.get('p_Apellido')
        Email = request.form.get('p_Email')
        Direccion = request.form.get('p_Direccion')
        Telefono = request.form.get('p_Telefono')
        Usuario= request.form.get('p_Usuario')
        Contrasena = request.form.get('p_Contrasena')
        Cencriptada = generate_password_hash(Contrasena)


        cursor.execute("SELECT * FROM persona WHERE p_Usuario = %s OR p_Email = %s", (Usuario, Email))
        existe = cursor.fetchall()
        
        if existe:
            for v in existe:

                if v [3] == Email and v[6] == Usuario:
                    flash("El email y el usuario ya existen.", "mensaje")

                elif v[3] == Email:
                    flash("El email ya existe.", "me")

                elif v[6] == Usuario:
                    flash("El usuario ya existe.", "mu")

                
            return redirect(url_for("registrar_usuario"))
        else:
            #insertar datos a la tabla persona
            cursor.execute("INSERT INTO persona(P_Nombre, p_Apellido, p_Email, p_Direccion, p_Telefono, p_Usuario, p_Contraseña)VALUES(%s,%s,%s,%s,%s,%s,%s)",(Nombres, Apellidos, Email, Direccion, Telefono, Usuario, Cencriptada))
            return redirect(url_for('registrar_usuario'))
    db.commit()
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
    


@app.route('/password/<contraencrip>')    
def encriptarcontra(contraencrip):
    #Generar un hash(encriptado) de la contraseña
    #encriptar = bcrypt.hashpw(contraencrip.encode('utf-8'),bcrypt.gensalt())
    encriptar = generate_password_hash(contraencrip)
    valor = check_password_hash(encriptar,contraencrip)

    #return "Encriptado:{0} | coincide: {1}".format(encriptar,valor)
    return valor






@app.route("/login", methods=['GET','POST'])
def login():
    cursor = db.cursor()
    if request.method == 'POST':
     #Verificar credenciales

     username = request.form.get('Usuariol')
     password = request.form.get('Contral')
     cursor.execute ("SELECT p_Usuario, p_Contraseña FROM persona where p_Usuario = %s ",(username,))
     resultado = cursor.fetchone()
    
     if resultado and check_password_hash(resultado[1], password ):
        session['usuario'] = username
        return redirect (url_for ('lista'))
        
     else:
        
        error = 'Credenciales invalidas. Por favor intentarlo de nuevo'
        return render_template('Login.html',error=error)
     
    return render_template('Login.html')

@app.route("/logout")
def logaout():
    session.pop('usuario',None)
    print("Sesión finalizada")
    return redirect(url_for('login'))    
    
@app.route("/a_cancion", methods =['GET', 'POST'])
def add_song():
    cursor = db.cursor()
    if request.method == 'POST':
        Titulo = request.form.get('title')  
        Artista = request.form.get('artist')
        Genero = request.form.get('genre')
        Precio = request.form.get('price')
        Duracion = request.form.get('duration')
        Fecha = request.form.get('date')
        Imagen = request.form.get('image')



        cursor.execute("INSERT INTO canciones (Titulo, Artista, Genero, Precio, Duracion, A_Lanzamiento,img)VALUES(%s,%s,%s,%s,%s,%s,%s)",(Titulo,Artista,Genero,Precio,Duracion,Fecha,Imagen))
        return redirect(url_for('add_song'))
    db.commit()
    return render_template("C_add.html")
    


@app.route("/l_cancion")
def list_song():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM canciones")
    cancion = cursor.fetchall()
    return render_template("C_lista.html", canciones = cancion)
    


    
if __name__ == '__main__':
    app.add_url_rule('/', view_func=lista)
    app.run(debug = True, port=5000)
#Rutas
    

