"""
Script to create the databases needed.
IMPORTANT: If the databases already exist they will be overwritten
"""

import sqlite3
con = sqlite3.connect('db.db')

cur = con.cursor()

# Hint can only exist once per image.
# (Perhaps add ID to person who came up with the hint)
# The strength value should be an indicator of how certain we are this hint suits the image. (Not sure if this is the best method)
cur.execute('DROP TABLE IF EXISTS hints')
cur.execute('''CREATE TABLE hints
                (hint TEXT, 
                strength FLOAT,
                image_id INTEGER,
                hint_orig TEXT,
                PRIMARY KEY (hint, image_id),
                FOREIGN KEY(image_id) REFERENCES images(image_id));
            ''')

cur.execute('DROP TABLE IF EXISTS images')
cur.execute('''CREATE TABLE images
                (path TEXT, 
                image_id INTEGER UNIQUE NOT NULL PRIMARY KEY,
                cv_description TEXT,
                cv_tags TEXT,
                question1 BOOLEAN DEFAULT FALSE);
            ''')


# cur.execute('''CREATE TABLE games
#                 (image_id INTEGER,
#                 hint TEXT,
#                 strength FLOAT,
#             ''')

con.commit()

con.close()
