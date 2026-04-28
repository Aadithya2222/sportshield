from google import genai

# 🔑 your API key
client = genai.Client(api_key="AIzaSyAZOgpVklK6or39pCKPlYNEdRFJRfNwYok")

def extract_match_info(title):
    prompt = f"""
    Extract cricket teams from this title.
    Return ONLY like: RR vs RCB

    Title: {title}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return response.text.strip()


# 🧪 TEST
title = "RCB vs RR IPL 2026 Full Match Highlights"
print("👉 Extracted:", extract_match_info(title))