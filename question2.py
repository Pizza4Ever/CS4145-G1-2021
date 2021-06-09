import random
import time

import toloka.client as toloka
import datetime
import sqlite3

### Variables one should modify
project_name = "Remove the images!"
pool_name = "My Pool!"
hints_required = 4
URL = 'https://123toloka.nl:5000/static/'
###


# Create a file named token.txt and place your toloka token on the first line. Do not commit this file.
f = open("token.txt", "r")
token = f.read()
f.close()


toloka_client = toloka.TolokaClient(token, 'SANDBOX')

# This is just to test if your token is correct (If it fails, request a new toloka Oauth token)
requester = toloka_client.get_requester()
print(f'Your account: {requester}')


# # The code below shows how to create a new toloka project using html files
def create_project():
    # Construct a new project
    new_project = toloka.project.Project(
        assignments_issuing_type=toloka.project.Project.AssignmentsIssuingType.AUTOMATED,
        public_name=project_name,
        public_description='--Public description--', # TODO: Insert good descriptions
    )

    # This is a toloka JavaScript library, which adds useful integration.
    recording_assets = toloka.project.view_spec.ClassicViewSpec.Assets(
        script_urls=["$TOLOKA_ASSETS/js/toloka-handlebars-templates.js"]
    )

    # Create the page that a worker will see. We use the older HTML+JS+CSS method since it allows more for control.
    project_interface = toloka.project.view_spec.ClassicViewSpec(
        script=open('./page/question2.js').read().strip(),
        markup=open('./page/question2.html').read().strip(),
        styles=open('./page/question2.css').read().strip(),
        assets=recording_assets
    )

    # For this task, we have an input image and an output text.
    # (They are labeled: image and result respectively, this is also the HTML reference)
    input_specification = {'query_image': toloka.project.field_spec.ArrayUrlSpec(),
                           'image_id': toloka.project.field_spec.ArrayStringSpec(),
                           'hints': toloka.project.field_spec.ArrayStringSpec(),
                           'correct_image': toloka.project.field_spec.StringSpec()}
    output_specification = {'result': toloka.project.field_spec.JsonSpec(required=True)}

    new_project.task_spec = toloka.project.task_spec.TaskSpec(
        input_spec=input_specification,
        output_spec=output_specification,
        view_spec=project_interface
    )

    return new_project


# Searched for a project on your Toloka account with the specified name
def find_project(name):
    projects = toloka_client.find_projects()
    for p in projects.items:
        if p.public_name == name and not p.status == toloka.project.Project.ProjectStatus.ARCHIVED:
            return p
    return False


# Either creates a new project or updates an already existing one
def create_or_update():
    new_project = create_project()
    p = find_project(project_name)
    if p:
        print("Updating the project")
        new_project = toloka_client.update_project(p.id, new_project)
    else:
        print("Creating a new project")
        new_project = toloka_client.create_project(new_project)
    return new_project


# Creates a pool, this pool is where the collection of tasks is gathered
def create_pool(project):
    # Create the skill used for repeats
    skill_name = 'Beaut!'
    skill = next(toloka_client.get_skills(name=skill_name), None)
    if skill:
        print('Skill already exists')
    else:
        print('Creating new skill')
        skill = toloka_client.create_skill(
            name=skill_name,
            hidden=True,
            public_requester_description={'EN': 'The performer played our game'},
        )

    pool = toloka.pool.Pool(
        project_id=project.id,
        private_name=pool_name,
        may_contain_adult_content=True,
        will_expire=datetime.datetime.utcnow() + datetime.timedelta(hours=2),
        reward_per_assignment=0.15,
        auto_accept_solutions=False,
        auto_accept_period_day=1,
        assignment_max_duration_seconds=60 * 10,
        filter=(
                (toloka.filter.Languages.in_('EN')) &
                (toloka.filter.Skill(skill.id) == None) &
                (toloka.filter.ClientType == toloka.filter.ClientType.ClientType.BROWSER)
        ),
        defaults=toloka.pool.Pool.Defaults(default_overlap_for_new_task_suites=1),

    )

    set_pool_requirements(pool, skill)

    pool = toloka_client.create_pool(pool)
    return pool


