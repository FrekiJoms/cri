from datetime import date, datetime
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = "cri-demo-secret-key"

users = {
    "gwapo@bisu.edu.ph": {"password": "admin123", "role": "admin"},
    "pangit@bisu.edu.ph": {"password": "user123", "role": "user"},
}

products = [
    {
        "id": 10,
        "name": "Product 10",
        "base_price": 120.00,
        "price_history": [
            {
                "old_price": None,
                "new_price": 120.00,
                "updated_by": "System Seed",
                "timestamp": "2026-03-27 09:00",
            }
        ],
    },
    {
        "id": 11,
        "name": "Product 11",
        "base_price": 245.50,
        "price_history": [
            {
                "old_price": None,
                "new_price": 245.50,
                "updated_by": "System Seed",
                "timestamp": "2026-03-27 09:00",
            }
        ],
    },
    {
        "id": 12,
        "name": "Product 12",
        "base_price": 315.75,
        "price_history": [
            {
                "old_price": None,
                "new_price": 315.75,
                "updated_by": "System Seed",
                "timestamp": "2026-03-27 09:00",
            }
        ],
    },
]

discount_rules = []


def current_user():
    username = session.get("username")
    if not username:
        return None
    user = users.get(username)
    if not user:
        return None
    return {"username": username, "role": user["role"]}


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user():
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            return redirect(url_for("login"))
        if user["role"] != "admin":
            flash("Only admin users can update prices.", "error")
            return redirect(url_for("userdashboard_section", section="pricing"))
        return view_func(*args, **kwargs)

    return wrapper


def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def compute_discounted_price(base_price, percent):
    discounted_price = base_price - (base_price * (percent / 100))
    return round(discounted_price, 2)


def build_discount_views():
    today = date.today()
    rule_views = []
    active_rules = []

    for rule in discount_rules:
        product = get_product(rule["product_id"])
        if not product:
            continue

        start_date = datetime.strptime(rule["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(rule["end_date"], "%Y-%m-%d").date()
        is_active = start_date <= today <= end_date

        view = {
            **rule,
            "product_name": product["name"],
            "base_price": product["base_price"],
            "is_active": is_active,
        }
        rule_views.append(view)

        if is_active:
            active_rules.append(view)

    return rule_views, active_rules


def build_dashboard_context(section):
    user = current_user()
    discount_rule_views, active_rules = build_discount_views()

    return {
        "section": section,
        "username": user["username"],
        "role": user["role"],
        "products": products,
        "discount_rules": discount_rule_views,
        "active_discounts": active_rules,
        "today": date.today().isoformat(),
    }


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/admindashboard")
@login_required
def admindashboard():
    user = current_user()
    if user["role"] != "admin":
        return redirect(url_for("userdashboard"))
    return render_template("admindashboard.html", username=user["username"])


@app.route("/userdashboard")
@login_required
def userdashboard():
    return render_template("userdashboard.html", **build_dashboard_context("dashboard"))


@app.route("/userdashboard/<section>")
@login_required
def userdashboard_section(section):
    if section not in {"dashboard", "pricing", "settings"}:
        return redirect(url_for("userdashboard"))

    template_map = {
        "dashboard": "userdashboard.html",
        "pricing": "pricingdashboard.html",
        "settings": "settingsdashboard.html",
    }

    return render_template(template_map[section], **build_dashboard_context(section))


@app.route("/userdashboard/pricing/update", methods=["POST"])
@admin_required
def update_pricing():
    product_id = request.form.get("product_id", "").strip()
    new_price_raw = request.form.get("price", "").strip()
    user = current_user()

    if not product_id or not new_price_raw:
        flash("Product and price are required.", "error")
        return redirect(url_for("userdashboard_section", section="pricing"))

    try:
        product = get_product(int(product_id))
    except ValueError:
        product = None

    if not product:
        flash("Selected product does not exist.", "error")
        return redirect(url_for("userdashboard_section", section="pricing"))

    try:
        new_price = float(new_price_raw)
    except ValueError:
        flash("Price must be a valid number.", "error")
        return redirect(url_for("userdashboard_section", section="pricing"))

    if new_price <= 0:
        flash("Price must be greater than 0.", "error")
        return redirect(url_for("userdashboard_section", section="pricing"))

    old_price = product["base_price"]
    product["base_price"] = round(new_price, 2)
    product["price_history"].append(
        {
            "old_price": round(old_price, 2),
            "new_price": round(new_price, 2),
            "updated_by": user["username"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )

    flash(f"{product['name']} price updated successfully.", "success")
    return redirect(url_for("userdashboard_section", section="pricing"))


@app.route("/userdashboard/discount/create", methods=["POST"])
@login_required
def create_discount():
    product_id = request.form.get("product_id", "").strip()
    rule_name = request.form.get("rule_name", "").strip()
    percent_raw = request.form.get("discount_percent", "").strip()
    start_date = request.form.get("start_date", "").strip()
    end_date = request.form.get("end_date", "").strip()
    created_by = current_user()["username"]

    if not all([product_id, rule_name, percent_raw, start_date, end_date]):
        flash("All discount fields are required.", "error")
        return redirect(url_for("userdashboard_section", section="discount"))

    try:
        product = get_product(int(product_id))
    except ValueError:
        product = None

    if not product:
        flash("Selected product does not exist.", "error")
        return redirect(url_for("userdashboard_section", section="discount"))

    try:
        discount_percent = float(percent_raw)
    except ValueError:
        flash("Discount must be a valid number.", "error")
        return redirect(url_for("userdashboard_section", section="discount"))

    if discount_percent < 1 or discount_percent > 100:
        flash("Discount must be between 1 and 100.", "error")
        return redirect(url_for("userdashboard_section", section="discount"))

    try:
        parsed_start = datetime.strptime(start_date, "%Y-%m-%d").date()
        parsed_end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        flash("Discount dates must use a valid date.", "error")
        return redirect(url_for("userdashboard_section", section="discount"))

    if parsed_end < parsed_start:
        flash("Discount end date must be on or after the start date.", "error")
        return redirect(url_for("userdashboard_section", section="discount"))

    discounted_price = compute_discounted_price(product["base_price"], discount_percent)
    if discounted_price < 0:
        flash("Discounted price must not be negative.", "error")
        return redirect(url_for("userdashboard_section", section="discount"))

    discount_rules.append(
        {
            "id": len(discount_rules) + 1,
            "rule_name": rule_name,
            "product_id": product["id"],
            "discount_percent": round(discount_percent, 2),
            "start_date": start_date,
            "end_date": end_date,
            "discounted_price": discounted_price,
            "created_by": created_by,
        }
    )

    flash(f"Discount rule saved for {product['name']}.", "success")
    return redirect(url_for("userdashboard_section", section="discount"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        user = users.get(username)

        if not user or user["password"] != password:
            return render_template(
                "login.html", message="Invalid username or password"
            )

        session["username"] = username
        session["role"] = user["role"]

        if user["role"] == "admin":
            return redirect(url_for("admindashboard"))
        return redirect(url_for("userdashboard"))

    return render_template("login.html", message="")


if __name__ == "__main__":
    app.run(debug=True)
