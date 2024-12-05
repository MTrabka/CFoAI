import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os

# Załadowanie konfiguracji z pliku .env
load_dotenv("config.env")
api_key = os.getenv("API_KEY")

# Konfiguracja modelu Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Inicjalizacja aplikacji Flask
app = Flask(__name__, template_folder='Templates')

# Zmienna przechowująca historię rozmowy
conversation = []
turns = 0  # Licznik tur
user_data = {}  # Zmienna przechowująca dane użytkownika

# Funkcja do zapisywania logów rozmowy
def save_conversation_log(conversation):
    with open("conversation_log.txt", "a") as log_file:
        for turn in conversation:
            log_file.write(f"{turn}\n")
        log_file.write("\n---\n")

# Funkcja do generowania pytań przez AI
def generate_ai_question(isFinal=False):
    global conversation
    if not isFinal:
        prompt_judge = f"""
               You are the judge in a Turing test. 
               Your task is to ask questions to determine whether you are conversing with a human or an AI.
               This is the conversation so far: {conversation}. 
               Continue the conversation by asking insightful, creative, or challenging questions that help you make your judgment. 
               Ask one question at a time and don't explain."""
    else:
        prompt_judge = f"""
        You are the judge in a Turing test. Based on the entire conversation so far: {conversation}, your task is to write your judgment.
        1. Clearly state whether you believe the participant is a human or an AI. 
        2. Explain your reasoning in a concise and logical manner, focusing on the characteristics of the responses that influenced your decision.
        3. Highlight specific examples from the conversation that led you to your conclusion, such as patterns, linguistic cues, or reasoning styles. 
        4. Write your judgment in a formal, objective tone."""

    try:
        response = model.generate_content(prompt_judge)
        ai_question = response.text.strip()
        return ai_question
    except Exception as e:
        return f"Błąd: {str(e)}"

from flask import send_file

# Route to download the conversation log
@app.route("/download-log", methods=["GET"])
def download_log():
    try:
        return send_file("conversation_log.txt", as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/delete-log", methods=["GET"])
def delete_log():
    try:
        log_file_path = "conversation_log.txt"
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
            message = "Conversation log has been deleted."
        else:
            message = "Conversation log does not exist."
        return render_template("indexUser.html", model_response=message, isFinal=False, user_data={})
    except Exception as e:
        return f"Error: {str(e)}"

# Strona główna - wyświetlenie formularza
@app.route("/", methods=["GET", "POST"])
def index():
    global conversation, turns, user_data
    model_response = ""
    isFinal = False  # Domyślnie nie finalny osąd


    # Obsługa resetu
    if request.args.get("reset") == "true":
        # Resetowanie zmiennych
        conversation = []
        turns = 0
        user_data = {}

        # Generowanie nowego pytania od AI
        ai_question = generate_ai_question()
        conversation.append(f"Judge: {ai_question}")
        turns += 1

        # Wyświetlenie strony z nowym pytaniem
        return render_template("indexUser.html", model_response=ai_question, isFinal=False, user_data={})

    print(request.form)
    if request.method == "POST":
        if turns != 0 and turns < 6:
            # Pobranie odpowiedzi użytkownika i generowanie kolejnego pytania
            user_input = request.form.get("user_input")
            conversation.append(f"Participant: {user_input}")
            ai_question = generate_ai_question()
            conversation.append(f"Judge: {ai_question}")
            turns += 1
            model_response = ai_question
            print(f"Truns: {turns}")
        elif turns == 6:
            print(f"Truns: {turns}")
            user_input = request.form.get("user_input")
            conversation.append(f"Participant: {user_input}")
            isFinal = True
            turns+=1
        elif turns == 7 and not user_data:
            print(f"Truns form: {turns}")
            print("Form submission received.")  # Debugging statement
            user_data = {
                "gender": request.form.get("gender"),
                "age": request.form.get("age"),
                "education": request.form.get("education")
            }
            print(f"Received participant data: {user_data}")
            conversation.append(f"Participant Data: {user_data}")
            model_response = generate_ai_question(isFinal=True)
            conversation.append(f"Judge: {model_response}")
            save_conversation_log(conversation)


    elif request.method == "GET":
        # Przy pierwszym załadowaniu strony, generuj pytanie, jeśli rozmowa jest pusta
        if turns == 0 and not conversation:
            ai_question = generate_ai_question()
            conversation.append(f"Judge: {ai_question}")
            turns += 1
            model_response = ai_question
    return render_template("indexUser.html", model_response=model_response, isFinal=isFinal, user_data=user_data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
