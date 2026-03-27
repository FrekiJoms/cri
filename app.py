from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

users = {
    'gwapo@bisu.edu.ph' : ['admin123','admin'],
    'pangit@bisu.edu.ph' : ['user123','user']
}

@app.route('/')
def home():
    return 'KINSA KA OOOIIIEEEEE'

@app.route('/admindashboard')
def admindashboard():
    return render_template('admindashboard.html')

@app.route('/userdashboard')
def userdashboard():
    return render_template('userdashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            if users[username][0] == password and users[username][1] == 'admin':
                return render_template('admindashboard.html', massage=username)
            else:
                return render_template('userdashboard.html', massage=username)           
        else:
             return render_template('login.html', massage='Invalid username or password')        
    return render_template('login.html', massage='')  


if __name__ == '__main__':
    app.run(debug=True)


