from flask import Flask, render_template, redirect,url_for,request,flash
from flask_login import LoginManager ,UserMixin,login_user,login_required,logout_user
from flask_login import current_user
app=Flask(__name__)
app.config['SECRET_KEY']='your_secret_key'
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
users={'user1':{'password':'password123'}}
class User(UserMixin):
    def _init_(self,id):
        self.id=id
@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None

@app.route('/')
@login_required
def  home():
    return render_template('home.html',name = current_user.id)
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
    
        if username in users and users[username]['password']==password:
            user=User(username)
            login_user(user)
            return ('valid password')
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    #return render_template('login.html')
if __name__=='__main__':
    app.run(debug=True)
    