import toloka.client as toloka

# Create a file named token.txt and place your toloka token on the first line. Do not commit this file.
f = open("token.txt", "r")
token = f.read()
f.close()

toloka_client = toloka.TolokaClient(token, 'SANDBOX')

# This is just to test if your token is correct (If it fails, request a new toloka Oauth token)
requester = toloka_client.get_requester()
print(f'Your account: {requester}')

# # The code below shows how to create a new toloka project using html

# Construct a new project
new_project = toloka.project.Project(
    assignments_issuing_type=toloka.project.Project.AssignmentsIssuingType.AUTOMATED,
    public_name='What is this image about?',
    public_description='--Public description--',
)

# This is a toloka JavaScript library, which adds useful integration.
recording_assets = toloka.project.view_spec.ClassicViewSpec.Assets(
    script_urls=["$TOLOKA_ASSETS/js/toloka-handlebars-templates.js"]
)

# Create the page that a worker will see. We use the older HTML+JS+CSS method since it allows more for control.
project_interface = toloka.project.view_spec.ClassicViewSpec(
    script=open('./page/test.js').read().strip(),
    markup=open('./page/test.html').read().strip(),
    styles=open('./page/test.css').read().strip(),
    assets=recording_assets
)

# For this task, we have an input image and an output text.
# (They are labeled: image and result respectively, this is also the HTML reference)
input_specification = {'image_left': toloka.project.field_spec.UrlSpec(), 'image_right': toloka.project.field_spec.UrlSpec()}
output_specification = {'result': toloka.project.field_spec.StringSpec()}

new_project.task_spec = toloka.project.task_spec.TaskSpec(
    input_spec=input_specification,
    output_spec=output_specification,
    view_spec=project_interface
)

# Here the toloka client creates the project we constructed above
new_project = toloka_client.create_project(new_project)
