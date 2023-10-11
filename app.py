from flask import Flask, request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from urllib import parse

#init app
app = Flask(__name__)
"""#docker app
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')"""
#local app
username = 'postgres'
password = parse.quote('@Rc.)))))')
database = 'arcapitest'

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@localhost:5432/{database}"

db =SQLAlchemy(app)

#models
class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(80),unique=True,nullable=False)
    email= db.Column(db.String(120),unique=True,nullable=False)

    def __init__(self,username,email):
        self.username = username
        self.email = email
    
    def json(self):
        return {'id':self.id, 'username':self.username, 'email':self.email}

#routes
#create a test route
@app.route('/status',methods=['GET'])
def test():
    try:
        return make_response(jsonify({'status':'OK'}),200)
    except  Exception as e:
        return make_response(jsonify({'status':'error'}),500)

#create a user
@app.route('/user',methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'],email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message':'user created'}),201)
    
    except  Exception as e:
        return make_response(jsonify({'message':'error user not created' + str(e)}),500)
    
#get all users
@app.route('/users',methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify({'users': [user.json() for user in users]}),200)

    except Exception as e:
        return make_response(jsonify({'message':'error getting users'}),500)

#get user by id
@app.route('/users/<int:id>',methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'user': user.json()}),200)
        return make_response(jsonify({'message': 'user mot found'}),404)

    except Exception as e:
        return make_response(jsonify({'message':'error getting user'}),500)

#update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'user updated'}),200)
        return make_response(jsonify({'message': 'user mot found'}),404)
    
    except Exception as e:
         return make_response(jsonify({'message':'error updating user'}),500)

#delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}),200)
        return make_response(jsonify({'message': 'user mot found'}),404)
    
    except Exception as e:
         return make_response(jsonify({'message':'error deleting user'}),500)
         pass

if __name__ == '__main__':
    #create db if it doesnt exist    
    with app.app_context():

        db.create_all()
        db.session.commit()
    
    #run the app
    app.run(host='127.0.0.1', port=5050)


    

    


