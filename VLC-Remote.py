import requests
import json
import time

passwd = ''
vlc_host = 'localhost:8080'
sync_server = 'localhost:3000'


def loop():
    prev_state = 'paused'
    while True:
        vlc_status = json.loads(requests.get('http://' + vlc_host + '/requests/status.json', auth=('', passwd)).text)
        state = vlc_status['state']
        if state != prev_state:
            payload = {'status': state}
            requests.post('http://' + sync_server + '/status/set', payload)
            print(state)

        server_state = json.loads(requests.get('http://' + sync_server + '/status').text)
        if state != server_state['status']:
            if server_state['status'] == 'playing':
                send_command('command=pl_play')
            if server_state['status'] == 'paused':
                send_command('command=pl_pause')

        prev_state = state
        time.sleep(0.2)


def send_command(command):
    return requests.get('http://' + vlc_host + '/requests/status.json?' + command,
                        auth=('', passwd))


if __name__ == '__main__':
    passwd = input('Please enter your VLC password:')
    sync_server = input('Please enter the address for the sync server:')
    loop()
