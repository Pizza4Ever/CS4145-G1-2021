<<<<<<< HEAD
=======
from os import curdir, terminal_size
>>>>>>> 75dfc6d... Add object for processing question 2 submissions
from question_2_submission import Question_2_Submission
import time
from functools import reduce

import toloka.client as toloka
import datetime
import sqlite3

# Manually modify this
pool_id = 24890934


f = open("token.txt", "r")
token = f.read()
f.close()
toloka_client = toloka.TolokaClient(token, 'PRODUCTION')
requester = toloka_client.get_requester()
print(f'Your account: {requester}')

con = sqlite3.connect('db.db')
cur = con.cursor()


# Function from toloka-kit github for retrieving results adjusted for our case
results_list = []


def get_res_mult_queries(queries):
    res = []
    for query in queries:
        cur.execute(query)
        res.append(cur.fetchone()[0])

    return res


for assignment in toloka_client.get_assignments(pool_id=pool_id, status=toloka.assignment.Assignment.ACCEPTED):
    for task, solution in zip(assignment.tasks, assignment.solutions):
        images = task.input_values['image_id']
        hints = task.input_values['hints']

        submission = Question_2_Submission()
        submission.correct_image = task.input_values["correct_image"]
        image_index = str(images.index(submission.correct_image))

        for i, round in enumerate(solution.output_values['result']):
            # Check if the correct image is eliminated
            if image_index in round:
                submission.image_found = False

                # If the correct image is eliminated when the honeypot hint is asked, this is an invalid submission
                if i == 3:
                    submission.honeypot_hint = "failed"
                    submission.correct_image = True
                
                # Else we can not check if this is an invalid submission
                else:
                    submission.honeypot_hint = "not applicable"

            
            images_ids_queries = submission.get_queries_images_ids(round, images)
            submission.rounds.append(get_res_mult_queries(images_ids_queries))
        submission.assert_invalid_elimination_pattern()

        cur.execute(submission.get_image_id_query())
        submission.correct_image_id = cur.fetchone()[0]
        hints_ids_queries = submission.get_queries_hints_ids(hints)
        submission.hints_ids = get_res_mult_queries(hints_ids_queries)
        
        results_list.append(submission)

        # results_list.append({
        #     'assignment_id': assignment.id,
        #     'input_values': task.input_values,
        #     'output_values': solution.output_values
        # }) 

print(f'New results received: {len(results_list)}' if len(results_list) > 0 else 'Not received any new results yet, try to run this cell later.')

print(results_list[0])


def build_insert_query():
    pass