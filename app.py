import requests
import time
import requests
import os
from samp_py.client import SampClient

url = os.getenv('DISCORD_WEBHOOK')

players = ''

while True:

    with SampClient(address=os.getenv('SAMP_SERVER_HOST'), port=int(os.getenv('SAMP_SERVER_PORT'))) as client:
        info = client.get_server_info()
        print(info)
        if int(info.players) > 0:
            if len([player.name for player in client.get_server_clients_detailed()]) == 0:
                continue
            current = ', '.join([player.name for player in client.get_server_clients_detailed()])
        else:
            current = 'No Players'
        print(current)
        if players != current:
            players = current
            data = {
                "content" : f"Players: {players}",
                "username" : "ECS Figyelo"
            }

            result = requests.post(url, json = data)

            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print(f"Payload delivered successfully, code {result.status_code}.")
    time.sleep(3)


