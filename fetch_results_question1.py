import time

import toloka.client as toloka
import datetime
import sqlite3

import cleanup

# Manually modify this
pool_id = 894310


f = open("token.txt", "r")
token = f.read()
f.close()
toloka_client = toloka.TolokaClient(token, 'SANDBOX')
requester = toloka_client.get_requester()
print(f'Your account: {requester}')


# Function from toloka-kit github for retrieving results
results_list = []

for assignment in toloka_client.get_assignments(pool_id=pool_id, status=toloka.assignment.Assignment.SUBMITTED):
    for task, solution in zip(assignment.tasks, assignment.solutions):
        results_list.append({
            'assignment_id': assignment.id,
            'input_values': task.input_values,
            'output_values': solution.output_values
        })

print(f'New results received: {len(results_list)}' if len(results_list) > 0 else 'Not received any new results yet, try to run this cell later.')


def load_in_db(results_list):
    print(results_list)
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    for r in results_list:
        results = r['output_values']
        path = r['input_values']['image_id']
        print(path)
        for value in results.values():
            original = value
            strength_value = 0.0
            spellchecked = cleanup.check_grammer(original.lower())
            cur.execute(f'''
                INSERT INTO hints (hint, strength, image_id, hint_orig) 
                    VALUES ('{spellchecked}', '{strength_value}', (SELECT image_id FROM images WHERE path='{path}'), '{original}') 
                    ON CONFLICT(hint, image_id) DO UPDATE SET strength=strength+1.0, hint_orig = hint_orig || ',' || '{original}'
            ''')

    con.commit()
    con.close()

load_in_db(results_list)

