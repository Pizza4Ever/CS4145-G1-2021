import time

import toloka.client as toloka
import datetime
import sqlite3

### Variables one should modify
project_name = "Remove the images!"
pool_name = "My Pool!"
hints_required = 5
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
    input_specification = {'query_image': toloka.project.field_spec.ArrayUrlSpec(), 'image_id': toloka.project.field_spec.ArrayStringSpec()}
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
        if p.public_name == name:
            return p
    return False


# Either creates a new project or updates an already existing one
def create_or_update():
    new_project = create_project()
    p = find_project(project_name)
    if p and not p.status == toloka.project.Project.ProjectStatus.ARCHIVED:
        print("Updating the project")
        new_project = toloka_client.update_project(p.id, new_project)
    else:
        print("Creating a new project")
        new_project = toloka_client.create_project(new_project)
    return new_project


# Create or reuse a Toloka project
project = create_or_update()
print("Project id:" + project.id)
