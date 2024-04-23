from flask import Flask, g, jsonify, render_template, request
from fmp.fmp_data_fetcher import (
    fetch_available_companies,
    generate_financial_statement_dfs,
)

app = Flask(__name__)

# with app.app_context():
#     tickers, names, dropdowns = fetch_available_companies()
#     g.tickers = tickers
#     g.names = names
#     g.dropdowns = dropdowns


@app.route("/")
def index():
    _, _, dropdowns = fetch_available_companies()
    return render_template("index.html", dropdowns=dropdowns)


if __name__ == "__main__":
    app.run(debug=True)
