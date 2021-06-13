from question_2_submission import Question_2_Submission
import time
from functools import reduce

import toloka.client as toloka
import datetime
import sqlite3


def get_res_mult_queries(queries):
    res = []
    for query in queries:
        print(query)
        cur.execute(query)
        res.append(cur.fetchone()[0])

    return res


def load_in_db(results_list):
    for r in results_list:
        image_found_val = 1 if r.image_found else 0
        invalid_game_val = 1 if r.invalid else 0
        
        rounds_cols = 'hint_r1, eliminated_r1'
        first_round_imgs = ','.join([str (j) for j in r.rounds[0]])
        rounds_vals = f"{r.hints_ids[0]}, '{first_round_imgs}' "

        # For each additional hint and round we 
        for i in range(1, len(r.rounds)):
            rounds_cols += f', hint_r{i+1}, eliminated_r{i+1}'
            round_str = ",".join([str (j) for j in r.rounds[i]])
            if i >= len(r.hints_ids):
                rounds_vals += f", NULL, '{round_str}'"
            else:
                rounds_vals += f", {str(r.hints_ids[i])}, '{round_str}'"

        
        query_str = f'''
            INSERT INTO seeker_games (correct_image_id, correct_image_found, honeypot_hint, invalid_game, {rounds_cols}) 
                VALUES ({r.correct_image_id}, {image_found_val}, '{r.honeypot_hint}', {invalid_game_val}, {rounds_vals})
        '''
        print(f"Executing: {query_str}")
        cur.execute(query_str)

    con.commit()


if __name__=="__main__":
    
    # Manually modify this
    pool_id = 24912393


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

    print(f"Getting assignments in pool {pool_id}")
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
                        submission.invalid = True
                    
                    # Else we can not check if this is an invalid submission
                    else:
                        submission.honeypot_hint = "not applicable"

                
                print(f"Getting images ids ")
                images_ids_queries = submission.get_queries_images_ids(round, images)
                submission.rounds.append(get_res_mult_queries(images_ids_queries))
            submission.assert_invalid_elimination_pattern()

            print(f"Getting id for correct image {submission.correct_image}")
            cur.execute(submission.get_image_id_query())
            submission.correct_image_id = cur.fetchone()[0]

            print("Getting id for hints")
            hints_ids_queries = submission.get_queries_hints_ids(hints)
            submission.hints_ids = get_res_mult_queries(hints_ids_queries)
            
            results_list.append(submission)
    
    con.commit()
    print(f'New results received: {len(results_list)}' if len(results_list) > 0 else 'Not received any new results yet, try to run this cell later.')

    print("Storing results in db")
    load_in_db(results_list)

