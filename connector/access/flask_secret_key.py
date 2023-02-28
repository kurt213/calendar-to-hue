import secrets
import json
from os.path import exists

def get_key():

    if exists('connector/access/flask_secret_key.json'):
        with open('connector/access/flask_secret_key.json', 'r') as f:
            json_output = json.load(f)
        f.close()
    else:
        with open('connector/access/flask_secret_key.json', 'w') as f:
            json_output = {'flask-secret-key': secrets.token_hex(32)}
            json.dump(json_output, f)
        f.close()

    return json_output['flask-secret-key']

if __name__ == '__main__':
    output = get_key()
    print(output)