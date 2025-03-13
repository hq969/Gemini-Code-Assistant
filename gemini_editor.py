import openai
from flask import Flask, request, jsonify
from pygments import highlight
from pygments.lexers import PythonLexer, JavascriptLexer, HtmlLexer
from pygments.formatters import HtmlFormatter

# Initialize Flask app
app = Flask(__name__)

# OpenAI API Key (Replace with your key)
openai.api_key = "sk-proj-aGP6uHtD9sLETpKyQLqPamwzVzxEtmEG1z-SFOQKPY2oM1zUBla3KIkPOSjiSJ3ctYBYi6Q_OET3BlbkFJQuMTGA5rWFUqzIMbCj0fKRTXPanekPm3GwTVgCjQ9D5_BpXpMDkZPc5lIi2DmCk2-Jua5utDQAQ"

# Function to generate code suggestions using OpenAI GPT
def generate_code_suggestion(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

# Endpoint for code suggestion
@app.route('/suggest_code', methods=['POST'])
def suggest_code():
    data = request.json
    prompt = data.get("prompt", "")
    suggestion = generate_code_suggestion(prompt)
    return jsonify({"suggestion": suggestion})

# Endpoint for syntax highlighting
@app.route('/highlight_code', methods=['POST'])
def highlight_code():
    data = request.json
    code = data.get("code", "")
    language = data.get("language", "python").lower()

    # Choose lexer based on language
    if language == "python":
        lexer = PythonLexer()
    elif language == "javascript":
        lexer = JavascriptLexer()
    elif language == "html":
        lexer = HtmlLexer()
    else:
        return jsonify({"error": "Unsupported language"})

    highlighted_code = highlight(code, lexer, HtmlFormatter())
    return jsonify({"highlighted_code": highlighted_code})

# Endpoint for saving code to cloud (dummy example)
@app.route('/save_to_cloud', methods=['POST'])
def save_to_cloud():
    data = request.json
    file_name = data.get("file_name", "code.txt")
    code_content = data.get("code", "")

    # Simulate saving to cloud (replace with actual cloud integration)
    with open(file_name, 'w') as file:
        file.write(code_content)

    return jsonify({"message": f"Code saved as {file_name} successfully!"})

# Run the Flask app
if __name__ == '_main_':
    app.run(debug=True)