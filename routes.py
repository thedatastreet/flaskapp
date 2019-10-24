from flask import Flask, render_template,request, session, redirect, url_for
from models import db, User, Place
from forms import SignUpForm, LoginForm, AddressForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost/flaskapp'
db.init_app(app)

app.secret_key = "test_key"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/signup", methods=['GET','POST'])
def signup():
	if 'email' in session:
		return redirect(url_for("home"))
	form = SignUpForm(request.form)

	print("print session info:", session)
	if request.method == 'POST':
		if form.validate_on_submit() == False:
			print("Form Password:", form.password.data)
			print("Validation failed")
			return render_template("signup.html", form=form)
		else:
			newuser = User(form.first_name.data,form.last_name.data,form.email.data,form.password.data)
			db.session.add(newuser)
			try:
				db.session.commit()
			except:
				db.session.rollback()
				return render_template("signup.html", form=form, error='This email id already exists in the database')
			session['email'] = newuser.email
			print("New user email:"+newuser.email+" and password :"+form.password.data)
			return redirect(url_for('home'))
	elif request.method == 'GET':
		return render_template("signup.html", form=form)

@app.route("/home", methods=['GET','POST'])
def home():
	if 'email' not in session:
		return redirect(url_for("login"))

	form = AddressForm()
	places = []
	my_coordinates = (17.4435,78.3772)

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('home.html',form=form)
		else:
			address = form.address.data
			
			p = Place()
			places = p.query(address)

			return render_template('home.html',form=form, my_coordinates=my_coordinates, places=places)

	elif request.method == 'GET':
		return render_template("home.html",form=form, my_coordinates=my_coordinates, places=places)

@app.route("/login",methods=["GET","POST"])
def login():
	if 'email' in session:
		return redirect(url_for("home"))
	form = LoginForm()

	if request.method == 'POST':
		if form.validate() == False:
			print("Login validation failed")
			return render_template("login.html",form=form)
		else:
			print("Login validation successful")
			email = form.email.data
			password = form.password.data

			user = User.query.filter_by(email=email).first()
			print("retreiving user object:", user)
			print("user password check:", user.check_password(password))
			if user is not None and user.check_password(password):
				session['email'] = form.email.data
				return redirect(url_for("home"))
			else:
				return redirect(url_for("login"))
	elif request.method == 'GET':
		return render_template("login.html",form=form)

@app.route("/logout")
def logout():
	session.pop('email',None)
	return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug='True')