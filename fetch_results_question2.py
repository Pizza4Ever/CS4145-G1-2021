import time

import toloka.client as toloka
import datetime
import sqlite3

# Manually modify this
pool_id = 897853


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

print(results_list)