import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute("SELECT symbol, shares FROM stocks WHERE user_id = ? GROUP BY symbol", session["user_id"])

    total_money = 0

    for stock in stocks:
        api = lookup(stock["symbol"])
        stock["name"] = api["name"]
        stock["price"] = api["price"]
        stock["total"] = stock["price"] * stock["shares"]
        total_money += stock["total"]

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']
    total_money += cash

    return render_template("index.html", stocks=stocks, cash=cash, total=total_money)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        stock = lookup(request.form.get("symbol"))

        if stock == None:
            return apology("Symbol don't exist", 400)

        if not request.form.get("shares").isdigit():
            return apology("invalid number", 400)

        shares = int(request.form.get("shares"))
        total = stock["price"] * shares

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']

        if total > cash:
            return apology("You don't have enought money")

        row = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND symbol = ?", session["user_id"], stock["symbol"])
        if len(row) > 0:
            total_shares = row[0]["shares"]
            total_shares += shares

            db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND symbol = ?",
                       int(total_shares), session["user_id"], stock["symbol"])
        else:
            db.execute("INSERT INTO stocks (user_id, symbol, shares) VALUES (?, ?, ?)", session["user_id"], stock["symbol"], shares)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total, session["user_id"])

        db.execute("INSERT INTO history (user_id, symbol, shares, price, action, timestamp) VALUES (?, ?, ?, ?, 'buy', datetime('now'))",
                   session["user_id"], stock["symbol"], shares, stock["price"])

        flash('Bought!')
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Get stocks from history table
    stocks = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])

    # Add total of cash, and symbol "+" or "-"
    for stock in stocks:
        if stock["action"] == "buy":
            stock["total"] = "-" + usd(stock["price"] * stock["shares"])
        else:
            stock["total"] = "+" + usd(stock["price"] * stock["shares"])

    return render_template("/history.html", stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Must provide symbol", 400)

        stock_info = lookup(request.form.get("symbol"))

        if stock_info == None:
            return apology("Symbol don't exist")

        return render_template("quoted.html", stock_info=stock_info)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) == 0:
            if request.form.get("password") == request.form.get("confirmation"):
                pwd_hash = generate_password_hash(request.form.get("password"))
                db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), pwd_hash)
                return redirect("/")
            else:
                return apology("password confirmation fail", 400)
        else:
            return apology("user already exists", 400)

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    stocks = db.execute("SELECT symbol, shares FROM stocks WHERE user_id = ?", session["user_id"])

    if request.method == "POST":

        symbols = []
        for stock in stocks:
            symbols.append(stock["symbol"])

        symbol_sell = request.form.get("symbol")
        # Ensure is a valid symbol
        if symbol_sell not in symbols:
            return apology("symbol not owned", 400)

        total_shares = 0
        for stock in stocks:
            if stock["symbol"] == symbol_sell:
                total_shares = stock["shares"]
                break

        shares_sell = int(request.form.get("shares"))
        if shares_sell > total_shares:
            return apology("too many shares")

        if shares_sell == total_shares:

            db.execute("DELETE FROM stocks WHERE symbol = ? AND user_id = ?", symbol_sell, session["user_id"])

        else:
            db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND symbol = ?",
                       total_shares - shares_sell, session["user_id"], symbol_sell)

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']

        cash_sell = lookup(symbol_sell)["price"] * shares_sell

        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash + cash_sell, session["user_id"])

        db.execute("INSERT INTO history (user_id, symbol, shares, price, action, timestamp) VALUES (?, ?, ?, ?, 'sell', datetime('now'))",
                   session["user_id"], symbol_sell, shares_sell, cash_sell)

        return redirect("/")

    else:
        return render_template("/sell.html", stocks=stocks)
