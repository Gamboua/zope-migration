from config import *
import psycopg2


class Connection:

    def __init__(self):
        conn_str = "host=%s dbname=%s user=%s password=%s port=%s" % (
            HOST, BASE, USER, PASS, PORT
        )
        self.con = psycopg2.connect(conn_str)
        self.cursor = self.con.cursor()
