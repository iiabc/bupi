from datetime import datetime
from .models import load_data, save_data, get_user, add_session, add_message_to_session

def create_session(user_id):
    """为指定用户创建会话，并自动生成标题和时间"""
    # 从文件加载用户数据
    users_data = load_data(user_id)
    user = get_user(users_data, user_id)

    # 自动生成会话ID和时间
    session_id = int(datetime.now().timestamp())
    title = "新会话"
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 为用户添加会话
    add_session(users_data, user_id, session_id, title, date)

    # 保存数据到用户的文件
    save_data(user_id, users_data)

    # 返回会话ID、标题和时间
    return {"session_id": session_id, "title": title, "date": date}

def get_sessions(user_id):
    """获取指定用户的所有会话"""

    # 从文件加载用户数据
    users_data = load_data(user_id)

    # 获取用户
    user = get_user(users_data, user_id)

    # 会话信息列表
    sessions_info = []

    # 遍历会话数据
    for session_id, session_data in user["sessions"].items():
        session_info = {
            "id": session_id,
            "title": session_data["title"],
            "date": session_data["date"]
        }
        # 添加到会话信息列表
        sessions_info.append(session_info)

    return sessions_info

def add_message(user_id, session_id, role, content):
    """向指定会话添加消息"""
    users_data = load_data(user_id)

    # 创建消息数据
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # 向指定会话添加消息
    add_message_to_session(users_data, user_id, session_id, message)

    # 保存数据到文件
    save_data(user_id, users_data)

    return "已添加消息"

def get_messages(user_id, session_id):
    """获取指定会话的所有消息"""
    users_data = load_data(user_id)
    user = get_user(users_data, user_id)
    return user["sessions"].get(str(session_id), {}).get("messages", [])
