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
class Station(db.Model):
    __tablename__='stations'
    id = db.Column(db.Integer,primary_key=True)
    compno= db.Column(db.String(80),unique=True,nullable=False)
    weathervar= db.Column(db.String(120),nullable=False)
    val= db.Column(db.Float,nullable=False)

    def __init__(self,compno,weathervar,val):
        self.compno = compno
        self.weathervar = weathervar
        self.val = val
    
    def json(self):
        return {'id':self.id, 'compno':self.compno, 'weathervar':self.weathervar, 'val':self.val}

#routes
#create a test route
@app.route('/status',methods=['GET'])
def test():
    try:
        return make_response(jsonify({'status':'OK'}),200)
    except  Exception as e:
        return make_response(jsonify({'status':'error'}),500)

#create a station
@app.route('/station',methods=['POST'])
def create_station():
    try:
        data = request.get_json()
        new_station = Station(compno=data['compno'],weathervar=data['weathervar'],val=data['val'])
        db.session.add(new_station)
        db.session.commit()
        return make_response(jsonify({'message':'station created'}),201)
    
    except  Exception as e:
        return make_response(jsonify({'message':'error station not created' + str(e)}),500)
    
#get all stations
@app.route('/stations',methods=['GET'])
def get_stations():
    try:
        stations = Station.query.all()
        return make_response(jsonify({'stations': [station.json() for station in stations]}),200)

    except Exception as e:
        return make_response(jsonify({'message':'error getting stations'}),500)

#get station by id
@app.route('/stations/<int:id>',methods=['GET'])
def get_station(id):
    try:
        station = Station.query.filter_by(id=id).first()
        if station:
            return make_response(jsonify({'station': station.json()}),200)
        return make_response(jsonify({'message': 'station not found'}),404)

    except Exception as e:
        return make_response(jsonify({'message':'error getting station'}),500)

#update a station
@app.route('/stations/<int:id>', methods=['PUT'])
def update_station(id):
    try:
        
        station = Station.query.filter_by(id=id).first()
        if station:
            data = request.get_json()
            station.compno = data['compno']
            station.weathervar = data['weathervar']
            station.val = data['val']
            db.session.commit()
            return make_response(jsonify({'message': 'station updated'}),200)
        return make_response(jsonify({'message': 'station not found'}),404)
    
    except Exception as e:
         return make_response(jsonify({'message':'error updating station'}),500)

#delete a station
@app.route('/stations/<int:id>', methods=['DELETE'])
def delete_station(id):
    try:
        station = Station.query.filter_by(id=id).first()
        if station:
            db.session.delete(station)
            db.session.commit()
            return make_response(jsonify({'message': 'station deleted'}),200)
        return make_response(jsonify({'message': 'station not found'}),404)
    
    except Exception as e:
         return make_response(jsonify({'message':'error deleting station'}),500)
         pass

if __name__ == '__main__':
    #create db if it doesnt exist    
    with app.app_context():

        db.create_all()
        db.session.commit()
    
    #run the app
    app.run(host='127.0.0.1', port=5050)


    

    


