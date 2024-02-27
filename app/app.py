from flask import *

#Instancia
app = Flask (__name__)

#Para ejecutar
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/registrar')
def saludos():
    return render_template('Registrar.html')



if __name__ == '__main__':
    app.add_url_rule('/', view_func=index)
    app.run(debug = True, port=5005)
#Rutas
