import toloka.client as toloka
import toloka.client.project.template_builder as tb

token = ''

toloka_client = toloka.TolokaClient(token, 'SANDBOX')

requester = toloka_client.get_requester()
print('You have enough money on your account - ', requester.balance > 3.0)