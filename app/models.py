import json
import os
from datetime import datetime

# 定义用户数据文件夹
USER_DATA_FOLDER = "user_data"

# 确保用户数据文件夹存在
if not os.path.exists(USER_DATA_FOLDER):
    os.makedirs(USER_DATA_FOLDER)

def get_user_file_path(user_id):
    """获取用户的 JSON 文件路径"""
    return os.path.join(USER_DATA_FOLDER, f"{user_id}.json")

def load_data(user_id):
    """从用户的 JSON 文件加载数据，若文件不存在则返回空字典"""
    user_file = get_user_file_path(user_id)
    if os.path.exists(user_file):
        with open(user_file, "r", encoding="utf-8") as f:
            return json.load(f)
    # 用户文件不存在时返回一个空字典
    return {}

def save_data(user_id, users_data):
    """将数据保存到用户的 JSON 文件"""
    user_file = get_user_file_path(user_id)
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(users_data, f, indent=4, ensure_ascii=False)

def get_user(users_data, user_id):
    """获取用户数据，如果用户不存在则初始化"""
    if str(user_id) not in users_data:
        users_data[str(user_id)] = {"sessions": {}}
    return users_data[str(user_id)]

def add_session(users_data, user_id, session_id, title, date):
    """为用户添加新会话"""
    user = get_user(users_data, user_id)
    user["sessions"][str(session_id)] = {
        "title": title,
        "date": date,
        "messages": []
    }

def get_sessions(users_data, user_id):
    """获取指定用户的所有会话"""
    user = get_user(users_data, user_id)
    return user["sessions"]

def add_message_to_session(users_data, user_id, session_id, message):
    """向指定会话添加消息"""
    user = get_user(users_data, user_id)
    session = user["sessions"].get(str(session_id))

    if session is None:
        user["sessions"][str(session_id)] = {"messages": []}
        session = user["sessions"][str(session_id)]

    session["messages"].append(message)
