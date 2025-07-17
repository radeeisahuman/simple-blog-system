import bcrypt
import json
from database import cursor

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