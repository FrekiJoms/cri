# CRI Project Documentation


This project is a small Flask web application that looks like the start of a role-based dashboard system. Right now, the app has a login page, an admin dashboard, a user dashboard, and two extra product/pricing templates that appear to be planned features but are not yet connected to the Flask routes.

From my perspective, this repository is currently in a prototype stage. The UI is mostly hardcoded, the authentication logic is very basic, and there is no database yet. The project still helps me understand the intended direction: users log in, the system checks their role, and then it sends them to the correct dashboard.

## Tech stack I am using

- Python
- Flask
- Jinja2 templates
- HTML and inline CSS
- One standalone CSS file in `static/style.css`

## Current repository structure

```text
cri/
|-- app.py
|-- README.md
|-- static/
|   `-- style.css
`-- templates/
    |-- admindashboard.html
    |-- login.html
    |-- pricingdashboard.html
    |-- productdashboard.html
    `-- userdashboard.html
```

## How the application works right now

### 1. Flask app setup

The main backend file is `app.py`.

It imports:

- `Flask`
- `render_template`
- `redirect`
- `url_for`
- `request`

Only `Flask`, `render_template`, `url_for`, and `request` are actually used. `redirect` is imported but not used yet.

The Flask application is created with:

```python
app = Flask(__name__)
```

### 2. User storage

I am currently storing users in a hardcoded Python dictionary:

```python
users = {
    'gwapo@bisu.edu.ph' : ['admin123','admin'],
    'pangit@bisu.edu.ph' : ['user123','user']
}
```

This means:

- the dictionary key is the username/email
- index `0` is the password
- index `1` is the role

So the app currently knows only two users:

- `gwapo@bisu.edu.ph` with password `admin123` and role `admin`
- `pangit@bisu.edu.ph` with password `user123` and role `user`

There is no registration, no hashing, no database, and no session handling.

### 3. Routes

#### `/`

This is the home route:

```python
@app.route('/')
def home():
    return 'KINSA KA OOOIIIEEEEE'
```

It does not render a page yet. It only returns plain text.

#### `/admindashboard`

This route simply renders the admin dashboard template:

```python
@app.route('/admindashboard')
def admindashboard():
    return render_template('admindashboard.html')
```

There is no protection here, so anyone who knows the URL can open it directly.

#### `/userdashboard`

This route renders the user dashboard template:

```python
@app.route('/userdashboard')
def userdashboard():
    return render_template('userdashboard.html')
```

This also has no access control.

#### `/login`

This is the main working route in the app:

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
```

Behavior:

- `GET /login` loads the login page
- `POST /login` reads form values from the template
- it checks whether the username exists in the `users` dictionary
- if the password matches and the role is `admin`, it renders the admin dashboard
- otherwise, if the username exists but is not admin, it renders the user dashboard
- if the username does not exist, it reloads the login page with an error message

### 4. Login decision logic

The current login logic is:

1. Read `username`
2. Read `password`
3. Check if `username` exists in `users`
4. If it exists and the password matches and the role is `admin`, show admin dashboard
5. Otherwise, show user dashboard
6. If username does not exist, show invalid login message

Important detail: the logic does **not** fully validate non-admin passwords.

Because of this condition:

```python
if users[username][0] == password and users[username][1] == 'admin':
    return render_template('admindashboard.html', massage=username)
else:
    return render_template('userdashboard.html', massage=username)
```

If the username exists but is not an admin, the code goes to the `else` block even if the password is wrong.

That means any existing non-admin username can currently enter the user dashboard without the correct password. For my own understanding, this is the biggest logic bug in the app right now.

## Template-by-template explanation

### `templates/login.html`

This is the login page.

What it contains:

- a centered glass-style login card
- a background image from Unsplash
- a form that posts to `/login`
- two inputs:
  - `username`
  - `password`
- a message placeholder:

```html
<div class="message">{{ message }}</div>
```

Purpose:

- collect login credentials
- display an error message if login fails

Important issue I noticed:

In `app.py`, the template is rendered using `massage=` instead of `message=`:

```python
return render_template('login.html', massage='Invalid username or password')
```

and

```python
return render_template('login.html', massage='')
```

But inside the template, the variable is `{{ message }}`.

So the backend and template variable names do not match. That means the message will not display correctly unless this typo is fixed.

Another thing I noticed is the title text:

```html
<h1>ðŸŒ¿ Welcome</h1>
```

This looks like an encoding issue. It was probably meant to show an emoji.

### `templates/admindashboard.html`

This is the admin dashboard UI.

What it contains:

- a dark sidebar
- links for admin sections like:
  - Dashboard
  - User Management
  - Product Management
  - Orders
  - Inventory
  - Reports
  - Settings
  - Logout
- a main content area with cards for:
  - Users
  - Products
  - Inventory
  - Reports

Purpose:

- provide a placeholder admin interface after login

Current state:

- mostly static
- sidebar links are mostly `#`
- there is no dynamic data loading
- the welcome text always says `Welcome, Administrator`

Even though `app.py` passes `massage=username` when rendering, this template does not use that variable.

