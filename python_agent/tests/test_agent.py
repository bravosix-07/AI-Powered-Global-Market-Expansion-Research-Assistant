from app.agent import CrossBorderAgent
from app.profile import Profile
from dashboard import app


def test_profile_requires_interview_until_complete():
    profile = Profile()
    assert profile.needs_interview() is True

    profile.mark_interview_complete()
    assert profile.needs_interview() is False


def test_agent_starts_interview_when_profile_incomplete():
    agent = CrossBorderAgent()
    response = agent.handle_message("I want to sell porcelain to South Korea")

    assert "What product or category do you want to sell?" in response
    assert "Which country are you targeting?" in response


def test_agent_generates_market_brief_after_completion():
    agent = CrossBorderAgent()
    agent.profile.mark_interview_complete()
    agent.profile.add_fact("destination_market", "South Korea")
    agent.profile.add_fact("product", "porcelain tableware")

    response = agent.handle_message("Give me a full market brief")

    assert "destination" in response.lower()
    assert "trend_analysis" in response.lower() or "platform_recommendation" in response.lower()


def test_agent_can_skip_interview_and_continue():
    agent = CrossBorderAgent()
    agent.profile.skip_interview()

    response = agent.handle_message("What is trending in Brazil?")

    assert "destination" in response.lower() or "analysis" in response.lower()


def test_agent_handles_generic_product_and_destination():
    agent = CrossBorderAgent()
    agent.profile.mark_interview_complete()
    response = agent.handle_message("Generate a brief for wireless earbuds in Japan")

    assert "japan" in response.lower()
    assert "wireless earbuds" in response.lower()


def test_dashboard_generates_rich_report():
    client = app.test_client()
    response = client.post(
        "/",
        data={
            "product": "wireless earbuds",
            "destination": "Japan",
            "market_language": "ja",
            "target_channel": "Amazon",
            "price_band": "medium",
            "constraints": ["Margins", "Logistics"],
            "budget": "moderate",
            "notes": "Premium audio segment",
        },
    )

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "wireless earbuds" in html
    assert "Japanese" in html or "Japan" in html
    assert "Detailed market report" in html
