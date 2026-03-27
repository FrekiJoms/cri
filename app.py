from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

users = {
    'gwapo@bisu.edu.ph' : ['admin123','admin'],
    'pangit@bisu.edu.ph' : ['user123','user']
}

products = [
    {
        'id': 10,
        'name': 'Product 10',
        'base_price': 120.00,
        'price_history': [
            {
                'old_price': None,
                'new_price': 120.00,
                'updated_by': 'System',
                'timestamp': '2026-03-27 09:00'
            }
        ]
    },
    {
        'id': 11,
        'name': 'Product 11',
        'base_price': 245.50,
        'price_history': [
            {
                'old_price': None,
                'new_price': 245.50,
                'updated_by': 'System',
                'timestamp': '2026-03-27 09:00'
            }
        ]
    }
]

@app.route('/')
def home():
    return 'KINSA KA OOOIIIEEEEE'

@app.route('/admindashboard')
def admindashboard():
    return render_template('admindashboard.html')

@app.route('/userdashboard')
def userdashboard():
    return render_template('userdashboard.html', username='User', role='user')

@app.route('/userdashboard/<section>')
def userdashboard_section(section):
    if section == 'pricing':
        return render_template(
            'pricingdashboard.html',
            username='User',
            role='user',
            products=products
        )
    elif section == 'discount':
        return render_template(
            'discountdashboard.html',
            username='User',
            role='user'
        )
    elif section == 'settings':
        return render_template(
            'settingsdashboard.html',
            username='User',
            role='user'
        )
    return render_template('userdashboard.html', username='User', role='user')

@app.route('/userdashboard/pricing/update', methods=['POST'])
def update_pricing():
    product_id = request.form['product_id']
    price = request.form['price']

    for product in products:
        if str(product['id']) == product_id:
            old_price = product['base_price']
            product['base_price'] = float(price)
            product['price_history'].append(
                {
                    'old_price': old_price,
                    'new_price': float(price),
                    'updated_by': 'User',
                    'timestamp': 'Updated'
                }
            )
            break

    return render_template(
        'pricingdashboard.html',
        username='User',
        role='user',
        products=products
    )

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            if users[username][0] == password and users[username][1] == 'admin':
                return render_template('admindashboard.html', massage=username)
            else:
                return render_template(
                    'userdashboard.html',
                    massage=username,
                    username=username,
                    role=users[username][1]
                )           
        else:
             return render_template('login.html', massage='Invalid username or password')        
    return render_template('login.html', massage='')  


if __name__ == '__main__':
    app.run(debug=True)
