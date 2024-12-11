from app import create_app
from flask_cors import CORS

def main():

    # Flask
    app = create_app()

    # DEBUG
    CORS(app)  # 允许所有来源的请求
    app.run(debug=True)

if __name__ == '__main__':
    main()
