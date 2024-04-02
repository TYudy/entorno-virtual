from flask import Flask , flash, render_template,request,redirect,url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash
from PIL import Image 
import base64

from datetime import datetime


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
@app.route('/lista')
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
        roles = request.form.get('txtrol')


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
            cursor.execute("INSERT INTO persona(P_Nombre, p_Apellido, p_Email, p_Direccion, p_Telefono, p_Usuario, p_Contraseña,Roles)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(Nombres, Apellidos, Email, Direccion, Telefono, Usuario, Cencriptada,roles))
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
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
     #Verificar credenciales

     username = request.form.get('Usuariol')
     password = request.form.get('Contral')
     sql = "SELECT p_Usuario, p_Contraseña,Roles FROM persona where p_Usuario = %s "
     cursor.execute(sql,(username,))
     user = cursor.fetchone()
    
     if user and check_password_hash(user['p_Contraseña'], password ):
        session['usuario'] = user ['p_Usuario']
        session['rol'] = user['Roles']
        # De acuerdo al rol asignamos la url 
        if user['Roles'] == 'Administrador':
            return redirect (url_for ('lista'))
        else:
            return redirect (url_for ('listc_song'))

        
     else:
        
        error = 'Credenciales invalidas. Por favor intentarlo de nuevo'
        return render_template('Login.html',error=error)
     
    return render_template('Login.html')

@app.route("/logout")
def logout():
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
        Imagen = request.files['image']
        imagenb = Imagen.read()

        #cursor.execute("select * from canciones where Titulo = %s"(Titulo))
        #existing_canciones = cursor.fetchone()
        #if existing_canciones:
         #   return render_template('C_add.html')



        cursor.execute("INSERT INTO canciones (Titulo, Artista, Genero, Precio, Duracion, A_Lanzamiento,img)VALUES(%s,%s,%s,%s,%s,%s,%s)",(Titulo,Artista,Genero,Precio,Duracion,Fecha,imagenb))
        print(Imagen)
        return redirect(url_for('add_song'))
    db.commit()
    return render_template("C_add.html")


@app.route("/l_cancion")
def list_song():
    cursor = db.cursor()
    cursor.execute("SELECT ID_Cancion,Titulo, Artista, Genero, Precio, Duracion, A_Lanzamiento,img FROM canciones")
    canciones = cursor.fetchall()


    if canciones:
        cancioneslist = []
        for cancion in canciones:
            imagen = base64.b64encode(cancion[7]).decode('utf-8')
            cancioneslist.append({
                'ID_Cancion':cancion[0],
                'Titulo':cancion[1],
                'Artista':cancion[2],
                'Genero':cancion[3],
                'Precio':cancion[4],
                'Duracion':cancion[5],
                'A_Lanzamiento':cancion[6],
                'img':imagen
                })
            
        return render_template("C_lista.html", canciones = cancioneslist)
    else:
        return print("canciones no encontradas")
    

@app.route("/lc_cancion")
def listc_song():
    cursor = db.cursor()
    cursor.execute("SELECT ID_Cancion,Titulo, Artista, Genero, Precio, Duracion, A_Lanzamiento,img FROM canciones")
    canciones = cursor.fetchall()


    if canciones:
        cancioneslist = []
        for cancion in canciones:
            imagen = base64.b64encode(cancion[7]).decode('utf-8') 
            cancioneslist.append({
                'ID_Cancion':cancion[0],
                'Titulo':cancion[1],
                'Artista':cancion[2],
                'Genero':cancion[3],
                'Precio':cancion[4],
                'Duracion':cancion[5],
                'A_Lanzamiento':cancion[6],
                'img':imagen
                })
            
        return render_template("C_listac.html", canciones = cancioneslist)
    else:
        return render_template("C_listac.html")
       
        

    

@app.route("/d_cancion/<int:id>", methods=["GET"])
def delete_song(id):
    cursor = db.cursor()
    if request.method == "GET":
        cursor.execute( "delete from canciones where ID_Cancion=%s" , (id,))
        db.commit()
        return redirect(url_for("list_song"))
    


@app.route("/u_cancion/<int:id>", methods=["POST", "GET"])
def update_song(id):
    cursor = db.cursor()
    if request.method == "POST":
        Titulou = request.form.get('t')  
        Artistau = request.form.get('a')
        Generou = request.form.get('g')
        Preciou = request.form.get('p')
        Duracionu = request.form.get('d')
        Fechau = request.form.get('da')
        Imagen = request.files['im']
        imagenb = Imagen.read()
        

        cursor.execute("update canciones set Titulo=%s, Artista=%s, Genero=%s, Precio=%s, Duracion=%s, A_Lanzamiento=%s,img=%s where ID_Cancion=%s",(Titulou,Artistau,Generou,Preciou,Duracionu,Fechau,imagenb,id))
        db.commit()
        return redirect(url_for('list_song'))
    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM canciones WHERE ID_Cancion =%s", (id,))
        data = cursor.fetchall()
        return render_template("C_update.html", cancion=data[0])

@app.route("/cart/<int:id>")
def cart(id):
    cursor = db.cursor()
    cursor.execute("select * from canciones where ID_Cancion = %s",(id,))
    cancion = cursor.fetchone()
    
    
    if cancion:
        cursor = db.cursor()
        n = session["usuario"]
        cursor.execute("select ID_Persona from persona where P_Usuario =%s ",(n,) )
        usuarioi = cursor.fetchone()
        if usuarioi:
                usuario = usuarioi[0]
                fecha = datetime.now()
                precio = cancion[4]
                can = cancion[0]
                metodo = "Tarjeta"
                cursor.execute("insert into compras (Fecha_Compra,Precio,ID_persona, ID_Cancion, MPago)VALUES(%s,%s,%s,%s,%s)",(fecha,precio,usuario,can,metodo))
                db.commit() 
        return redirect(url_for('listc_song'))
    else:
        print("NO SE EJECUTÓ")
   
    return redirect(url_for('listc_song', cancion = cancion))


@app.route("/s_cart")
def s_cart():
    cursor = db.cursor()
    usuario = session['usuario']
    cursor.execute("select ID_Persona from persona where P_Usuario =%s",(usuario,))
    sesion = cursor.fetchone()
   
    if sesion:
        cursor.execute("select cp.Fecha_Compra, c.img, SUM(cp.Precio), COUNT(cp.ID_Cancion), c.Titulo, cp.ID_Compra, cp.ID_Cancion, cp.Precio, cp.MPago, p.ID_Persona from compras cp inner join canciones c ON cp.ID_Cancion = c.ID_Cancion inner join persona p on cp.ID_Persona = p.ID_Persona where cp.ID_Persona = %s group by c.ID_Cancion",(sesion[0],))
        compras = cursor.fetchall()
        if compras:
            print("holaa")
            carrito = []
            for cancion in compras:
                imagen = base64.b64encode(cancion[1]).decode('utf-8')
                carrito.append({
                    'fecha':cancion[0],
                    'img':imagen,
                    'total':cancion[2],
                    'cantidad':cancion[3],
                    'titulo':cancion[4],
                    'idc':cancion[5],
                    'id':cancion[6],
                    'Precio':cancion[7],
                    'metodo':cancion[8],
                    'persona':cancion[9]
                    })
            return render_template("Carrito.html", compras = carrito)
        else:
            print("holaa888")
            print(usuario)
            return render_template("Carrito.html")
    else:
        print("Se pudrio todo")
        return render_template("Carrito.html")


@app.route("/d_cart/<int:id>/<int:idc>", methods=["GET"])
def d_cart(id,idc):
    cursor = db.cursor()
    if request.method == "GET":
        cursor.execute( "delete from compras where ID_Cancion=%s and ID_Compra=%s" , (id,idc))
        db.commit()
        return redirect(url_for("s_cart"))


@app.route("/a_cart/<int:id>/<float:precio>/<string:metodo>/<string:fecha>/<int:persona>", methods=["GET","POST"])
def a_cart(id,precio, metodo, fecha,persona):
    fechao = datetime.strptime(fecha, '%Y-%m-%d').date()
    cursor = db.cursor()
    if request.method == "GET":
        print("sos una capa")
        cursor.execute("insert into compras (Fecha_Compra,Precio,ID_persona, ID_Cancion, MPago)VALUES(%s,%s,%s,%s,%s)",(fechao,precio,persona,id,metodo))
        db.commit()
        return redirect(request.referrer)  # Redirigir al usuario a la misma página desde donde vino
    else:
        return redirect(request.referrer)
    
@app.route("/da_cart") 
def da_cart():
    cursor = db.cursor()
    usuario = session['usuario']
    cursor.execute("select ID_Persona from persona where P_Usuario =%s",(usuario,))
    sesion = cursor.fetchone()
    if sesion:
        #cursor.execute("ALTER TABLE compras AUTO_INCREMENT=0;")
        #db.commit()
        cursor.execute("DELETE FROM compras WHERE ID_Persona=%s", (sesion[0],))
        db.commit()
        return render_template("Carrito.html")
    else:
        return render_template("Carrito.html")

if __name__ == '__main__':
    app.add_url_rule('/', view_func=login)
    app.run(debug = True, port=5000)
#Rutas
    

