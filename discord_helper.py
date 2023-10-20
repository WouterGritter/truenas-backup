import os
import sys

from discord_webhook import DiscordWebhook
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')

print(f'DISCORD_WEBHOOK={DISCORD_WEBHOOK[:60]}...')

def send_discord_message(message):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK, content=message)
    webhook.execute()

def start_phase():
    send_discord_message('Starting TrueNAS sync with backups now.')

def end_phase(log_file):

    f = open(log_file, 'r')
    log_content = f.read()
    f.close()

    if len(log_content) > 1000:
        log_content = log_content[:1000] + '...'

    message = f'TrueNAS sync complete. Trunkated log file:\n```{log_content}```'
    send_discord_message(message)

def main():
    if len(sys.argv) < 2:
        print(f'Usage:')
        print(f'- python3 {sys.argv[0]} start-phase')
        print(f'- python3 {sys.argv[0]} end-phase <log-file>')
        exit(-1)

    phase = sys.argv[1]
    if phase == 'start-phase':
        start_phase()
    elif phase == 'end-phase':
        if len(sys.argv) < 3:
            print('Please provide a log file.')
            exit(-1)

        log_file = sys.argv[2]
        end_phase(log_file)
    else:
        print('Invalid phase!')

if __name__ == '__main__':
    main()
