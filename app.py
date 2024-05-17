import os
import tempfile
import uuid

import pandas as pd
from flask import (
    Flask,
    Response,
    jsonify,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from fmp.fmp_data_fetcher import (
    fetch_available_companies,
    generate_financial_statement_dfs,
)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY environment variable is not set")


@app.route("/")
def index():
    _, _, dropdowns = fetch_available_companies()
    return render_template("index.html", dropdowns=dropdowns)


@app.route("/fetch_data", methods=["POST"])
def fetch_data():
    company_name = request.form["company_name"]
    ticker = company_name.split("  --  ")[0].lstrip()
    data_dict = generate_financial_statement_dfs(ticker)

    # Create temporary files for each DataFrame
    temp_files = {}
    for key, df in data_dict.items():
        # Flip DataFrame columns horizontally if needed
        # df = df.iloc[:, ::-1]

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        with pd.ExcelWriter(temp_file.name, engine="openpyxl") as writer:
            df.to_excel(writer, index=True, sheet_name=key)
        temp_files[key] = temp_file.name

    unique_id = str(uuid.uuid4())
    session[unique_id] = temp_files

    links = {
        key: url_for("download_excel", unique_id=unique_id, key=key)
        for key in temp_files.keys()
    }

    return jsonify({"links": links})


@app.route("/download_excel/<unique_id>/<key>")
def download_excel(unique_id, key):
    temp_files = session.get(unique_id)
    if not temp_files or key not in temp_files:
        return "Data not found", 404

    return send_file(temp_files[key], as_attachment=True, download_name=f"{key}.xlsx")


if __name__ == "__main__":
    app.run(debug=True)
