from flask import Flask , render_template , request , redirect , session , url_for , flash
from werkzeug.security import generate_password_hash , check_password_hash
from flask_sqlalchemy import SQLAlchemy
import joblib
import papermill as pm
import sys


app = Flask(__name__)

app.secret_key = "Your_secret_key"

# Configure Sql Alchemy to work with flask

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Creating a database

db = SQLAlchemy(app)

# Database Model  : Single row within database

class User(db.Model):
      
      #Class Variables Creation

    id = db.Column(db.Integer , primary_key = True) 
    username = db.Column(db.String(20) , unique = True , nullable = False) 
    email = db.Column(db.String(30), unique = True , nullable = False)
    password_hash = db.Column(db.String(128) , nullable = False) 

   
    def set_password(self, password):
         self.password_hash = generate_password_hash(password)
    
    
    def check_password(self, password):
         return check_password_hash(self.password_hash,password)





# App Routing 

@app.route("/")
def index():
        if "username" in session:
              return redirect(url_for("mainpage"))
        else:
            return redirect(url_for('home'))


# Home


@app.route('/home')
def home():
    return render_template('home.html')

# Login

@app.route("/Login", methods = ['GET', 'POST'])

def login():
     
     # Collect info from the form
     if request.method  == 'POST':
          username = request.form.get('username')
          password = request.form.get('password')

          
     # Check if its in the database

          user = User.query.filter_by(username = username).first()
          if user and user.check_password(password) :
               session ['username'] = username
               return redirect(url_for('mainpage'))
    
          else:
               flash("Invalid username or password", "error")
               return render_template("login.html")

          
     return render_template("login.html")


#Otherwise ask them to register


# Register

@app.route("/register", methods = ['GET' , 'POST'])

def register():
     if request.method == 'POST':
          username = request.form.get('username')
          email = request.form.get('email')
          password = request.form.get('password')
     
     # Checking if user already exists
          existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

          if existing_user:
               flash("Username already registered!", "error")
               return redirect(url_for('login'))
          else :
               new_user = User(username=username , email = email)
               new_user.set_password(password)
               db.session.add(new_user)
               db.session.commit()
               flash("User created sucessfully" , "success")

               
          
     return render_template("login.html")

# Main page
@app.route("/mainpage")
def mainpage():
    if "username" in session:
        username = session['username']
        return render_template('mainpage.html', username=username)
    return redirect(url_for('login'))



#Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route("/submit_review", methods=['POST'])
def submit_review():
    rating = float(request.form['rating'])
    review = request.form.get('review').strip()

    # Paths for input/output notebooks
    input_notebook = r'C:/Rozanne/Minor Project/text_processing.ipynb'
    output_notebook = r'C:/Rozanne/Minor Project/text_processing_OUTPUT.ipynb'

    try:
        # Execute the notebook with parameters
        pm.execute_notebook(
            input_notebook,
            output_notebook,
            parameters={'input_review': review, 'input_rating': rating}
        )

        # Extract predictions from the output notebook
        from nbformat import read
        import json

        with open(output_notebook, 'r', encoding='utf-8') as f:
            nb = read(f, as_version=4)

        # Get the last cell's output (where predictions are printed)
        prediction_output = None
        for cell in nb.cells:
            if cell.cell_type == 'code' and 'print(' in cell.source:
                outputs = cell.outputs
                if outputs:
                    for output in outputs:
                        if 'text' in output:
                            prediction_output = output['text']
                            break

        if prediction_output:
            
            formatted_output = prediction_output.replace("\n", "<br>")  
            formatted_output = "<br>".join([f"<strong>{line}</strong>" for line in formatted_output.split("<br>")])
            styled_message = f"""
                <div style='background-color:#f8f9fa; padding:15px; margin-top:20px;
                font-size:16px; font-weight:normal; color:#333; line-height:1.5; white-space:pre-line;'>
                <span style='font-size:20px; font-weight:bold; color:#0056b3;'>Prediction Result:</span><br>{formatted_output}
                </div>
            """
            flash(styled_message, "success")



        else:
            flash("Review processed, but no prediction found.", "warning")

        return redirect(url_for('mainpage'))

    except Exception as e:
        print(f"Error executing notebook: {str(e)}")
        flash("Error processing your review. Please try again.", "error")
        return redirect(url_for('mainpage'))



if  __name__ == "__main__" :
    with app.app_context():
          db.create_all()
    app.run(debug = True)