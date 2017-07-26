from flask import Flask , render_template , request ,redirect , session
from time import localtime, strftime
import dataset
import os
db = dataset.connect("postgres://axhifbkpwevbyr:fde9124d2d41e4d1b127cd0795358912284f8b2d3d17548297914157fdc703bb@ec2-54-204-32-145.compute-1.amazonaws.com:5432/dd4f0ebt1ijhbf")
app=Flask(__name__)
app.secret_key= os.urandom(24)
@app.route("/")
def home():
	return render_template("home.html")
@app.route("/register" , methods=["POST" , "GET"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	else:
		form=request.form
		email = form["email"]
		username = form["username"]
		password = form["password"]
		firstname=form["firstname"]
		gender = form["radios"]
		print gender
		lastname=form["lastname"]
		email = form["email"]
		hometown = form["hometown"]
		website = form["website"]
		password = form["password"]
		usersTable = db["users"]
		entry = {"email" : email ,"username":username , "password":password , "firstname" : firstname , "lastname":lastname , "hometown":hometown , "website" : website , "gender":gender}
		if len(list(usersTable.find(username=username)))==0:
			usersTable.insert(entry)
			return render_template("register.html" , email=email ,username=username , password=password , firstname=firstname , lastname=lastname  , hometown=hometown , website=website , gender=gender)
		else:

			taken = 1
			return render_template("register.html" , taken=taken)

@app.route("/login" , methods=["POST" , "GET"])
def login():
	if request.method == "GET":
		if "failed" in session:
			failed =True
			session.pop("failed", None)
			return render_template("login.html"  , failed=failed )
		if "erorr" in session:
			message= True
			session.pop("erorr", None)
			return render_template("login.html" , message=message )
		if "username" in session:
			return redirect ("/newsfeed")
		return render_template("login.html")
	else:
			form=request.form
			usersTable = db["users"]
			username = form["username"]
			password = form["password"]
			if len(list(usersTable.find(username=username , password=password)))==0:
				session["failed"]="failed"
				return redirect("/login")
			else:
				session["username"]=username
	 			return redirect ("/newsfeed")
@app.route("/newsfeed" , methods=["POST" , "GET"])
def newsfeed():
	if "username" in session:
		if request.method == "GET":
			poststable = db["posts"]
			posts = list(poststable.all())[::-1]
			username=session["username"]
			return render_template("newsfeed.html" , posts=posts , username=username)
		else:
			form=request.form
			username=session["username"]
			status=form["subject"]
			poststable=db["posts"]
			time = strftime("%Y-%m-%d %H:%M:%S", localtime())
			table_entry={"status" : status , "time":time , "username":username}
			print table_entry
			poststable.insert(table_entry)
			posts = list(poststable.all())[::-1]
		return render_template("newsfeed.html" , status=status , posts=posts , username=username)
	else:
		session["erorr"]="Please login first"
		return redirect("/login")
@app.route("/logout")
def logout():
  if "username" in session:
    session.pop("username", None)
    return redirect ("/")
  else:
	return redirect("/")
@app.route("/list")
def showAll():
	if "username" in session:
		users=db["users"]
		allUsers =list(users.all())
		return render_template("lists.html" , users =allUsers)
	else:
		session["erorr"]="Please login first"
		return redirect("/login")
if __name__ == "__main__":
	app.run()