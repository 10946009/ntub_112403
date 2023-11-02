import psycopg2


class Postgres:
    def __init__(self):
        self.conn = None
        try:
            # connect to the PostgreSQL server
            print("Connecting to the PostgreSQL database...")
            self.conn = psycopg2.connect(
                host="localhost",
                dbname="trip",
                user="postgres",
                password="10946029"
            )
        except (Exception, psycopg2.DatabaseError) as error:
            print('有錯誤', error)

    def __del__(self):
        if self.conn is not None:
            self.conn.close()
            print("Database connection closed.")

    def create_multi(self, query, values) -> int:
        try:
            cur = self.conn.cursor()
            cur.executemany(query, values)
            self.conn.commit()
            cur.close()
            return cur.rowcount
        except (Exception, psycopg2.DatabaseError) as error:
            print('有錯誤', error)

    def read(self, query) -> list:
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return rows
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def update(self, query, values) -> int:
        """Update records"""
        try:
            cur = self.conn.cursor()
            cur.execute(query, values)
            updated_record = cur.rowcount
            self.conn.commit()
            cur.close()
            return updated_record
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
