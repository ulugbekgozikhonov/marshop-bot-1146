import sqlite3

con = sqlite3.connect("marshop.db")
cur = con.cursor()

class DatabaseManager():
    
    def __init__(self,dbname) -> None:
        self.dbname = dbname
        self.__con = sqlite3.connect(self.dbname)
        self.__cur = self.__con.cursor()
        
    
    async def create_tables(self):
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            full_name VARCHAR(100),
            phone_number VARCHAR(25),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")
        
        
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            photo TEXT,
            price FLOAT,
            description VARCHAR,
            count INTEGER,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
            )""")

    async def register_user(self,data: dict):
        try:
            self.__cur.execute("INSERT INTO users(chat_id,full_name,phone_number) VALUES(?,?,?)",
                           (data.get("chat_id"),data.get("full_name"),data.get("phone_number")))
            self.__con.commit()
            return True
        except Exception as ex:
            print(ex)
            return False
        
    async def get_user_by_chat_id(self,chat_id):
        try:
            user = self.__cur.execute("SELECT * FROM users WHERE chat_id=?",(chat_id,)).fetchone()
            return user
        except Exception as ex:
            print(ex)
            return False
            
    async def add_product(self,data:dict):
        try:
            self.__cur.execute("""INSERT INTO products (name,photo,price,description,count,user_id) VALUES (?,?,?,?,?,?)""",
            (data.get("name"),data.get("photo"),data.get("price"),data.get("description"),data.get("count"),data.get("user_id")))
            self.__con.commit()
            return True
        except Exception as ex:
            print(ex)
            return False
    async def get_all_products_by_user_id(self,user_id: int):
        try:
            products = self.__cur.execute("SELECT * FROM products WHERE user_id=?",(user_id,)).fetchall()
            return products
        except Exception as e:
            print(e)
            return False
        

# cur.execute("ALTER TABLE products ADD status BOOLEAN DEFAULT(FALSE)")
# con.commit()
        
# def delete_user_by_chat_id(chat_id: int):
#     con = sqlite3.connect("marshop.db")
#     cur = con.cursor()
    
#     cur.execute("DELETE FROM users WHERE chat_id=?",(chat_id,))
#     con.commit()

# delete_user_by_chat_id(909437832)