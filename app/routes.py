from flask import request, jsonify
from .services import create_session, get_sessions, add_message, get_messages
from app.answer.knowledge_base import KnowledgeBase

import json

with open("config.json") as config_file:
    config = json.load(config_file)

api_key = config.get("API_KEY")
if not api_key:
    raise ValueError("config.json 没有设置 API_KEY")

kb = KnowledgeBase(api_key=api_key)

def init_routes(app):
    # 用户相关操作
    @app.route('/users/<int:user_id>/sessions', methods=['GET'])
    def get_user_sessions(user_id):
        """获取用户的所有会话"""
        sessions = get_sessions(user_id)
        return jsonify(sessions)

    @app.route('/users/<int:user_id>/sessions', methods=['POST'])
    def create_new_session(user_id):
        """为用户创建新会话"""
        session_data = create_session(user_id)
        return jsonify(session_data), 201

    # 消息相关操作
    @app.route('/users/<int:user_id>/sessions/<int:session_id>/messages', methods=['GET'])
    def get_session_messages(user_id, session_id):
        """获取指定会话的消息"""
        messages = get_messages(user_id, session_id)

        # 如果没有消息，返回空列表
        return jsonify(messages)  # 即使没有消息，也返回空列表

    @app.route('/users/<int:user_id>/sessions/<int:session_id>/messages', methods=['POST'])
    def add_new_message(user_id, session_id):
        """向指定会话添加消息"""
        data = request.get_json()
        content = data.get('content')

        if not content:
            return jsonify({"error": "Content is required."}), 400

        # 默认 role 为 'User'
        role = "User"
        response = add_message(user_id, session_id, role, content)

        # 生成 AI 角色的回答
        ai_answer = kb.get_answer(content)
        ai_role = "AI"
        add_message(user_id, session_id, ai_role, ai_answer)

        # 获取当前会话的所有消息（包括用户和AI的消息）
        messages = get_messages(user_id, session_id)

        if response == "已添加消息":
            return jsonify(messages), 201  # 返回完整的消息列表
        return jsonify({"error": response}), 400
