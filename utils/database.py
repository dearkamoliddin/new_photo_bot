import psycopg2 as db
from main import config


class Database:
    def __init__(self):
        self.conn = db.connect(
            database=config.DB_NAME,
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASS
        )
        self.cursor = self.conn.cursor()

    def create_tables(self):
        user_table = """
                CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                chat_id BIGINT NOT NULL,
                full_name VARCHAR(55),
                phone_number VARCHAR(13),
                location_name VARCHAR(55));
        """

        photos = """
               CREATE TABLE IF NOT EXISTS photos(
               id SERIAL PRIMARY KEY,
               user_id BIGINT REFERENCES users(id),
               status BOOLEAN DEFAULT false);
        """

        likes = """
              CREATE TABLE IF NOT EXISTS likes(
              id SERIAL PRIMARY KEY,
              user_id BIGINT REFERENCES users(id),
              photo_id BIGINT REFERENCES photos(id),
              is_like BOOLEAN DEFAULT false);
        """

        self.cursor.execute(user_table)
        self.cursor.execute(photos)
        self.cursor.execute(likes)

        self.conn.commit()

    def get_user_by_chat_id(self, chat_id):
        query = f"SELECT * FROM users WHERE chat_id = '{chat_id}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def add_user(self, data: dict):
        chat_id = data['chat_id']
        full_name = data['full_name']
        phone_number = data['phone_number']
        location = data['location']
        query = f"""INSERT INTO users (chat_id, full_name, phone_number, location_name)
        VALUES({chat_id}, '{full_name}', '{phone_number}', '{location}');"""
        self.cursor.execute(query)
        self.conn.commit()
        return True







