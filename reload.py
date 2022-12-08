import requests
import os

# add each of the variables to your environment as follows without the < > marks
# on linux/macOS as below, on windows go here: https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/
# export PA_USERNAME=<username on pythonanywhere>

# use this if running from GitHub Action
pa_username = os.environ["PA_USERNAME"]
api_token = os.environ["API_TOKEN"]
domain_name = os.environ["DOMAIN_NAME"]

response = requests.post(
    'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
        username=pa_username, domain_name=domain_name
    ),
    headers={'Authorization': 'Token {token}'.format(token=api_token)}
)
if response.status_code == 200:
    print('reloaded OK')
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))