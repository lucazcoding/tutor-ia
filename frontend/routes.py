import sys
import os
from flask import Blueprint, request, render_template, jsonify, session, Response

# Adiciona a pasta raiz ao sys.path, permitindo importar backend.main
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from backend.chatbot import chat_listmessages, generate_speech_from_text, enviar_mensagem_para_ia

def configure_routes(app):
    @app.route("/")
    def homepage():
        return render_template("homepage.html")

    @app.route("/api/chat", methods=["POST"])
    def chat():
        data = request.get_json()
        user_message = data.get("message")
        print(f"Requisição recebida: {user_message}")

        if not user_message:
            return jsonify({"error": "Mensagem não fornecida"}), 400

        try:
            chat_history = session.get('chat_history', [])
            print(f"Histórico antes do processamento: {chat_history}")
            ai_response, updated_history = chat_listmessages(user_message, chat_history)
            session['chat_history'] = updated_history
            print(f"Resposta gerada: {ai_response}")
            print(f"Histórico após o processamento: {updated_history}")
            return jsonify({"response": ai_response})
        except Exception as e:
            print(f"Erro ao processar mensagem do chat: {e}")
            return jsonify({"error": "Ocorreu um erro ao processar sua requisição no chatbot."}), 500

    @app.route("/api/reset_chat", methods=["POST"])
    def reset_chat():
        print("Resetando histórico de chat")
        session.pop('chat_history', None)
        return jsonify({"message": "Histórico de chat resetado."}), 200

    @app.route("/api/speak", methods=["POST"])
    def speak():
        data = request.get_json()
        text_to_speak = data.get("text")
        print(f"Gerando áudio para: {text_to_speak}")

        if not text_to_speak:
            return jsonify({"error": "Texto não fornecido para fala."}), 400

        audio_data = generate_speech_from_text(text_to_speak)
        if audio_data:
            return Response(audio_data, mimetype="audio/mpeg")
        else:
            return jsonify({"error": "Falha ao gerar áudio."}), 500