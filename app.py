from flask import Flask ,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import DATABASE_URI
#import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

# Public AD model
class PublicAD(db.Model):
    __tablename__ = 'PublicAD'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    price = db.Column(db.Float)

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

# City model
class City(db.Model):
    __tablename__ = 'Cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,unique=True)
    users = db.relationship('User', backref="city", lazy="joined")

    def __init__(self, name):
        self.name = name

# User model
class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String,unique=True)
    email = db.Column(db.String)
    password =db.Column(db.String)
    phone = db.Column(db.String(13))
    city_name = db.Column(db.String,db.ForeignKey('Cities.name'))
    localads = db.relationship('LocalAD', backref="user", lazy="joined")

    def __init__(self,fullname,email,password,phone,city_name):
        self.fullname = fullname
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        #bcrypt.check_password_hash(pw_hash, 'hunter2')  # returns True
        self.phone = phone
        self.city_name = city_name

# Local AD model
class LocalAD(db.Model):
    __tablename__ = 'LocalAD'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price = db.Column(db.Float)
    author_fullname = db.Column(db.String,db.ForeignKey('Users.fullname'))
    user_phone = db.Column(db.String(13))

    def __init__(self, title, price, author_fullname,user_phone):
        self.title = title
        self.price = price
        self.author_fullname = author_fullname
        self.user_phone = user_phone

# Public Ad Schema
class PublicADSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author','price')

# City Ad Schema
class CitySchema(ma.Schema):
    class Meta:
        fields = ('id','name')

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','fullname','email','password','phone','city_name')

# Local Ad Schema
class LocalADSchema(ma.Schema):
    class Meta:
        fields = ('id','title','price','author_fullname','user_phone')

# Init schema for publicad
publicad_schema = PublicADSchema()
publicads_schema = PublicADSchema(many=True)

# Init schema for city
city_schema = CitySchema()
cities_schema = CitySchema(many=True)

# Init schema for user
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Init schema for localad
localad_schema = LocalADSchema()
localads_schema = LocalADSchema(many=True)

