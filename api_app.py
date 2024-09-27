from flask import Flask , render_template , request, redirect, jsonify
from shared_database.models import db, NokiaUser
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nokia.db'
db.init_app(app)


@app.route('/users', methods = ['GET'])
def get_all_users():
    try:
        users = NokiaUser.query.order_by(NokiaUser.date_updated).all()
        users = [user.to_dict() for user in users]
        return jsonify(users),200
    except Exception as e:
        print(f"Get All Error : {e}")
        return jsonify({'error' : 'There is a big error in your system'}),500
    
@app.route('/users', methods = ['POST'])
def add_user():
    try:
        data = request.get_json()
        name = data.get('name')
        
        if(name is None):
            return jsonify({'error':'Please provide a name'}),400
        
        user = NokiaUser(name = name)
    
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()),201
    except Exception as e:
        print(f"Add Error: {e}")
        return jsonify({'error': 'There was an issue adding the user'}),500
    
@app.route('/users/<int:id>', methods = ['DELETE'])
def delete_user(id):
    try:
        user = NokiaUser.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message':'User deleted successfully'}),204
    except Exception as e:
        print(f"Delete Error: {e}")
        return jsonify({'error':'There was a problem deleting the user'}),500

@app.route('/users/<int:id>', methods = ['PATCH'])
def update_user(id):
    try:
        user = NokiaUser.query.get_or_404(id)

        data = request.get_json()
        name = data.get('name')
        
        if(name is None):
            return jsonify({'error':'Please provide a name'}),400
        
        user.name = name
        user.date_updated = datetime.utcnow()
    
        db.session.commit()
        return jsonify(user.to_dict()),201
    except Exception as e:
        print(f"Update Error: {e}")
        return jsonify({'error': 'There was an issue updating the user'}),500
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True,port=5001)