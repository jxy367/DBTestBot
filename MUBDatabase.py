import psycopg2


class MUBDatabase:
    db_url = ""
    conn = ""
    cur = ""

    def __init__(self, db_url: str):
        self.db_url = db_url
        self.conn = psycopg2.connect(db_url, sslmode='require')
        self.cur = self.conn.cursor()

    def add_test(self, test_id: int, name: str):
        self.check_connection()
        sql = """INSERT INTO test(id, name) VALUES(%s, %s);"""
        try:
            self.cur.execute(sql, (test_id, name,))
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            print(e)
            print("Test was not added")
            return False
        return True

    def remove_test(self, test_id: int):
        self.check_connection()
        sql = """DELETE FROM test WHERE id = %s;"""
        try:
            self.cur.execute(sql, (test_id,))
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            print(e)
            print("Test was not removed")
            return False
        return True

    def update_test(self, test_id: int, name: str):
        self.check_connection()
        sql = """UPDATE users SET name = %s WHERE id = %s"""
        try:
            self.cur.execute(sql, (name, test_id,))
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            print(e)
            print("Test was not updated")
            return False
        return True

    def get_test(self):
        self.check_connection()
        test = {}
        sql = """SELECT * from test"""
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            for tup in data:
                test[tup[0]] = tup[1]
        except Exception as e:
            print(e)
            print("Failed to get test")
        return test

    def check_connection(self):
        print("Connection closed: " + str(self.conn.closed))
        if self.conn.closed != 0:
            self.cur.close()
            self.conn.close()
            self.conn = psycopg2.connect(self.db_url, sslmode='require')
            self.cur = self.conn.cursor()
