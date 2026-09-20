# AI-Powered Global Market Expansion Assistant

A Python-based AI business research and strategy tool designed for international market expansion, product-market fit analysis, and cross-border growth planning.

This project was built to support the kind of work involved in global business development: identifying target countries, analyzing customer segments, evaluating competitors, understanding pricing and positioning, and turning research into actionable market entry strategies.

## Project Focus

The system is designed to help businesses answer practical questions such as:

- Which markets deserve attention?
- Which customer segments are most promising?
- What products or categories are likely to perform well?
- Which channels and marketplaces fit the product and buyer behavior?
- What are the risks, pricing dynamics, and local positioning constraints?
- How can AI accelerate research, analysis, and decision-making?

Rather than acting as a generic chatbot, it is structured as a strategic research assistant for international expansion, market discovery, and business development support.

## What This Repo Includes

- AI-assisted research workflow for target markets and product categories
- customer and market opportunity analysis
- platform and channel recommendation logic
- pricing and positioning considerations
- keyword and SEO planning for localization
- risk assessment and data-gap analysis
- structured report generation suitable for business presentations
- interactive dashboard for exploring research and recommendations

## Why It Fits in the Business Context 

The project reflects the important themes behind this kind of role: global business, market research, strategic planning, entrepreneurship, execution, and practical AI usage for business outcomes.

It is especially aligned with work involving:

- international market research and strategy
- competitive analysis in overseas markets
- product and positioning research
- cross-border e-commerce insights
- sales and business development support
- digital marketing and customer discovery
- AI-assisted data organization, research, and decision support

## Core Features

- Dynamic product and destination inputs
- Market opportunity evaluation across multiple countries
- Trend and demand signal assessment
- marketplace and channel recommendation workflow
- product opportunity and competitive positioning analysis
- SEO and keyword planning for localization
- risk and mitigation review
- detailed market brief generation in a readable report format
- Flask-based dashboard for interactive business use

## Example Use Cases

- Evaluate a product category in a new international market
- Compare market fit across multiple destination countries
- Recommend the most suitable sales channels for expansion
- Generate a concise market entry brief for business discussions
- Support a global marketing or business development strategy with AI-assisted research

## Project Structure

- `dashboard.py` — web dashboard for interactive market analysis
- `main.py` — command-line version of the assistant
- `app/agent.py` — orchestration logic for market analysis
- `app/skills.py` — modular research workflows for trends, entry strategy, SEO, and risk
- `app/tools.py` — data and validation helpers for research operations
- `app/profile.py` — profile and session-based business context tracking
- `app/config.py` — environment configuration
- `templates/` — dashboard interface
- `static/` — frontend styling and interactivity
- `tests/` — validation for the project workflow

## How It Works

1. The user defines a product and target market.
2. The assistant gathers business context such as constraints, channel preference, and pricing goals.
3. It evaluates opportunities across market demand, competition, platform fit, and risk.
4. It generates a structured recommendation with trend analysis, product opportunity, platform guidance, SEO direction, and risk notes.
5. The output is surfaced through an interactive dashboard and can be exported as a clear report.

## Business Value

This project showcases the ability to combine:

- business thinking
- market analysis
- research organization
- AI-assisted decision support
- strategic recommendation generation
- practical execution in a lightweight product workflow

It demonstrates a strong understanding of how AI can support business operations, international expansion planning, and customer-driven market strategy without replacing human judgment.

## Tech Stack

- Python
- Flask
- OpenAI-compatible API integration
- Pydantic
- Requests
- HTML/CSS/JavaScript

## Setup

```bash
cd python_agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then add your API credentials to `.env`:

```env
AISA_API_KEY=your_api_key
AISA_BASE_URL=https://api.aisa.one/v1
AISA_DATA_BASE_URL=https://api.aisa.one/apis/v1
MODEL_NAME=kimi-k2.6
```

## Run the Dashboard

```bash
python dashboard.py
```

Open:

```text
http://127.0.0.1:5000
```

## Run the CLI Version

```bash
python main.py
```

## Example Inputs

- Wireless earbuds in Japan
- Premium skincare in Germany
- Lifestyle goods in South Korea
- Home products in Brazil
- Consumer goods in the US

## Summary

This repository is a practical example of AI-driven business research and market expansion support. It reflects core themes of global expansion, market discovery, customer analysis, cross-border commerce, digital marketing, and AI-enabled execution, while staying focused on creating useful, decision-ready output for real business contexts.
