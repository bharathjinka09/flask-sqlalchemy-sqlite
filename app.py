from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
from flask_classful import FlaskView
from flask_sqlalchemy import SQLAlchemy

# we'll make a list to hold some quotes for our app
quotes = [
    "A noble spirit embiggens the smallest man! ~ Jebediah Springfield",
    "If there is a way to do it better... find it. ~ Thomas Edison",
    "No one knows what he can do till he tries. ~ Publilius Syrus"
]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super secret key'

# models
db = SQLAlchemy(app)
class students(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))  
   address = db.Column(db.String(200))
   pincode = db.Column(db.String(10))

def __init__(self, name, city, address,pincode):
   self.name = name
   self.city = city
   self.address = address
   self.pincode = pincode

'''
https://www.tutorialspoint.com/flask/flask_sqlalchemy.htm

db.session.add(model object) − inserts a record into mapped table

db.session.delete(model object) − deletes record from table

model.query.all() − retrieves all records from table (corresponding to SELECT query).
'''


# http://localhost:5000/quotes/
# http://localhost:5000/quotes/<name>/
class QuotesView(FlaskView):
    def index(self):
        return "<br>".join(quotes)

    # http://localhost:5000/quotes/<name>/
    # http://localhost:5000/quotes/bharath/
    def get(self, name):
        print("get request", name)
        return jsonify({"message": name})

    # http://localhost:5000/quotes/
    def post(self):
        print('post body_payload', request.get_json())
        body_payload = request.get_json()
        return jsonify({"message": body_payload})
    
    # http://localhost:5000/quotes/4546/
    def patch(self, id):
        print(f'patch {id}', request.get_json())
        body_payload = request.get_json()
        return jsonify({"message": body_payload})

    # http://localhost:5000/quotes/4546/
    def delete(self, id):
        print('delete', id)
        return jsonify({"message": f"Deleted {id}"})

QuotesView.register(app)

# http://localhost:5000/show_all/ (Home page)
@app.route('/show_all')
def show_all():
    return render_template('show_all.html', students=students.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      print(request.form,'request.form')
      
      if 'address' in request.form and 'pincode' in request.form:
         student = students(name=request.form['name'], city=request.form['city'],
            address=request.form['address'], pincode=request.form['pincode'])        
      else:
         student = students(name=request.form['name'], city=request.form['city'],
            address=request.form['addr'], pincode=request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')


if __name__ == '__main__':
    app.run(debug=True)