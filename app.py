import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask , render_template , request , redirect , session , url_for , flash
from werkzeug.security import generate_password_hash , check_password_hash
from flask_sqlalchemy import SQLAlchemy
import joblib
import papermill as pm
import sys
from datetime import datetime
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized

# import key_secret, clientId, clientSecret from app_secrets file
from app_secrets import *

app = Flask(__name__)

app.secret_key = key_secret

# Configure Sql Alchemy to work with flask

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


app.config['GOOGLE_OAUTH_CLIENT_ID'] = clientId
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = clientSecret

google_bp = make_google_blueprint(
    client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
    client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_to="mainpage",
    offline=True,  # Add this to enable refresh tokens
    reprompt_consent=True,
)
app.register_blueprint(google_bp, url_prefix="/google-login")

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



# Create a database to store English Reviews and predictions.
class EnglishReview(db.Model):
    id = db.Column(db.Integer , primary_key = True) 
    review_text = db.Column(db.Text , nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    prediction = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# Similar for Romanized Nepali Review
class RomanReview(db.Model):
    id = db.Column(db.Integer , primary_key = True) 
    review_text = db.Column(db.Text , nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    prediction = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class NepaliReview(db.Model):
    id = db.Column(db.Integer , primary_key = True) 
    review_text = db.Column(db.Text , nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    prediction = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    


def get_username():
    return session.get('username', None)

@app.context_processor
def inject_username():
    return dict(username=get_username())

# App Routing 

@app.route("/")
def index():
        if "username" in session:
              return render_template(("home.html"))
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
 


@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google.", "error")
        return False
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Failed to fetch user info from Google.", "error")
        return False
    user_info = resp.json()
    google_name = user_info.get("name", "User")
    google_email = user_info["email"]

    user = User.query.filter_by(email=google_email).first()
    if not user:
        user = User(username=google_name, email=google_email)
        user.set_password("default_password")
        db.session.add(user)
        db.session.commit()
    session['username'] = user.username
    flash("Successfully signed in with Google.", "success")
    # Return False to prevent Flask-Dance from automatically saving the token
    return False


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
               
          
     return render_template("register.html")

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
    rating = int(request.form['rating'])
    review = request.form.get('review').strip()
    
    current_user = User.query.filter_by(username=session['username']).first()

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
        # import json

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
            
            
            
            svm_prediction = "Fake" if "SVM Prediction: Fake" in prediction_output else "Real"
            rf_prediction = "Fake" if "Random Forest Prediction: Fake" in prediction_output else "Real"
            lr_prediction = "Fake" if "Logistic Regression Prediction: Fake" in prediction_output else "Real"
            
            predictions = [svm_prediction, rf_prediction, lr_prediction]
            majority_prediction = max(set(predictions), key=predictions.count)
            
            
            current_user = User.query.filter_by(username=session['username']).first()
            
            if current_user:
                new_review = EnglishReview(
                    review_text = review,
                    rating = int(rating),
                    prediction = majority_prediction,
                    user_id = current_user.id
                    
                )
                db.session.add(new_review)
                db.session.commit()
            
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




#Route to Nepali Page

@app.route('/nepali')
def nepali():
    if "username" in session:
        username = session['username']
        return render_template('nepali.html', username=username)
    return redirect(url_for('login'))




@app.route('/Romanized_Nepali' , methods = ['POST'])
def Romanized_Nepali():
    nr_input_rating = int(request.form['rating'])
    nr_input_review = request.form.get('review').strip()

    nr_input_notebook = r'C:\Rozanne\Minor Project\file.ipynb'
    nr_output_notebook = r'C:\Rozanne\Minor Project\file_OUTPUT.ipynb'

    try:
        pm.execute_notebook(
            nr_input_notebook,
            nr_output_notebook,
            parameters= {'nr_input_rating' : nr_input_rating , 'nr_input_review' : nr_input_review}
        ) 

        from nbformat import read

        with open(nr_output_notebook , 'r' , encoding = 'utf-8') as f:
             nbnr = read(f, as_version= 4)

        
        prediction_output = None
        for cell in nbnr.cells:
            if cell.cell_type == 'code' and 'print(' in cell.source:
                outputs = cell.outputs
                if outputs:
                    # for output in outputs:
                    #     if 'text' in output:
                    #         prediction_output = output['text']
                    #         break
                    for output in cell.outputs:
                        if hasattr(output, 'text'):
                            prediction_output = output.text.strip()
                            
        if prediction_output:
            
            prediction = 'Fake' if "FAKE" in prediction_output else "Real"
            current_user = User.query.filter_by(username=session['username']).first()
            
            if current_user:
                new_review = RomanReview(
                    review_text =nr_input_review,
                    rating = nr_input_rating,
                    prediction = prediction,
                    user_id = current_user.id
                )
                db.session.add(new_review)
                db.session.commit()
            
            
            
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

        return redirect(url_for('nepali'))

    except Exception as e:
        print(f"Error executing notebook: {str(e)}")
        flash("Error processing your review. Please try again.", "error")
        return redirect(url_for('nepali'))



@app.route('/Devnagari_Nepali' , methods = ['POST'])
def Devnagari_Nepali():
    n_input_rating = int(request.form['rating'])
    n_input_review = request.form.get('review').strip()

    n_input_notebook = r'Input_devnagari.ipynb'
    n_output_notebook = r'devnagari_OUTPUT.ipynb'

    try:
        pm.execute_notebook(
            n_input_notebook,
            n_output_notebook,
            parameters= {'n_input_rating' : n_input_rating , 'n_input_review' : n_input_review}
        ) 

        from nbformat import read

        with open(n_output_notebook , 'r' , encoding = 'utf-8') as f:
             nbnr = read(f, as_version= 4)

        
        prediction_output = None
        for cell in nbnr.cells:
            if cell.cell_type == 'code' and 'print(' in cell.source:
                outputs = cell.outputs
                if outputs:
                    for output in outputs:
                        if 'text' in output:
                            prediction_output = output['text']
                            break

        if prediction_output:
            
            label_text = 'Fake' if "Fake" in prediction_output else "Real"
            current_user = User.query.filter_by(username=session['username']).first()
            
            if current_user:
                new_review = NepaliReview(
                    review_text =n_input_review,
                    rating = n_input_rating,
                    prediction = label_text,
                    user_id = current_user.id
                )
                db.session.add(new_review)
                db.session.commit()
            
            
            
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

        return redirect(url_for('nepali'))

    except Exception as e:
        print(f"Error executing notebook: {str(e)}")
        flash("Error processing your review. Please try again.", "error")
        return redirect(url_for('nepali'))



@app.route('/historypage')
def historypage():
    if 'username' in session:
        username = session['username']
        current_user = User.query.filter_by(username=username).first()
        
        english_review = EnglishReview.query.filter_by(user_id = current_user.id).all()
        roman_review = RomanReview.query.filter_by(user_id = current_user.id).all()
        nepali_review = NepaliReview.query.filter_by(user_id= current_user.id).all()
        
        # # Debug: Print number of reviews fetched
        # print(f"English Reviews: {len(english_review)}")
        # print(f"Nepali Reviews: {len(roman_review)}")
        
        return render_template('history.html', 
                               username= username,
                               english_review=english_review,
                               roman_review=roman_review,
                               nepali_review = nepali_review
                               )
    
    return redirect(url_for('login'))



if  __name__ == "__main__" :
    with app.app_context():
          db.create_all()
    app.run(debug = True)