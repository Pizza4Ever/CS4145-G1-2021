import sqlite3
con = sqlite3.connect('db.db')

cur = con.cursor()

# Hint can only exist once per image.
# (Perhaps add ID to person who came up with the hint)
cur.execute('''CREATE TABLE hints
                (hint TEXT, 
                strength FLOAT,
                image_id INTEGER,
                PRIMARY KEY (hint, image_id),
                FOREIGN KEY(image_id) REFERENCES images(image_id));
            ''')

cur.execute('''CREATE TABLE images
                (path TEXT, 
                image_id INTEGER UNIQUE NOT NULL PRIMARY KEY);
            ''')

con.commit()

con.close()
