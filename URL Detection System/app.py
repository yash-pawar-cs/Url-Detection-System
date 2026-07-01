from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace this with your real API key
API_KEY = 'YOUR_GOOGLE_API_KEY_HERE'

def check_url_safety(url):
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
    payload = {
        "client": {
            "clientId": "your-company-name",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    response = requests.post(endpoint, json=payload)
    data = response.json()

    if "matches" in data:
        return "⚠️ Suspicious or Unsafe URL", "unsafe", [10, 90]
    else:
        return "✅ Safe URL", "safe", [90, 10]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    result_class = ""
    chart_data = [50, 50]
    
    if request.method == 'POST':
        url = request.form['url']
        result, result_class, chart_data = check_url_safety(url)

    return render_template('index.html', result=result, result_class=result_class, chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)