# Create an public ad
@app.route('/ad', methods =['POST'])
def add_publicad():
    try:
        title = request.json['title']
        author = request.json['author']
        price = request.json['price']

        new_publicad = PublicAD(title, author, price)

        db.session.add(new_publicad)
        db.session.commit()
        #return publicad_schema.jsonify(new_publicad)
        return jsonify({'message': 'Public ad created successfully'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Enter all data."}), 400

# Create a city
@app.route('/city',methods=['POST'])
def add_city():
    try:
        name = request.json['name']
        new_city = City(name)

        db.session.add(new_city)
        db.session.commit()
        #return city_schema.jsonify(new_city)

        return jsonify({'message': 'City created successfully'}),201
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Enter all data."}),400


# Create a user
@app.route('/user',methods=['POST'])
def add_user():
    try:
        fullname = request.json['fullname']
        email = request.json['email']
        password = request.json['password']
        phone = request.json['phone']
        city_name = request.json['city_name']

        new_user = User(fullname,email,password,phone,city_name)

        db.session.add(new_user)
        db.session.commit()
        #return user_schema.jsonify(new_user)
        return jsonify({'message': 'User created successfully'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Enter all data."}), 400

# Create a local ad
@app.route('/localad', methods =['POST'])
def add_localad():
    try:
        title = request.json['title']
        price = request.json['price']
        author_fullname = request.json['author_fullname']
        user = User.query.filter_by(fullname=author_fullname).first()
        user_phone = user.phone

        new_localad = LocalAD(title, price, author_fullname,user_phone)

        db.session.add(new_localad)
        db.session.commit()
        # return localad_schema.jsonify(new_localad)
        return jsonify({'message': 'Local ad created successfully'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Enter all data."}), 400

# Get all publicads
@app.route('/ad',methods=['GET'])
def get_publicads():
    try:
        all_publicads = PublicAD.query.all()
        result = publicads_schema.dump(all_publicads)

        return jsonify(result), 200
    except Exception:
        db.session.rollback()
        return jsonify({"message": "List empty!"}), 400

# Get all cities
@app.route('/city',methods=['GET'])
def get_cities():
    try:
        all_cities = City.query.all()
        result = cities_schema.dump(all_cities)

        return jsonify(result),200
    except Exception:
        db.session.rollback()
        return jsonify({"message": "List empty!"}), 400

# Get all users
@app.route('/user',methods=['GET'])
def get_users():
    try:
        all_users = User.query.all()
        result = users_schema.dump(all_users)

        return jsonify(result),200
    except Exception:
        db.session.rollback()
        return jsonify({"message": "List empty!"}), 400

# Get all localads
@app.route('/localad',methods=['GET'])
def get_localads():

    try:
        all_localads = LocalAD.query.all()
        result = localads_schema.dump(all_localads)

        return jsonify(result),200

    except Exception:
        db.session.rollback()
        return jsonify({"message": "List empty!"}), 400


# Get single public ad
@app.route('/ad/<id>',methods=['GET'])
def get_publicad(id):

    try:
        publicad = PublicAD.query.get(id)
        return publicad_schema.jsonify(publicad),200

    except Exception:
        db.session.rollback()
        return jsonify({"message": "No such id found!"}), 404

# Get single city
@app.route('/city/<id>',methods=['GET'])
def get_city(id):
    try:
        city = City.query.get(id)
        return city_schema.jsonify(city)
    except Exception:
        db.session.rollback()
        return jsonify({"message": "No such id found!"}), 404

# Get single user
@app.route('/user/<id>',methods=['GET'])
def get_user(id):
    try:
        user = User.query.get(id)
        return user_schema.jsonify(user)
    except Exception:
        db.session.rollback()
        return jsonify({"message": "No such id found!"}), 404

# Get single local ad
@app.route('/localad/<id>',methods=['GET'])
def get_localad(id):
    try:
        localad = LocalAD.query.get(id)
        return localad_schema.jsonify(localad)
    except Exception:
        db.session.rollback()
        return jsonify({"message": "No such id found!"}), 404

# Update a public ad
@app.route('/ad/<id>',methods=['PUT'])
def update_publicad(id):
    try:
        publicad = PublicAD.query.get(id)

        title = request.json['title']
        author = request.json['author']
        price = request.json['price']

        publicad.title = title
        publicad.author = author
        publicad.price = price

        db.session.commit()
        #return publicad_schema.jsonify(publicad)
        return jsonify({"message":"Public ad ({}) updated successfully".format(publicad.title)}),200
    except Exception:
        db.session.rollback()
        return jsonify({"message":"Ups something went wrong!"}),400

# Update a user
@app.route('/user/<id>',methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get(id)

        fullname = request.json['fullname']
        email = request.json['email']
        password = request.json['password']
        phone = request.json['phone']
        city_name = request.json['city_name']

        password = bcrypt.generate_password_hash(password).decode('utf-8')
        # bcrypt.check_password_hash(pw_hash, 'hunter2')  # returns True

        user.fullname = fullname
        user.email = email
        user.password = password
        user.phone = phone
        user.city_name = city_name

        db.session.commit()
        #return user_schema.jsonify(user)
        return jsonify({'message':'User {} updated successfully'.format(user.fullname)}),200
    except Exception:
        db.session.rollback()
        return jsonify({"message":"Ups something went wrong!"}),400

# Update a local ad
@app.route('/localad/<id>',methods=['PUT'])
def update_localad(id):
    try:
        localad = LocalAD.query.get(id)

        title = request.json['title']
        price = request.json['price']

        localad.title = title
        localad.price = price

        db.session.commit()
        #return localad_schema.jsonify(localad)
        return jsonify({'message': 'Local ad ({}) updated successfully'.format(localad.title)}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"message":"Ups something went wrong!"}),400

# Delete a public ad
@app.route('/ad/<id>',methods=['DELETE'])
def delete_publicad(id):
    try:
        publicad = PublicAD.query.get(id)
        db.session.delete(publicad)
        db.session.commit()
       #return publicad_schema.jsonify(publicad)
        return jsonify({'message': 'Public ad with id({}) deleted successfully'.format(publicad.id)}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"message": "No such id found!"}), 404
# Delete a city
@app.route('/city/<id>',methods=['DELETE'])
def delete_city(id):
    try:
        city = City.query.get(id)
        db.session.delete(city)
        db.session.commit()
        #return city_schema.jsonify(city)
        return jsonify({'message': 'City with id({}) deleted successfully'.format(city.id)}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"message": "No such id found!"}), 404

# Delete a user
@app.route('/user/<id>',methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        #return user_schema.jsonify(user)
        return jsonify({'message': 'User with id({}) deleted successfully'.format(user.id)}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"message": "No such id found!"}), 404

# Delete a local ad
@app.route('/localad/<id>',methods=['DELETE'])
def delete_localad(id):
    try:
        localad = LocalAD.query.get(id)
        db.session.delete(localad)
        db.session.commit()
        #return localad_schema.jsonify(localad)
        return jsonify({'message': 'Local ad with id({}) deleted successfully'.format(localad.id)}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"message": "No such id found!"}), 404

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
