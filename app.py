from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), unique=True)
    l_name = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10), nullable=True)

    pr = db.relationship('Orders', backref='clients', uselist=False)

    def __repr__(self):
        return f'id = {self.id}, name: {self.f_name}, surname: {self.l_name}, gender: {self.gender}'

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    total = db.Column(db.String(100))

    def __repr__(self):
        return f"id = {self.id}, date: {self.date}, owner: {self.client_id}, total: {self.total}"

db.create_all()

@app.route('/')
def ListAll():
    try:
        info0 = Clients.query.all()
        info1 = Orders.query.all()
    except:
        info0 = "Ошибка чтения из БД"
        info1 = info0

    return render_template("ListAll.html", clients = info0, orders = info1)

@app.route('/orders/')
def ListOrders():
    if not bool(Clients.query.filter_by(id = request.args.get('client_id')).first()):
        c = 'incorrect client'
        o = []
    else:
        c_id = request.args.get('client_id')
        o_id = request.args.get('order_id')
        c = Clients.query.get(c_id)
        flag = Orders.query.get(o_id)
        if str(flag.client_id) == str(c_id):
            o = flag
        else:
            o = Orders.query.filter(Orders.client_id == c_id).all()
    return render_template("ListOrders.html", client = c, orders = o)

@app.route('/delete/')
def Delete():
    try:
        c_id = request.args.get('client_id')
        c = Clients.query.get(c_id)
        o = Orders.query.filter(Orders.client_id == c_id).all()
        db.session.delete(c)
        for i in o:
            db.session.delete(i)
        db.session.commit()
    except Exception:
        o_id = request.args.get('order_id')
        o = Orders.query.get(o_id)
        db.session.delete(o)
        db.session.commit()
    return render_template("Delete.html")

@app.route('/NewOrder/')
def OrderCreation():
    no = Orders(date = request.args.get('date'),
                client_id = request.args.get('client_id'),
                total = request.args.get('total'))
    db.session.add(no)
    db.session.commit()
    return render_template('Created.html')

@app.route('/NewClient/')
def ClientCreation():
    nc = Clients(f_name = request.args.get('fname'),
                l_name = request.args.get('lname'),
                gender = request.args.get('gender'))
    db.session.add(nc)
    db.session.commit()
    return render_template('Created.html')

@app.route('/ORupdate/')
def O_UPD():
    o_id = request.args.get('id')
    o = Orders.query.get(o_id)
    if bool(request.args.get('data')):
        o.data = request.args.get('data')
    if bool(request.args.get('client_id')):
        o.client_id = request.args.get('client_id')
    if bool(request.args.get('total')):
        o.total = request.args.get('total')
    db.session.commit()
    return render_template('Updated.html', object = o)


@app.route('/CLupdate/')
def C_UPD():
    c_id = request.args.get('id')
    c = Orders.query.get(c_id)
    if bool(request.args.get('data')):
        c.data = request.args.get('data')
    if bool(request.args.get('client_id')):
        c.client_id = request.args.get('client_id')
    if bool(request.args.get('total')):
        c.total = request.args.get('total')
    db.session.commit()
    return render_template('Updated.html', object=c)

if __name__ == '__main__':
    app.run(debug=True)

