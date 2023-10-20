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

def summarize_log(content, max_length):
    lines = [l for l in content.split('\n') if should_show_log_line(l)]
    lines_concatenated = '\n'.join(lines)
    if len(lines_concatenated) < max_length:
        return lines_concatenated, False

    summarized = ''

    # Add lines from start until a length of `max_length / 2` is reached
    while len(lines) > 0 and len(summarized) + len(lines[0]) < max_length / 2:
        summarized = summarized + lines[0] + '\n'
        del lines[0]

    # Add lines from end until a length of max_length is reached, if there are still lines left
    if len(lines) > 0:
        summarized_end = ''
        while len(lines) > 0 and len(summarized) + len(summarized_end) + len(lines[-1]) + 6 < max_length:
            summarized_end = lines[-1] + '\n' + summarized_end
            del lines[-1]
        summarized = summarized + '\n...\n\n' + summarized_end

    return summarized, True

def should_show_log_line(line):
    return not ('%' in line and not '100%' in line)

def start_phase():
    send_discord_message('Starting TrueNAS sync with backups now.')

def end_phase(log_file):
    f = open(log_file, 'r')
    log_content = f.read()
    f.close()

    log_content, is_truncated = summarize_log(log_content, 1500)

    message = f'TrueNAS sync complete. {"Truncated l" if is_truncated else "L"}og file `{log_file}`:\n```{log_content}```'
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
