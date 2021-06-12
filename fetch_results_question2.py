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


# Function from toloka-kit github for retrieving results
results_list = []

for assignment in toloka_client.get_assignments(pool_id=pool_id, status=toloka.assignment.Assignment.ACCEPTED):
    for task, solution in zip(assignment.tasks, assignment.solutions):
        images = task.input_values['image_id']
        submission = Question_2_Submission()
        submission.correct_image = task.input_values["correct_image"]
        image_index = images.index(submission.correct_image)

        for i, round in enumerate(solution.output_values['result']):
            # Check if the correct image is eliminated
            if int(image_index) in round:
                submission.image_found = False

                # If the correct image is eliminated when the honeypot hint is asked, this is an invalid submission
                if i == 3:
                    submission.honeypot_hint = "failed"
                    submission.correct_image = True
                
                # Else we can not check if this is an invalid submission
                else:
                    submission.honeypot_hint = "not applicable"

            submission.rounds.append(",".join([images[int(i)] for i in round]))

        results_list.append({
            'assignment_id': assignment.id,
            'input_values': task.input_values,
            'output_values': solution.output_values
        }) 

print(f'New results received: {len(results_list)}' if len(results_list) > 0 else 'Not received any new results yet, try to run this cell later.')

print(results_list[0])


def get_hints_ids_query(hints):
    pass


def build_query():
    pass