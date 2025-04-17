import psycopg2


class Database:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

        self.conn = self.connect()

    def connect(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def add_coins(self, coins: list[dict]):
        data = [(row["id"], row["name"], row["symbol"], row["image"]) for row in coins]
        query = """INSERT INTO coins(id, name, symbol, img_url) VALUES(%s, %s, %s, %s)"""
        self.conn.cursor().executemany(query, data)
        self.conn.commit()

    def add_market_data(self, market_data: list[dict]):
        data = [(row["id"], row["current_price"], row["market_cap_rank"], row["last_updated"]) for row in market_data]
        query = """INSERT INTO market_data(coin_id, current_price, rank, last_updated) VALUES(%s, %s, %s, %s) ON CONFLICT DO NOTHING """
        self.conn.cursor().executemany(query, data)
        self.conn.commit()


    def add_user(self, username: str, password: str):
        self.conn.cursor().execute(f"INSERT INTO users(username, password) VALUES('{username}', '{password}')")
        self.conn.commit()


    def check_user_exists(self, username: str, password: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}' and password = '{password}'")
        data = cursor.fetchone()
        if data:
            return True
        else:
            return False

    def get_coins(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT name FROM coins")
        data = [i[0] for i in cursor.fetchall()]
        return data


    def close(self):
        self.conn.close()
