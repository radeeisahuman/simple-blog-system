import sqlite3

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
			email TEXT NOT NULL UNIQUE,
			content TEXT NOT NULL,
			user_id INTEGER,
			FOREIGN KEY (user_id) REFERENCES users(id)
		);
	'''

	cursor.execute(user_tables_statement)
	cursor.execute(posts_table_statement)
	conn.commit()

def get_user_id(username: str):
	user_id_statement = '''
		SELECT id FROM users
		WHERE username = ?
		LIMIT 1;
	'''

	results = cursor.execute(user_id_statement, (username, )).fetchone()

	if not results:
		return False

	(user_id,) = results

	return user_id

def create_post(title: str, content: str, user_id: int, is_logged_in: bool):
	if not is_logged_in:
		return False

	insert_post_statement = '''
		INSERT INTO posts (title, content, user_id)
		VALUES (?, ?, ?);
	'''

	cursor.execute(insert_post_statement, (title, content, user_id,))
	conn.commit()
	return True

def get_posts(user_id: int, is_logged_in: bool):
	if not is_logged_in:
		return False

	fetch_posts_query = '''
		SELECT posts.title, posts.content, users.username
		FROM posts
		INNER JOIN users
		ON posts.user_id = users.id
		WHERE users.id = ?;
	'''

	posts = cursor.execute(fetch_posts_query, (user_id,)).fetchone
	post_list = []

	for i in posts:
		(post_name, post_content, username,) = i
		post_list.append({
			'post_name': post_name,
			'post_content': post_content,
			'username': username
		})
	
	return post_list

def get_post(user_id: int, post_id: int, is_logged_in: bool):
	if not is_logged_in:
		return False

	fetch_post_query = '''
		SELECT posts.title, posts.content, users,username
		FROM posts
		INNER JOIN users
		ON posts.user_id = users.id
		WHERE users.id = ?
		AND posts.id = ?
		LIMIT 1;
	'''

	result = cursor.execute(fetch_post_query, (user_id, post_id)).fetchone()

	if not result:
		return "This post does not belong to you"

	(post_name, post_content, username,) = result

	return {'post_name': post_name, 'post_content': post_content, 'username': username}