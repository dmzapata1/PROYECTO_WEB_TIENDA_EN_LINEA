from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Inicializar la instancia de la aplicación
app = Flask(__name__)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Crear el modelo de la base de datos
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f'<Product {self.name} - available {self.quantity}>'

# Rutas

#Pagina Principal
@app.route('/')
def index():
    return render_template('index.html')

# Create
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        new_product = Product(name=name, price=price, quantity=quantity)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('list_products'))
    return render_template('add_products.html')

#Read
@app.route('/catalogue')
def list_products():
    products = Product.query.all()
    return render_template('list_products.html', products=products)

#Update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.quantity = request.form['quantity']
        db.session.commit()
        return redirect(url_for('list_products'))
    return render_template('update_product.html', product=product)

#Delete
@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('list_products'))


#Client View

@app.route('/client')
def client():
    products = Product.query.all()
    return render_template('client.html', products=products)

# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)
