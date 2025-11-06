import google.generativeai as genai
import os
from flask import Flask, render_template, request

genai.configure(api_key="")
model=genai.GenerativeModel("gemini-1.0-pro")

app = Flask(__name__)


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/food', methods=['POST'])
def form():
    name = request.form.get('name')
    height = request.form.get('height')
    weight = request.form.get('weight')
    return render_template("food.html", name=name, height=height, weight=weight)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = {key: request.form.get(key) for key in [
        "name", "height", "weight", "goal",
        "breakfast", "lunch", "snacks", "dinner"
    ]}

    prompt = f"""
    Analyze this user's daily diet and health info. Give personalized feedback in bullet points.

    Name: {data['name']}
    Height: {data['height']} cm
    Weight: {data['weight']} kg
    Goal: {data['goal']}
    Meals:
    - Breakfast: {data['breakfast']}
    - Lunch: {data['lunch']}
    - Snacks: {data['snacks']}
    - Dinner: {data['dinner']}
    """

    response = model.generate_content(prompt)
    feedback = response.text

    return render_template("result.html",
        name=data['name'],
        height=data['height'],
        weight=data['weight'],
        breakfast=data['breakfast'],
        lunch=data['lunch'],
        snacks=data['snacks'],
        dinner=data['dinner'],
        feedback=feedback
    )
if __name__ == "__main__":
    app.run(debug=True)
