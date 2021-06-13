import sqlite3

con = sqlite3.connect('db.db')
cur = con.cursor()

cur.execute(f'''
    SELECT * FROM seeker_games WHERE invalid_game = 0
''')

rows = cur.fetchall()
print(f"Amount of rows: {len(rows)}")
for row in rows:
    passed_hints = []
    if row[5] == 0:
        for i in range(0, 14):
            hint = row[6+i*2]
            passed_hints.append(hint)
            eliminated = row[7+i*2]

            # If nothing was eliminated, continue
            if not eliminated:
                continue

            eliminated = [int(s) for s in eliminated.split(",")]

            # Store for each image which hint eliminated them
            for image in eliminated:
                cur.execute(f'''
                    INSERT INTO images_context (image_id, hint_id, eliminated) 
                    VALUES ('{image}', '{hint}', 1) 
                    ON CONFLICT(image_id, hint_id) DO UPDATE SET eliminated=eliminated+1
                    ''')

            # Store for each image which hint might be a possible contxt
            for hint in passed_hints:
                for image in eliminated:
                    cur.execute(f'''
                        INSERT INTO images_context (image_id, hint_id, pos_context) 
                        VALUES ('{image}', '{hint}', 1) 
                        ON CONFLICT(image_id, hint_id) DO UPDATE SET pos_context=pos_context+1
                        ''')

con.commit()
con.close()