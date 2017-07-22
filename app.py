from flask import Flask , render_template , request
import dataset
app=Flask(__name__)
@app.route('/register')
def site():
	form=request.form
	email = form["email"]
	firstname = form["firstname"]
	password = form["password"]
	
if __name__ == "__main__":
	app.run()