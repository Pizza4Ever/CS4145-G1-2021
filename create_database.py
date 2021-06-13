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
                hint_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                CONSTRAINT unique_hints UNIQUE (hint, image_id),
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

cur.execute('DROP TABLE IF EXISTS seeker_games')
cur.execute('''CREATE TABLE seeker_games
                (game_id INTEGER UNIQUE NOT NULL PRIMARY KEY,
                correct_image_id INTEGER,
                correct_image_found INTEGER,
                completion_time FLOAT,
                honeypot_hint TEXT NOT NULL,
                invalid_game INTEGER,
                hint_r1 INTEGER,
                eliminated_r1 TEXT,
                hint_r2 INTEGER,
                eliminated_r2 TEXT,
                hint_r3 INTEGER,
                eliminated_r3 TEXT,
                hint_r4 INTEGER,
                eliminated_r4 TEXT,
                hint_r5 INTEGER,
                eliminated_r5 TEXT,
                hint_r6 INTEGER,
                eliminated_r6 TEXT,
                hint_r7 INTEGER,
                eliminated_r7 TEXT,
                hint_r8 INTEGER,
                eliminated_r8 TEXT,
                hint_r9 INTEGER,
                eliminated_r9 TEXT,
                hint_r10 INTEGER,
                eliminated_r10 TEXT,
                hint_r11 INTEGER,
                eliminated_r11 TEXT,
                hint_r12 INTEGER,
                eliminated_r12 TEXT,
                hint_r13 INTEGER,
                eliminated_r13 TEXT,
                hint_r14 INTEGER,
                eliminated_r14 TEXT
                );
            ''')

cur.execute('''CREATE TABLE images_context (
                image_id INTEGER ,
                hint_id INTEGER,
                eliminated INTEGER,
                pos_context INTEGER,
                honeypot BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (image_id) REFERENCES images(image_id),
                FOREIGN KEY (hint_id) REFERENCES hints(hint_id),
                PRIMARY KEY (image_id, hint_id)
                );
            ''')    

con.commit()

con.close()
