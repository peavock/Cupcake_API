"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "emmadog2171"


connect_db(app)
# db.create_all()

@app.route('/')
def show_index():
    return render_template("plain_index.html")

# @app.route('/')
# def show_index():
#     cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
#     return render_template("plain_index.html", cupcakes = cupcakes)

@app.route('/api/cupcakes')
def show_cupcakes():
    """return and show data about all cupcakes"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def show_inidividual_cupcake(cupcake_id):
    """show info about individual cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake = cupcake.serialize())

@app.route("/api/cupcakes", methods = ["POST"])
def create_cupcake():

    """send post request to create new cupcake"""
    new_cupcake = Cupcake(
        flavor = request.json["flavor"],
        rating = request.json["rating"],
        size = request.json["size"],
        image = request.json["image"] or None
    )
    print(new_cupcake)

    db.session.add(new_cupcake)
    db.session.commit()

    response_json = jsonify(cupcake = new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ["PATCH"])
def update_cupcake(cupcake_id):
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor',cupcake.flavor)
    cupcake.size = request.json.get('size',cupcake.size)
    cupcake.rating = request.json.get('rating',cupcake.rating)
    cupcake.image = request.json.get('image',cupcake.image)

    db.session.commit()

    response_json = jsonify(cupcake = cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message = "deleted the cupcake",)