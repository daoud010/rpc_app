import os
import secrets

from flask import Flask, request, render_template, redirect, session

from Order import OrderManager
from order_client import OrderClient
from session_client import SessionClient

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'


def create_app():
    return app


session_instance = SessionClient()
order_instance = OrderClient()


@app.route("/")
def index():
    if not session.get("session_token"):
        return redirect("/login")

    orders_list = order_instance.GetAllOrders(session.get("user_id"))

    list_of_orders = []

    for order in orders_list.ordet_response:
        om = OrderManager()
        om.order_description = order.order_description
        om.payment_type = order.payment_type
        om.payment_card_or_cash_details = order.payment_card_or_cash_details
        om.order_amount = order.order_amount
        om.order_id = order.order_id
        list_of_orders.append(om)

    return render_template("index.html", orders_list=list_of_orders)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        status = session_instance.Authenticate(username, password)
        if status.auth_response == "Success":
            session["user_id"] = status.user_id
            session["session_token"] = secrets.token_hex(16)
            return redirect("/")
    return render_template("login_html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    [session.pop(key) for key in list(session.keys())]
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
def add_order():
    if not session.get("session_token"):
        return redirect("/login")
    if request.method == "POST":
        order_description = request.form["order_description"]
        payment_type = request.form["payment_type"]
        payment_card_or_cash_details = request.form["payment_card_or_cash_details"]
        order_amount = request.form["order_amount"]
        user_id = session.get("user_id")

        status = order_instance.AddOrder(user_id, order_description, payment_type,
                                         payment_card_or_cash_details, int(order_amount))
        if status is not None and status == "Success":
            return redirect("/")

        # order_list = order.service.GetAllOrders(session.get("user_id"))

        # return jsonify ({"message": Data Successfully Inserted, "order_list: orderlist})
        else:

            # return jsonify({"message": "Failure! Data not Inserted!"})
            return redirect("/")


@app.route("/edit", methods=["GET", "POST"])
def edit_order():
    if not session.get("session_token"):
        return redirect("/login")

    if request.method == "POST":
        order_description = request.form["order_description"]
        payment_type = request.form["payment_type"]
        payment_card_or_cash_details = request.form["payment_card_or_cash_details"]
        order_amount = request.form["order_amount"]
        user_id = session.get("user_id")
        order_id = request.form["order_id"]

        status = order_instance.EditOrder(order_description, payment_type, payment_card_or_cash_details,
                                          int(order_amount), user_id, int(order_id))
    return redirect("/")


@app.route("delete/<int:order_id>")
def DeleteOrder(order_id):
    if not session.get("session_token"):
        return redirect("/login")

    user_id = session.get("user_id")
    status = order_instance.CancelOrder(user_id, order_id)

    return redirect("/")
