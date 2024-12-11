from app import create_app
from flask_cors import CORS

def main():

    # Flask
    app = create_app()

    # DEBUG
    CORS(app)  # 允许所有来源的请求
    app.run(host="0.0.0.0", port=5000)

if __name__ == '__main__':
    main()
