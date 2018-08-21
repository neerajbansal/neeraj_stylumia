import sqlite3


class UserModel:
    def __init__(self, id, role_id, name, address, email, bio, username, password):
        self.id = id
        self.role_id = role_id
        self.name = name
        self.address = address
        self.email = email
        self.bio = bio
        self.username = username
        self.password = password

    @classmethod
    def find_by_name(cls, name, db_path='./db/datashop.db'):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'SELECT * FROM user WHERE username=?;'
        result = cursor.execute(query, (name,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                user = UserModel(row[0], row[1], row[2],
                                 row[3], row[4], row[5], row[6], row[7])
            connection.close()
            return user

    @classmethod
    def find_by_id(cls, id, db_path='./db/datashop.db'):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'SELECT * FROM user WHERE id=?'
        result = cursor.execute(query, (id,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                user = UserModel(row[0], row[1], row[2],
                                 row[3], row[4], row[5], row[6], row[7])
            connection.close()
            return user

    @classmethod
    def insert_user_into_table(cls, role_id, name, address, email, bio, username, password, db_path='./db/datashop.db'):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'INSERT INTO user VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)'
        cursor.execute(query, (role_id, name, address,
                               email, bio, username, password))
        connection.commit()
        connection.close()

    @classmethod
    def update_user_into_table(cls, id, role_id, name, address, email, bio, db_path='./db/datashop.db'):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        query = 'UPDATE user SET role_id = ?, name = ?, address = ?, email = ?, bio = ? WHERE id = ?'
        cursor.execute(query, (role_id, name, address,
                               email, bio, id))
        connection.commit()
        connection.close()

    @classmethod
    def find_all(cls, db_path='./db/datashop.db'):
        users = list()
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'SELECT * FROM user;'
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                users.append(UserModel(row[0], row[1], row[2],
                                       row[3], row[4], row[5], row[6], row[7]))
            return users
        connection.close()

    @classmethod
    def delete_user(self, id, db_path='./db/datashop.db'):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        query = 'SELECT * FROM user WHERE id=?'
        result = cursor.execute(query, (id,))
        rows = result.fetchall()

        if rows:
            user_to_delete = 'DELETE FROM user WHERE id=?;'
            cursor.execute(user_to_delete, (id,))
            connection.commit()
        connection.close()

    def json(self):
        return {"id": self.id,
                "role_id": self.role_id,
                "name": self.name,
                "address": self.address,
                "email": self.email,
                "bio": self.bio}
