import requests
import json
import time
from plexapi.server import PlexServer


def loop_vlc():
    prev_state = 'paused'
    while True:
        vlc_status = json.loads(requests.get(vlc_url + '/requests/status.json',
                                             auth=('', passwd)).text)
        state = vlc_status['state']
        if state != prev_state:
            payload = {'status': state}
            requests.post(sync_url + '/status/set', payload)
            print(state)

        server_state = json.loads(requests.get(sync_url + '/status').text)
        if state != server_state['status']:
            if server_state['status'] == 'playing':
                send_command('command=pl_play')
            if server_state['status'] == 'paused':
                send_command('command=pl_pause')

        prev_state = state
        time.sleep(0.2)


def loop_plex():
    prev_state = 'paused'
    while True:
        if client.isPlayingMedia():
            state = 'playing'
        else:
            state = 'paused'

        if state != prev_state:
            payload = {'status': state}
            requests.post(sync_url + '/status/set', payload)
            print(state)

        server_state = json.loads(requests.get(sync_url + '/status').text)
        if state != server_state['status']:
            if server_state['status'] == 'playing':
                client.play()
            if server_state['status'] == 'paused':
                client.pause()
        prev_state = state
        time.sleep(0.2)


def send_command(command):
    return requests.get(vlc_url + '/requests/status.json?' + command,
                        auth=('', passwd))


def get_prop(config, prop_key, prop_type=str):
    if prop_key in config:
        return prop_type(config[prop_key])
    else:
        return prop_type(input(f'Please enter the: {prop_key}:'))


if __name__ == '__main__':
    try:
        with open('config.json') as config_file:
            config = json.loads(config_file.read())
    except:
        config = {}

    client_type = get_prop(config, 'client_type')
    sync_url = get_prop(config, 'sync_url')

    if client_type == 'vlc':
        passwd = get_prop(config, 'passwd')
        vlc_url = get_prop(config, 'vlc_url')
        loop_vlc()

    elif client_type == 'plex':
        token = get_prop(config, 'token')
        plex_url = get_prop(config, 'plex_url')
        client_name = get_prop(config, 'client_name')
        plex = PlexServer(plex_url, token)
        client = plex.client(client_name)
        client.pause()
        loop_plex()

    else:
        print('Invalid client type!!!!!')
