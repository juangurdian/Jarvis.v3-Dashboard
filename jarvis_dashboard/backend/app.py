# backend/app.py
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os, time, pickle
from assist import ask_question_memory
from task_manager import add_task, get_tasks, update_task, delete_task
from news import fetch_latest_news
from crypto import fetch_trending_crypto

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)

conversation_history = []

@app.route('/api/news', methods=['GET'])
def news_endpoint():
    # Get an optional 'query' parameter from the URL
    query = request.args.get('query')
    news_data = fetch_latest_news(query)
    return jsonify(news_data)


@app.route('/api/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        data = request.get_json()
        message = data.get('message')
        conversation_history.append({"role": "user", "content": message})
        timestamp = time.strftime("%D:%H:%M:%S")
        response_text = ask_question_memory(message + " " + timestamp)
        conversation_history.append({"role": "assistant", "content": response_text})
        return jsonify({"response": response_text})
    else:
        return jsonify({"chat_history": conversation_history})

@app.route('/api/tasks', methods=['GET', 'POST'])
def tasks_endpoint():
    if request.method == 'POST':
        data = request.get_json()
        description = data.get('description')
        due_date = data.get('due_date')
        status = data.get('status', "not started")
        task = add_task(description, due_date, status)
        return jsonify(task)
    else:
        tasks_list = get_tasks()
        return jsonify(tasks_list)

@app.route('/api/tasks/<task_id>', methods=['PUT', 'DELETE'])
def task_detail(task_id):
    if request.method == 'PUT':
        data = request.get_json()
        description = data.get('description')
        due_date = data.get('due_date')
        status = data.get('status')
        task = update_task(task_id, description, due_date, status)
        if task:
            return jsonify(task)
        else:
            return jsonify({"error": "Task not found"}), 404
    elif request.method == 'DELETE':
        delete_task(task_id)
        return jsonify({"result": "Task deleted"})

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# New crypto endpoint
@app.route('/api/crypto', methods=['GET'])
def crypto_endpoint():
    crypto_data = fetch_trending_crypto()
    return jsonify(crypto_data)

if __name__ == '__main__':
    app.run(debug=True)
