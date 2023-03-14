
from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import send_from_directory
import os
import html
import re
import locale
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import urllib.parse, hashlib
import requests  
from markupsafe import escape
import cloudinary
import cloudinary.uploader
import cloudinary.api
from jinja2.utils import markupsafe 
from markupsafe import Markup


from werkzeug.utils import escape



app = Flask(__name__)
cloudinary.config(
  cloud_name = "dacwrjdao",
  api_key = "929543513912788",
  api_secret = "eFlFzOxMUJHm6xs3FfbnNyVPtXk",
  secure = True
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ujnwugpgvon3etap:gGyiBlcBrNBPRsU0doOd@bs2dpuyw1atuftpcyqku-mysql.services.clever-cloud.com:3306/bs2dpuyw1atuftpcyqku'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SSL'] = True
ssl=True
db = SQLAlchemy(app)
app.secret_key="clave_secreta"


with app.app_context():
    class Post(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        nombre = db.Column(db.String(255), nullable=False)
        fecha = db.Column(db.String(255), nullable=False)
        descripcion = db.Column(db.String(255), nullable=False)
        imagen= db.Column(db.String(255), nullable=False)
        contenido = db.Column(db.Text, nullable=False)
        tag = db.Column(db.String(255), nullable=False)
        nombre_imagen = db.Column(db.String(255), nullable=False)
    
    db.create_all()

@app.route("/css/<css>")
def css_link(css):
    return send_from_directory(os.path.join('templates/sitio/css'), css)

@app.route("/js/<js>")
def js_link(js):
    return send_from_directory(os.path.join('templates/sitio/js'), js)

@app.route("/fonts/<fonts>")
def fonts_link(fonts):
    return send_from_directory(os.path.join('templates/sitio/fonts'), fonts)

@app.route('/')
def inicio():
    quary = db.session.query(Post).order_by(Post.fecha.desc()).all()
    
    posts = []
    for post in quary:
        posts.append((post.id,post.nombre, post.fecha, post.descripcion, post.imagen, post.contenido, post.tag))
    
    return render_template('sitio/index.html', post=posts)

@app.route('/img/<imagen>')
def imagen(imagen):
    return send_from_directory(os.path.join('templates/sitio/img'), imagen)

@app.route('/post')
def post():
    posts = db.session.query(Post).all()
    print(posts)
    return render_template('sitio/post.html', post=post)

@app.route('/about')
def about():
    return render_template('sitio/about.html')

@app.route('/mangas')
def manga():
    return render_template('sitio/Mangas.html')

@app.route('/admin/')
def admin_index():
    if not session.get('login'):
        return redirect('/admin/login')
    return render_template('admin/indexadmin.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login/', methods=['POST'])
def admin_login_post():
    usuario = request.form['txtUsuario']
    password = request.form['txtPassword']
    print(usuario)
    print(password)
    if usuario == 'LeviS' and password == 'gadiel1999':
        session['login'] = True
        session['usuario'] = "Administrador"
        return redirect('/admin/')
    return redirect('/admin/login')

@app.route('/admin/cerrar')
def admin_cerrar():
    session.clear()
    return redirect('/')

@app.route('/admin/post')
def admin_post():
    if not session.get('login'):
        return redirect('/admin/login')
    quary = db.session.query(Post).order_by(Post.fecha.desc()).all()
    print(quary)
    
    posts = []
    for post in quary:
        posts.append((post.id,post.nombre, post.fecha, post.descripcion, post.imagen, post.contenido, post.tag))
    return render_template('admin/post.html', posts=posts)


@app.route('/admin/post/guardar', methods=['POST'])
def admin_post_guardar():
    if not session.get('login'):
        return redirect('/admin/login')

    titulo = request.form['txtNombre']
    fecha = request.form['txtFecha']
    imagen = request.files['txtImagen']
    descripcion = request.form['txtDescripcion']
    contenidos = request.form['txtContenido']
    tags = request.form['txtTag']
    tiempo=datetime.now()
    horaActual=tiempo.strftime("%Y%H%M%S")

    def limpiar_texto(texto):
        # Convertir las entidades HTML a sus caracteres correspondientes
        texto = html.unescape(texto)
        # Eliminar las etiquetas HTML
        texto = re.sub(r'<[^>]*>', '', texto)
        return texto

    contenido_limpio = limpiar_texto(contenidos)
    resultado = cloudinary.uploader.upload(imagen)
    nuevaUrlImagen = resultado['secure_url']
    nombre_imagen = resultado['public_id']
    

    # Crear un objeto Post con los datos del formulario
    post = Post(nombre=titulo, fecha=fecha, descripcion=descripcion,
                imagen=nuevaUrlImagen,
                contenido=contenido_limpio, tag=tags, nombre_imagen=nombre_imagen)

    # Guardar el objeto Post en la base de datos
    db.session.add(post)
    db.session.commit()

    return redirect('/admin/post')

@app.route('/admin/post/delete', methods=['POST'])
def admin_post_delete():
    if not session.get('login'):
        return redirect('/admin/login')
    id = request.form['txtID']
    print(id)
    
    # Obtener el nombre de la imagen del post a eliminar
    post = Post.query.filter_by(id=id).first()
    nombre_imagen = post.nombre_imagen
    
    # Eliminar la imagen del post
   # if os.path.exists("templates/sitio/img/" + nombre_imagen):
    #os.unlink("templates/sitio/img/" + nombre_imagen)
    cloudinary.uploader.destroy(nombre_imagen, invalidate=True)
    # Eliminar el post de la base de datos
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    
    return redirect('/admin/post')

@app.route("/blog/<nombre>")
def blog(nombre):
    
    quary = db.session.query(Post).filter(Post.nombre == nombre).all()
    print(quary)
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    posts = []
    for post in quary:
        fecha_modi = datetime.strptime(post.fecha, '%Y-%m-%d').strftime('%d de %B')
        posts.append((post.id,post.nombre, fecha_modi, post.descripcion, post.imagen,post.contenido, post.tag))
      
    return render_template('sitio/blog.html',posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
