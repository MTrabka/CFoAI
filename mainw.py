import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
load_dotenv("config.env")
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


app = Flask(__name__)

def chat_with_ai(mode):
    try:

        conversation = []

        for round_num in range(6):
            prompt_judge = f"""
            You are the judge in a Turing test. 
            Your task is to ask questions to determine whether you are conversing with a human or an AI.
             This is the conversation so far: {conversation}. 
             Continue the conversation by asking insightful, creative, or challenging questions that help you make your judgment. 
             Ask one question at a time and don't explain"""
            prompt_participant = f"""
            You are a participant in a Turing test. The goal is to convince the judge that you are human. Here is the conversation so far: {conversation}. Your previous responses are the ones marked as Participant.  

            Respond naturally, as if you were chatting with a friend. Focus on:  
            1. Using a light, friendly, and conversational tone, while occasionally showing vulnerability, humor, or hesitation.  
            2. Introducing small imperfections such as typos, incomplete thoughts, or slight contradictions, which are common in human speech.  
            3. Reflecting on personal experiences with unique details and vivid imagery, even if they are mundane or not directly relevant.  
            4. Expressing emotional responses authentically. Avoid generic descriptions—include nuanced reactions, like changes in voice, specific behaviors, or quirky personal reflections.  
            5. Adding context or anecdotes that feel spontaneous, even if they’re tangential, to mimic how humans sometimes digress in conversation.  

            Be creative but consistent in your persona. If you make a claim (e.g., "Sarah studied really hard"), make sure to add supporting details that feel personal and realistic. Avoid repeating patterns or providing overly formal or robotic explanations. Your goal is to make the judge believe you are human through your relatable and imperfect responses."""

            question = model.generate_content(prompt_judge)
            conversation.append(f"<b>Judge:</b> {question.text}")
            response = model.generate_content(prompt_participant+ "Your next question is: "+ question.text)
            conversation.append(f"<b>Participant:</b> {response.text}")

        prompt_final_judgment = f"""
        You are the judge in a Turing test. Based on the entire conversation so far: {conversation}, your task is to write your judgment.
        1. Clearly state whether you believe the participant is a human or an AI. 
        2. Explain your reasoning in a concise and logical manner, focusing on the characteristics of the responses that influenced your decision.
        3. Highlight specific examples from the conversation that led you to your conclusion, such as patterns, linguistic cues, or reasoning styles. 
        4. Write your judgment in a formal, objective tone."""
        final_question = model.generate_content(prompt_final_judgment)
        conversation.append(f"<b>Judge final answer:</b> {final_question.text}")

        conversation_text = "<br>".join(conversation)
        with open("conversation_log10.txt", "w", encoding="utf-8") as file:
            file.write(conversation_text)

        return conversation_text

    except Exception as e:
        return f"Error: {str(e)}"




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    mode = data.get("mode", "Gemini-gemini")


    conversation = chat_with_ai(mode)
    return jsonify({"conversation": conversation})



app.run(debug=True)