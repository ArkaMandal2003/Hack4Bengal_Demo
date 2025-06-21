from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory stores
expenses = []
investments = []
portfolio = []

expense_id = 1
portfolio_id = 1


# ----------- Expense Trackn korbe ----------- #
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/expenses')
def view_expenses():
    return render_template("expense/list.html", expenses=expenses)

@app.route('/expenses/add', methods=['GET', 'POST'])
def add_expense():
    global expense_id
    if request.method == 'POST':
        data = request.form
        expenses.append({
            "id": expense_id,
            "user_id": int(data['user_id']),
            "category": data['category'],
            "amount": float(data['amount']),
            "description": data['description'],
            "date": data['date'] or datetime.now().strftime("%Y-%m-%d")
        })
        expense_id += 1
        return redirect(url_for('view_expenses'))
    return render_template("expense/add.html")


# ----------- Investment Advice debe ----------- #
@app.route('/advisor', methods=['GET', 'POST'])
def advisor():
    suggestion = None
    if request.method == 'POST':
        saving = float(request.form['saving'])
        risk = request.form['risk']
        if risk == 'low':
            suggestion = {'FD': saving*0.5, 'Debt Funds': saving*0.3, 'Gold': saving*0.2}
        elif risk == 'medium':
            suggestion = {'Index Funds': saving*0.5, 'Gold': saving*0.2, 'FD': saving*0.3}
        else:
            suggestion = {'Stocks': saving*0.6, 'Crypto': saving*0.1, 'Index Funds': saving*0.3}
    return render_template('advisor/recommend.html', suggestion=suggestion)



# ----------- Portfolio  ----------- #
@app.route('/portfolio')
def view_portfolio():
    return render_template("portfolio/view.html", portfolio=portfolio)


@app.route('/portfolio/add', methods=['GET', 'POST'])
def add_portfolio():
    global portfolio_id
    if request.method == 'POST':
        data = request.form
        portfolio.append({
            "id": portfolio_id,
            "user_id": int(data['user_id']),
            "type": data['type'],
            "asset": data['asset'],
            "amount": float(data['amount']),
            "current_value": float(data['current_value']),
            "date": data['date'] or datetime.now().strftime("%Y-%m-%d")
        })
        portfolio_id += 1
        return redirect(url_for('view_portfolio'))
    return render_template("portfolio/add.html")

@app.route('/select-expenses', methods=['GET', 'POST'])
def select_expenses():
    cards = {
        'Rent': '💸',
        'Food': '🍜',
        'Transport': '🚌',
        'Save More': '💰',
        'Education': '🎓',
        'Home': '🏠'
    }

    if request.method == 'POST':
        selected = request.form.get('selected_categories').split(',')
        print("Selected categories:", selected)
        # Store or use them as needed.
        return redirect(url_for('home'))

    return render_template('select/select_expenses.html', cards=cards)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
