import sqlite3


def create_database(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    create_user_table = '{}{}{}{}{}{}{}{}'.format(
        ' CREATE TABLE IF NOT EXISTS',
        ' user(id INTEGER PRIMARY KEY,',
        ' role_id INTEGER NOT NULL REFERENCES role(id),',
        ' name text NOT NULL,',
        ' address text,',
        ' email text,',
        ' bio text,',
        ' username text NOT NULL,'
        ' password text NOT NULL);'
    )

    cursor.execute(create_user_table)

    create_role_table = '{}{}{}'.format(
        'CREATE TABLE IF NOT EXISTS',
        ' role(id INTEGER PRIMARY KEY,',
        ' role text);'
    )
    cursor.execute(create_role_table)

    cursor.execute('INSERT OR REPLACE INTO user VALUES(1, 1,"Neeraj Bansal", "Chandigarh Area", "bansal.neeraj94@gmail.com", "Full Stack Developer, AI is love", "neeraj_bansal", "demo");')

    cursor.execute('INSERT OR REPLACE INTO user VALUES(2, 1,"ShivamK", "Chennai Area", "shivam.k@gmail.com", "Python Developer, software achitect", "shivam_k", "demo");')

    cursor.execute('INSERT OR REPLACE INTO user VALUES(3, 1,"Rajanam", "Madras Area", "Rajanam@gmail.com", "JS Developer", "rajanam", "demo");')

    cursor.execute('INSERT OR REPLACE INTO user VALUES(4, 2,"Siddarath Kumaram", "Jaipur Area", "siddarath.kumaram@gmail.com", "ML/AI developer, Product Manager", "siddarath", "demo");')

    cursor.execute('INSERT OR REPLACE INTO user VALUES(5, 2,"Mahesh Babu", "Bengaluru Area", "mahesh.babu@gmail.com", "Software Product Manager", "mahesh_babu", "demo");')

    cursor.execute('INSERT OR REPLACE INTO user VALUES(6, 3,"Sri Ramanujam", "Bengaluru Area", "ramanujam@gmail.com", "CEO, Product Owner, Co-Founder", "ramanujam", "demo");')

    cursor.execute('INSERT OR REPLACE INTO role VALUES(1, "Officer");')
    cursor.execute('INSERT OR REPLACE INTO role VALUES(2, "Manager");')
    cursor.execute('INSERT OR REPLACE INTO role VALUES(3, "Admin");')

    connection.commit()
    connection.close()

    print('Database successfully created and populated with data!')
