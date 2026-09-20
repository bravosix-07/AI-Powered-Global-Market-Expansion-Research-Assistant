from __future__ import annotations

from flask import Flask, jsonify, render_template, request, send_file

from app.agent import CrossBorderAgent

app = Flask(__name__)
agent = CrossBorderAgent()


@app.route("/", methods=["GET", "POST"])
def index():
    default_product = "wireless earbuds"
    default_destination = "Japan"
    default_constraints = ["Margins", "Logistics"]
    default_channel = "Amazon"
    default_language = "ja"
    default_price_band = "medium"
    default_budget = "moderate"
    default_notes = "Premium segment with strong repeat-purchase potential."

    product = request.form.get("product", default_product)
    destination = request.form.get("destination", default_destination)
    market_language = request.form.get("market_language", default_language)
    target_channel = request.form.get("target_channel", default_channel)
    price_band = request.form.get("price_band", default_price_band)
    budget = request.form.get("budget", default_budget)
    notes = request.form.get("notes", default_notes)
    constraints = request.form.getlist("constraints") or default_constraints

    brief = agent.generate_brief(
        destination=destination,
        product=product,
        market_language=market_language,
        target_channel=target_channel,
        price_band=price_band,
        constraints=constraints,
        budget=budget,
        notes=notes,
    )

    brief["profile"] = {
        "product": product,
        "destination": destination,
        "market_language": market_language,
        "target_channel": target_channel,
        "price_band": price_band,
        "constraints": constraints,
        "budget": budget,
        "notes": notes,
    }

    return render_template(
        "index.html",
        brief=brief,
        product=product,
        destination=destination,
        market_language=market_language,
        target_channel=target_channel,
        price_band=price_band,
        budget=budget,
        notes=notes,
        constraints=constraints,
    )


@app.route("/api/report", methods=["POST"])
def api_report():
    data = request.get_json(silent=True) or {}
    brief = agent.generate_brief(
        destination=data.get("destination", "Japan"),
        product=data.get("product", "wireless earbuds"),
        market_language=data.get("market_language", "en"),
        target_channel=data.get("target_channel", "Amazon"),
        price_band=data.get("price_band", "medium"),
        constraints=data.get("constraints", ["Margins", "Logistics"]),
        budget=data.get("budget", "moderate"),
        notes=data.get("notes", ""),
    )
    return jsonify(brief)


@app.route("/download")
def download_report():
    product = request.args.get("product", "wireless earbuds")
    destination = request.args.get("destination", "Japan")
    brief = agent.generate_brief(destination=destination, product=product)
    content = brief.get("report_markdown", "# Market report\n\nNo details available.")
    return send_file(
        __import__("io").BytesIO(content.encode("utf-8")),
        mimetype="text/markdown",
        as_attachment=True,
        download_name=f"{product.lower().replace(' ', '-')}-{destination.lower().replace(' ', '-')}-report.md",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
