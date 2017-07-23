from flask import Flask , render_template , request
import dataset
db = dataset.connect("postgres://axhifbkpwevbyr:fde9124d2d41e4d1b127cd0795358912284f8b2d3d17548297914157fdc703bb@ec2-54-204-32-145.compute-1.amazonaws.com:5432/dd4f0ebt1ijhbf")
app=Flask(__name__)
@app.route("/register" , methods=["POST" , "GET"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	else:
		form=request.form
		email = form["email"]
		username = form["username"]
		password = form["password"]
		usersTable = db["users"]
		entry = {"email" : email ,"username":username , "password":password}
		if list(usersTable.find_one(username=username))==[]:
			usersTable.insert(entry)
			return render_template("register.html" , email=email ,username=username , password=password)
		else:
			return "error user is already taken"
@app.route("/login" , methods=["GET" , "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	else :
		username = form["username"]
		password = form["password"]
@app.route("/datatableamin7772001")
def showAll():
	users=db["users"]
	allUsers =list(users.all())
	return render_template("showdatabase.html" , users =allUsers)
if __name__ == "__main__":
	app.run()