import sqlite3
import bcrypt
import json

conn = sqlite3.connect('app.db')

cursor = conn.cursor()

def initialize_tables():
	user_tables_statement = '''
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT NOT NULL UNIQUE,
			password BLOB NOT NULL
		);
	'''

	posts_table_statement = '''
		CREATE TABLE IF NOT EXISTS posts (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT NOT NULL UNIQUE,
			content TEXT NOT NULL,
			user_id INTEGER,
			FOREIGN KEY (user_id) REFERENCES users(id)
		);
	'''

	cursor.execute(user_tables_statement)
	cursor.execute(posts_table_statement)
	conn.commit()


def user_register(username: str, password: str):
	salt = bcrypt.gensalt()
	hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

	username_exists = '''
		SELECT * FROM users
		WHERE username = ?
		LIMIT 1;
	'''

	username_results = cursor.execute(username_exists, (username,))
	exists = username_results.fetchone()

	if exists:
		print('This username already exists')
	else:
		insert_user = '''
			INSERT INTO users (username, password)
			VALUES (?,?)
		'''

		cursor.execute(insert_user, (username, hashed_password))
		conn.commit()
		print("User has been registered")


def user_login(username: str, password: str):
	user_query = '''
		SELECT username, password from users
		WHERE username = ?
		LIMIT 1;
	'''
	
	results = cursor.execute(user_query, (username,)).fetchone()

	if not results:
		return False
	
	db_name, hashed_pass = results

	return username == db_name and bcrypt.checkpw(password.encode('utf-8'), hashed_pass)