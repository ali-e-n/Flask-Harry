# flask Minimal app code 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# this is the model for the database    
class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def Home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = TodoModel(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

        
    alltodo = TodoModel.query.all()
    return render_template('index.html', alltodo=alltodo)

# @route is a decorator which tells the app which URL should call the associated function 
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = TodoModel.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('Home'))
    todo = TodoModel.query.filter_by(id=id).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:id>')

def delete(id):
    todo = TodoModel.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('Home'))

@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        search_query = request.args.get('search')
        search_query = f"%{search_query}%"  # Adding wildcard '%' for partial matching
        todos = TodoModel.query.filter(TodoModel.title.like(search_query)).all()
        return render_template('search.html', todos=todos)
    return redirect(url_for('Home'))




@app.route('/about')
def about():
    return render_template('about.html')

    
# this is the main app which will run the app
if __name__ == '__main__':
    app.run(debug=True)

    


