import os
import json

HOME = os.environ['HOME']
PLOTLY_HOME = HOME + '/.plotly'
PLOTLY_CREDENTIALS_FILE = PLOTLY_HOME + '/.credentials'
PLOTLY_CREDENTIALS = {
    'username': 'gmarciani',
    'api_key': '3q9thjrhtr'
}

if not os.path.exists(PLOTLY_HOME):
    os.makedirs(PLOTLY_HOME)

if not os.path.isfile(PLOTLY_CREDENTIALS_FILE):
    with open(PLOTLY_CREDENTIALS_FILE, 'w') as fp:
        json.dump(PLOTLY_CREDENTIALS, fp, sort_keys=False, indent=4)

with open(PLOTLY_CREDENTIALS_FILE, 'r') as fp:
    credentials = json.load(fp)

print('[Plotly] Logged as ' + credentials['username'] + ' with api key ' + credentials['api_key'])