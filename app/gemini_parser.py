import google.generativeai as genai

genai.configure(api_key="AIzaSyAZOgpVklK6or39pCKPlYNEdRFJRfNwYok")

model = genai.GenerativeModel("gemini-pro")

def extract_match_info():
    prompt = """
    Identify cricket teams from this text.
    Example output: RR vs RCB

    Text: IPL cricket match video highlights
    """

    response = model.generate_content(prompt)

    return response.text.strip()