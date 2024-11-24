import os
from datetime import datetime
import psycopg2
from flask import Flask, request

app = Flask(__name__)

# Подключение к базе данных
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://myuser:mypassword@db:5432/mydb')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')

def hello():
    try:
        # Получаем данные из запроса
        client_info = request.headers.get('User-Agent')
        now = datetime.now()

        # Подключаемся к базе данных
        conn = get_db_connection()
        cursor = conn.cursor()

        # Создаем таблицу, если она не существует
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS table_Counter (
                id SERIAL PRIMARY KEY,
                datetime TIMESTAMP NOT NULL,
                client_info TEXT NOT NULL
            );
        """)

        # Вставляем данные в таблицу
        cursor.execute("INSERT INTO table_Counter (datetime, client_info) VALUES (%s, %s)", (now, client_info))
        conn.commit()

        cursor.close()
        conn.close()

        return f"Hello World! Your request was recorded.\n"
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
