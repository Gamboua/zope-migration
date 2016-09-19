from Connection import Connection


class DataBase:

    def __init__(self):
        self.connection = Connection()

    def fetch(self, table, where, columns='*'):
        query = "SELECT %s FROM %s WHERE %s;" % (
            columns, table, where
        )
        self.connection.cursor.execute(query)

        return self.connection.cursor.fetchone()

    def update(self, table, fields, where):
        query = "UPDATE %s SET %s WHERE %s;" % (
            table, fields, where
        )
        return self.connection.cursor.execute(query)

    def insert(self, table, fields, values):
        query = "INSERT INTO %s(%s) VALUES(%s);" % (
            table, fields, values
        )
        return self.connection.cursor.execute(query)

    def fetch_all(self, table):
        pass
