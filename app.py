from flask import Flask, render_template, url_for, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        Note = request.form['content']
        new_Note = Todo(content = Note)
        if new_Note.content is not "":
            try:
                db.session.add(new_Note)
                db.session.commit()
                return redirect('/')
            except:
                return "error"
        else:
            return redirect("/")
    else:
        Notes = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',Notes = Notes)

@app.route('/delete/<int:id>')
def delete(id):
    Note = Todo.query.get_or_404(id)
    try:
        db.session.delete(Note)
        db.session.commit()
        return redirect('/')
    except:
        return "error"

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    Note = Todo.query.get_or_404(id)
    if request.method == 'POST':
        Note.content = request.form['content']
        if Note.content is not "":
            try:
                db.session.commit()
                return redirect('/')
            except:
                return "error"
        else:
            return redirect('/')
    else:
        return render_template('update.html',Note=Note)

if __name__ == "__main__":
    app.run()
