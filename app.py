from flask import Flask, request, render_template, redirect
from flask_cors import CORS, cross_origin #incorporado
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
import urllib.parse
from flask_wtf.file import FileAllowed

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:4306/proyecto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456'
app.config['MYSQL_PORT'] = 4306


db = SQLAlchemy(app)


ma = Marshmallow(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100))
    talle = db.Column(db.Integer)
    imagen = db.Column(db.LargeBinary)
    
    def __init__(self, tipo, talle, imagen):
        self.tipo = tipo
        self.talle = talle
        self.imagen = imagen

with app.app_context():
    db.create_all()

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'tipo', 'talle', 'imagen')

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

@app.route("/")
def inicio():
    return render_template("buzos.html")

@app.route('/productos', methods=['GET'])
def get_productos():
    all_productos = Producto.query.all()

    return productos_schema.jsonify(all_productos)

@app.route('/productos', methods=['POST'])
def create_producto():
    tipo = request.json['tipo']
    talle = request.json['talle']
    imagen = request.json['imagen']   # eliminar read() porque es un 
    
    print(tipo, talle, imagen) 

    try:
        new_producto = Producto(tipo, talle, imagen.encode('ascii'))
        db.session.add(new_producto)
        db.session.commit()
        return producto_schema.jsonify(new_producto)
       
    except Exception as e:
        print(type(e).__name__)

@app.route('/productos/<id>', methods=['GET'])
def get_producto(id):
    producto = Producto.query.get(id)
    return producto_schema.jsonify(producto)

@app.route('/productos/<id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)

@app.route('/productos/<id>', methods=['PUT'])
def update_producto(id):
    
    tipo = request.json['tipo'] # la clave es tipo no nombre
    talle = request.json['talle']  # la talle es tipo no precio
    imagen = request.json['imagen'].encode('ascii')
    print(tipo, talle, imagen, id)
    try:
        producto = Producto.query.get(id)
        print(producto)
        producto.tipo = tipo       #Error los atributos en minusculas
        producto.talle = talle
        producto.imagen = imagen
        db.session.commit()
        return producto_schema.jsonify(producto)
    except Exception as e:
        print(type(e).__name__)

class ImageForm(FlaskForm):
    tipo = StringField('Tipo')
    talle = IntegerField('Talle')
    imagen = FileField('Selecciona una imagen', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])

@app.route('/productos/upload', methods=['GET', 'POST'])
def upload_image():
    form = ImageForm()
    if form.validate_on_submit():
        tipo = form.tipo.data
        talle = form.talle.data
        imagen = form.imagen.data
        filename = secure_filename(imagen.filename)
        imagen.save(filename)
        return 'Imagen cargada exitosamente'
    return render_template('producto_nuevo.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)