def set_pool_requirements(pool, skill):
    # Automatically updating skills
    pool.quality_control.add_action(
        collector=toloka.collectors.AnswerCount(),
        # If the performer completed at least one task,
        conditions=[toloka.conditions.AssignmentsAcceptedCount > 0],
        # It doesn't add to the skill, it sets the new skill to 1
        action=toloka.actions.SetSkill(skill_id=skill.id, skill_value=1),
    )

    # The first rule in this project restricts pool access for performers who often make mistakes
    pool.quality_control.add_action(
        collector=toloka.collectors.AcceptanceRate(),
        conditions=[
            # Performer completed more than 2 tasks
            toloka.conditions.TotalAssignmentsCount > 2,
            # And more than 35% of their responses were rejected
            toloka.conditions.RejectedAssignmentsRate > 35,
        ],
        # This action tells Toloka what to do if the condition above is True
        # In our case, we'll restrict access for 15 days
        # Always leave a comment: it may be useful later on
        action=toloka.actions.RestrictionV2(
            scope=toloka.user_restriction.UserRestriction.ALL_PROJECTS,
            duration=1,
            duration_unit='DAYS',
            private_comment='Performer often make mistakes',  # Only you will see this comment
        )
    )

    # The second useful rule is "Fast responses". It allows us to filter out performers who respond too quickly.
    pool.quality_control.add_action(
        # Let's monitor fast submissions for the last 5 completed task pages
        # And define ones that take less than 20 seconds as quick responses.
        collector=toloka.collectors.AssignmentSubmitTime(history_size=5, fast_submit_threshold_seconds=10),
        # If we see more than one fast response, we ban the performer from all our projects for 10 days.
        conditions=[toloka.conditions.FastSubmittedCount > 1],
        action=toloka.actions.RestrictionV2(
            scope=toloka.user_restriction.UserRestriction.ALL_PROJECTS,
            duration=1,
            duration_unit='DAYS',
            private_comment='Fast responses',  # Only you will see this comment
        )
    )

    # The following increases overlap for the task if the assignment was rejected to ensure the task is done by another worker
    pool.quality_control.add_action(
        collector=toloka.collectors.AssignmentsAssessment(),
        conditions=[toloka.conditions.AssessmentEvent == toloka.conditions.AssessmentEvent.REJECT],
        action=toloka.actions.ChangeOverlap(delta=1, open_pool=False)
    )



# This function checks for existing pools with the specified name, if one exists it is reused
def create_or_get_pool(project):
    pools = toloka_client.find_pools(project_id=project.id)
    for p in pools.items:
        if p.project_id == project.id and p.private_name == pool_name and not p.is_archived():
            print("Found previous pool")
            return p
    print("Creating new pool")
    return create_pool(project)


def fetch_images_from_db():
    # Pull all images + hints from db
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    # Left join also gives the images with 0 hints.
    cur.execute('''
        SELECT a.*, h.* FROM images a
        LEFT JOIN hints h ON a.image_id = h.image_id
    ''')
    fetch = cur.fetchall()
    print(fetch)
    storage = dict()
    for f in fetch:
        if f[0] not in storage:
            storage[f[0]] = []
        if f[2] is not None:  # Making sure the None type is not inserted
            storage[f[0]].append(f[2])
    con.commit()
    con.close()
    return storage


# Creates the task description based on the items returned from fetch_image_from_db
def create_game(pool):
    storage = fetch_images_from_db()
    tasks = []
    print(storage)
    for key, value in storage.items():
        if len(value) > hints_required:
            # Sample n images, but not the main image
            sample_list = list(storage)
            sample_list.remove(key)
            sample = random.sample(sample_list, 23)
            sample.append(key)
            random.shuffle(sample)
            tasks.append(toloka.task.Task(
                input_values={
                    'query_image': list(map(lambda key: URL + key, sample)),
                    'image_id': sample,
                    'hints': value,
                    'correct_image': key
                },
                pool_id=pool.id,
            ))
    return tasks


# Encapsulates the tasks in a task suite (Don't know why)
def create_task_suite(tasks, pool):
    new_tasks_suite = toloka.task_suite.TaskSuite(
        pool_id=pool.id,
        tasks=tasks,
        overlap=1,
    )
    return new_tasks_suite


# # # Main pipeline starts here

# Create or reuse a Toloka project
project = create_or_update()
print("Project id:" + project.id)

# Create or reuse a pool from the project
pool = create_or_get_pool(project)
print("Pool id:" + pool.id)

# Create the tasks from db entries
tasks = create_game(pool)

# Wrap the tasks in a task suite (Still don't know why)
task_suite = create_task_suite(tasks, pool)

# Upload the task suite to the pool)
# This will create 1 task with 2 questions
toloka_client.create_task_suite(task_suite)


# This starts the pool.
toloka_client.open_pool(pool.id)

# TODO: Test this


# Function from toloka-kit github, used to wait until the pool is closed
def wait_pool_for_close(pool, sleep_time=60):
    # updating pool info
    pool = toloka_client.get_pool(pool.id)
    while not pool.is_closed():
        print(
            f'\t{datetime.datetime.now().strftime("%H:%M:%S")}\t'
            f'Pool {pool.id} has status {pool.status}.'
        )
        time.sleep(sleep_time)
        # updating pool info
        pool = toloka_client.get_pool(pool.id)


wait_pool_for_close(pool)