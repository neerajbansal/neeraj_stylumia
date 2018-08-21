import sqlite3


class RoleModel:

    def __init__(self, id, role):
        self.id = id
        self.role = role

    @classmethod
    def find_all_roles(cls, db_path='./db/datashop.db'):
        roles = list()
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'SELECT id, role FROM role;'
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                roles.append(RoleModel(row[0], row[1]))
            return roles
        connection.close()

    def json(self):
        return {'id': self.id,
                'role': self.role
                }