### `templates/userdashboard.html`

This is the user dashboard UI.

It is very similar to the admin dashboard, but intended for normal users.

What it contains:

- sidebar navigation
- dashboard cards
- placeholder links

Important issues I noticed:

- the Dashboard link points to `url_for('admindashboard')` instead of `userdashboard`
- there is a typo in the visible link text: `Dasboard`
- one link uses a literal file path:

```html
<a href="pricingdashboard.html" class="btn">Dasboard</a>
```

Since Flask normally serves pages through routes, this link will not work properly unless a route is created for it or the URL is corrected.

There is also an unnecessary script tag:

```html
<script src="https://unpkg.com"></script>
```

It does not appear to be used anywhere.

### `templates/productdashboard.html`

This looks like a planned product management page.

What it contains:

- a form that posts to `/add`
- fields for:
  - product id (stored under `name`)
  - price
- a products table using:

```jinja2
{% for product in products %}
```

Expected backend behavior:

- a route should provide a `products` list
- a route `/add` should add a product
- a route `/delete/<index>` should remove a product

Current state:

- none of those Flask routes exist in `app.py`
- this page cannot work yet with the current backend

Also, the label says `Product Id`, but the input name is `name`, which is inconsistent.

### `templates/pricingdashboard.html`

This looks like a separate pricing management page.

What it contains:

- an add product form posting to `/add`
- an update price form posting to `/update`
- a list of products rendered from:

```jinja2
{% for name, history in products.items() %}
```

- a history link:

```html
<a href="/history/{{ name }}">View History</a>
```

Expected backend behavior:

- `products` should be a dictionary
- each product should have a price history
- routes should exist for:
  - `/add`
  - `/update`
  - `/history/<name>`

Current state:

- none of these routes exist in `app.py`
- this page is currently disconnected from the running application

### `static/style.css`

This stylesheet defines:

- body styling
- container layout
- sidebar styling
- signup-form styling
- input and button styling
- terms section styling

Current state:

- this file is not linked from the templates I reviewed
- most templates use inline `<style>` blocks instead

So for now, `static/style.css` exists in the project but is effectively unused.

## Data flow I currently have in the app

The active flow is:

1. User opens `/login`
2. Flask renders `login.html`
3. User submits username and password
4. Flask checks the hardcoded `users` dictionary
5. Flask renders either:
   - `admindashboard.html`
   - `userdashboard.html`
   - or `login.html` again for invalid username

This means the app is currently rendering pages directly after form submission rather than redirecting to protected pages with session-based login state.

## What is working right now

- Flask app starts from `app.py`
- login page can load
- form submission can reach the backend
- admin user can be routed to the admin dashboard
- known non-admin user can be routed to the user dashboard
- admin and user dashboard templates can render

## What is incomplete or broken right now

### Authentication issues

- passwords are stored in plain text
- no session management
- no logout logic beyond a link back to `/login`
- admin and user dashboard routes are not protected
- non-admin password validation is flawed

### Template/backend mismatches

- `massage` is passed from Flask, but `message` is used in `login.html`
- passed username values are not displayed in the dashboard templates

### Routing gaps

- no route for `productdashboard.html`
- no route for `pricingdashboard.html`
- no route for `/add`
- no route for `/update`
- no route for `/delete/<index>`
- no route for `/history/<name>`

### Navigation issues

- user dashboard links to the admin dashboard
- one link points to `pricingdashboard.html` directly instead of a Flask route
- most links are placeholders

### UI/code organization issues

- CSS is duplicated inline across templates
- `static/style.css` is not connected
- there is an unused external script in `userdashboard.html`
- some text shows encoding problems

## My mental model of the project

If I explain this project to myself simply:

This is a starter Flask dashboard app with two user roles: admin and regular user. The only real backend feature implemented so far is login routing based on a hardcoded dictionary. The dashboards are mostly static UI shells. Product and pricing management pages were started in the templates folder, but their backend logic has not been built yet.

## If I continue developing this project, my next priorities should be

1. Fix the login logic so password validation is correct for all users.
2. Rename `massage` to `message` everywhere.
3. Add proper sessions so users stay logged in.
4. Protect `/admindashboard` and `/userdashboard` by role.
5. Decide whether `productdashboard.html` and `pricingdashboard.html` are both needed or should be merged.
6. Add real Flask routes for product and pricing operations.
7. Move repeated inline CSS into shared static files.
8. Replace hardcoded users with a database.

## How I can run the project

From the project root:

```bash
python app.py
```

Then I can open:

```text
http://127.0.0.1:5000/login
```

## Test credentials currently hardcoded

- Admin
  - username: `gwapo@bisu.edu.ph`
  - password: `admin123`
- User
  - username: `pangit@bisu.edu.ph`
  - password: `user123`

## Final summary for myself

This codebase is a basic role-based Flask prototype. The main idea is already visible: log in, identify the user role, and show the correct dashboard. However, most of the project is still UI scaffolding and unfinished backend integration. For my own understanding, the key thing is that only the login route is partially functional, while the product/pricing features and secure authentication flow are not implemented yet.
