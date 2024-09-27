from flask import Flask , render_template , request, redirect
from shared_database.models import db, NokiaUser
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nokia.db'
db.init_app(app)


@app.route('/')
def index():
    try:
        users = NokiaUser.query.order_by(NokiaUser.date_updated).all()
        return render_template('index.html',users = users)
    except:
        return 'There is a big error in your system'
    
@app.route('/add', methods = ['POST'])
def add():
    name = request.form['uname']
    user = NokiaUser(name = name)
    try:
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your task'
    
@app.route('/delete/<int:id>')
def delete(id):
    user = NokiaUser.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods = ['POST','GET'])
def update(id):
    user = NokiaUser.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['uname']
        user.date_updated = datetime.utcnow()
        db.session.commit()
        return redirect('/')
    else:
        return render_template('update.html',user = user)
    
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True,port=5000)