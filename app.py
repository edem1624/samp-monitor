"""
SAMP server info logger
"""
import argparse
import logging
import os
import sys
import time

import requests
from samp_py.client import SampClient


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(
        description='Checks for users on server and sends a webhook request with the players.'
    )
    parser.add_argument(
        '-w', '--wait-time',
        type=int,
        default=3,
        required=False,
        help="Wait time between checks in seconds (default: 3 seconds)"
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Enable verbose logs',
        action='store_const', dest='loglevel', const=logging.DEBUG,
        default=logging.INFO
    )
    options = parser.parse_args()
    logging.basicConfig(
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=options.loglevel
    )

    url = os.getenv('DISCORD_WEBHOOK')
    server_host = os.getenv('SAMP_SERVER_HOST')
    server_port = int(os.getenv('SAMP_SERVER_PORT', '7777'))

    if url is None:
        logging.critical("DISCORD_WEBHOOK must be defined!")
        sys.exit(1)

    if server_host is None or server_port is None:
        logging.critical("SAMP_SERVER_HOST and SAMP_SERVER_PORT must be defined!")
        sys.exit(1)

    players = ''
    while True:

        with SampClient(address=server_host, port=server_port) as client:
            try:
                info = client.get_server_info()
                logging.info(info)
                if int(info.players) > 0:
                    if len([player.name for player in client.get_server_clients_detailed()]) == 0:
                        continue
                    current = ', '.join(
                        [player.name for player in client.get_server_clients_detailed()]
                    )
                else:
                    current = 'No Players'
                print(current)
            except:
                logging.info("Error occured during getting server info")
            if players != current:
                players = current
                data = {
                    "content" : f"Players: {players}",
                    "username" : "ECS Figyelo"
                }

                result = requests.post(
                    url,
                    json=data,
                    timeout=600
                )

                try:
                    result.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    logging.exception("Exception occurred: %s", err)
                else:
                    logging.info("Payload delivered successfully, code %s.", result.status_code)
        time.sleep(3)


if __name__ == '__main__':
    main()
