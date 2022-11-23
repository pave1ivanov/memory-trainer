import sqlite3
import datetime


# Handles SQLite connection and handles CREATE, READ, DELETE queries
class DataBase:

    # Connecting to DB and creating a table in case there is none
    def __init__(self):
        self.con = sqlite3.connect('memory_trainer.db')
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS question 
                           (id             INTEGER PRIMARY KEY AUTOINCREMENT,
                            question       TEXT                     NOT NULL,
                            answer         TEXT                     NOT NULL,
                            time           TIMESTAMP                NOT NULL)''')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.cur.close()

    # deletes a question/answer pair
    def delete_card(self, id):
        self.cur.execute("DELETE FROM question WHERE id =?", (id,))
        self.con.commit()
        # DELETE 3 LINES BELOW ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
        cursor = self.con.execute("SELECT * FROM question")
        for row in cursor:
            print(row)

    # returns list with question and answer
    def get_card(self) -> tuple:
        # retrieving from db a random question/answer pair from 5 that have been shown least recently
        card = self.cur.execute('''SELECT * 
                                     FROM question
                                    WHERE time IN 
                                        (
                                            SELECT time 
                                            FROM question 
                                            ORDER BY time ASC
                                            LIMIT 5
                                         )
                                    ORDER BY RANDOM()''').fetchone()
        if card:
            self.cur.execute("UPDATE question SET time = ? WHERE id=?", (datetime.datetime.now(), card[0]))
            self.con.commit()
        return card

    # adds questions to the DB
    def add_card(self, question, answer):
        self.cur.execute(f"INSERT INTO question(question, answer, time) VALUES (?,?,?)",
                         (question, answer, datetime.datetime.now()))
        self.con.commit()
