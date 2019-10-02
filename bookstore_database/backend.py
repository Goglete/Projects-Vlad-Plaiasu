import sqlite3 as sq


class Database():

	def __init__(self):
		self.conn = sq.connect("books.db")
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS store (id INTEGER PRIMARY KEY, title text, author text, year integer, genre text)")
		self.conn.commit() 
		


	def insert(self,title,author,year,genre):
		self.cur.execute("INSERT INTO store VALUES (NULL,?,?,?,?)",(title,author,year,genre))
		self.conn.commit()
	

	def view(self):
		self.cur.execute("SELECT * FROM store")
		rows = self.cur.fetchall()
		return rows

	def search(self,title='',author='',year='',genre=''):
		self.cur.execute("SELECT * FROM store WHERE title=? OR author=? OR year=? OR genre=?",(title,author,year,genre))
		rows=self.cur.fetchall()
		if not rows:
			self.cur.execute("SELECT * FROM store WHERE author LIKE '{}'".format('%'+author+'%'))
			rows=self.cur.fetchall()
		return rows

	def search_select(self,id):
		self.cur.execute("SELECT * FROM store WHERE id=?",(id,))
		row = self.cur.fetchall()
		return row

	def delete(self,id):
		self.cur.execute("DELETE FROM store WHERE id=?",(id,))
		self.conn.commit()
		

	def update(self,id,title,author,year,genre):
		self.cur.execute("UPDATE store SET title=?,author=?,year=?,genre=? WHERE id=?",(title,author,year,genre,id))
		self.conn.commit()


	def __del__(self):
		self.conn.close()
		





	#connect()
	#insert("Book2","altul",2069,"comedy")
	#delete(3)
	#update(2,"Cartea3","nimeni",324,"sdfs")
	#print(view())
	#print(search(genre="com"))
	#print(search_select(2))