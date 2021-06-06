import time

import toloka.client as toloka
import datetime
import sqlite3

### Variables one should modify
project_name = "Where are you hiding?"
pool_name = "My Pool!"
hints_required = 5
URL = 'https:123toloka.nl:5000/static/'
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
        # Toloka supports HTML markup
        public_description="""
        In this task you are actually playing a game of hide and seek. You are tasked with hiding and will do that in up to 5 different locations. Each location represented by an image and
        at the moment all locations are classrooms.
        To help the other player (the seeker) find you, you must provide 3 to 5 contextual hints for each location.
        Explanation on what a contextual hint is, is given in the assignment.
        Asking for contextual hints prevents naming objects in the image, which would make the game very easy for the seeker (other player).
        """
    )
    new_project.public_instructions ="""
        <h1>Can you be found?</h1>
        <p>In this task you are actually playing a game of hide and seek. You are tasked with hiding and will do that in up to 5 different locations, each location represented by an image.
        At the moment all locations are classrooms. <br>
        To help the other player (the seeker) find you, you must provide 3 to 5 contextual hints for each location.</p>
        
        
        <h2>Locations: different types of classroom</h2>
        You will be given 5 locations to hide in. Each location represents a classroom. <br>
        For each location you hide in, a seeker (another real player in this game) is tasked in finding you. To do that they will be given 25 images of classrooms, including one you are "hiding in".
        To be able to deduct in which particular classroom you are hiding, they will be given the hints you provide in this task.
        
        <h2> Creating hints </h2>
        The hints that you will provide in this task are so-called "contextual" descriptions. Just stating objects that are present in the image would make the game to easy for the seeker, therefore you
        are asked to create hints that describe (potential) situations portrayed by the image.<br> Instead of the hint <q>There's a pencil</q>, a more contextual hint would be <q>I can create drawings here</q>.
        Both hints indicate the presence of a pencil, but only the latter describes a fitting context for that pencil in the given image. <br>
        For each location you hide in (image) you are asked to provide at least 3 contextual hints. Each hint will be of a different type. As contextual hints can still include objects or other straightforward
        terms, each image is accompanied with a black list of words you can not use in your hints.<br>

        There are 6 different kinds of contextual hints that could be asked of you. These are explained below.

        <h3>Activity context</h3>
        <b>Example:</b><i></>
        
        <h3>Role context</h3>
        <b>Example:</b><i></>

        <h3>Temporal context</h3>
        <b>Example:</b><i></>

        <h3>Relation context</h3>
        <b>Example:</b><i></>

        <h3>Mood context</h3>
        <b>Example:</b><i></>

        <h3>Goal context</h3>
        <b>Example:</b><i></>





        <h2>Purpose of this game</h2>
        """

    # This is a toloka JavaScript library, which adds useful integration.
    recording_assets = toloka.project.view_spec.ClassicViewSpec.Assets(
        script_urls=["$TOLOKA_ASSETS/js/toloka-handlebars-templates.js"]
    )

    # Create the page that a worker will see. We use the older HTML+JS+CSS method since it allows more for control.
    project_interface = toloka.project.view_spec.ClassicViewSpec(
        script=open('./page/question1.js').read().strip(),
        markup=open('./page/question1.html').read().strip(),
        styles=open('./page/question1.css').read().strip(),
        assets=recording_assets
    )

    # For this task, we have an input image and an output text.
    # (They are labeled: image and result respectively, this is also the HTML reference)
    input_specification = {'query_image': toloka.project.field_spec.UrlSpec(), 'image_id': toloka.project.field_spec.StringSpec()}
    output_specification = {'result0': toloka.project.field_spec.StringSpec(required=True),
                            'result1': toloka.project.field_spec.StringSpec(required=True),
                            'result2': toloka.project.field_spec.StringSpec(required=True),
                            'result3': toloka.project.field_spec.StringSpec(required=False),
                            'result4': toloka.project.field_spec.StringSpec(required=False)}

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
    pool = toloka.pool.Pool(
        project_id=project.id,
        private_name=pool_name,
        may_contain_adult_content=True,
        will_expire=datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        reward_per_assignment=0.02,
        auto_accept_solutions=False,
        auto_accept_period_day=1,
        assignment_max_duration_seconds=60 * 2,
        filter=toloka.filter.Languages.in_('EN'),
        defaults=toloka.pool.Pool.Defaults(default_overlap_for_new_task_suites=1),
    )
    pool = toloka_client.create_pool(pool)
    return pool


# This function checks for existing pools with the specified name, if one exists it is reused
def create_or_get_pool(project):
    pools = toloka_client.find_pools(project_id=project.id)
    for p in pools.items:
        if p.project_id == project.id and p.private_name == pool_name and not p.is_archived():
            print("Found previous pool")
            return p
    print("Creating new pool")
    return create_pool(project)


# Opens a connection with the SQLite db, pulls all images that lack the specified amount of hints
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
            storage[f[0]].append(f)
    con.commit()
    con.close()
    return storage


# Creates the task description based on the items returned from fetch_image_from_db
def create_tasks(pool):
    storage = fetch_images_from_db()
    tasks = []
    # Key is the img name, value is a list of hints.
    print(storage)
    for key, value in storage.items():
        if len(value) < hints_required:
            tasks.append(toloka.task.Task(
                input_values={
                    'query_image': URL + key,
                    'image_id': key
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
tasks = create_tasks(pool)

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

# TODO: Result retrieval
