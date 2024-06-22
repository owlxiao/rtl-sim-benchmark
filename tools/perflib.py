import subprocess
import json

perf_events = [
    "L1-dcache-loads",
    "L1-dcache-stores",
    "cycles",
    "instructions"
]


def check_events():
    result = subprocess.run("perf list", capture_output=True, shell=True)
    stdout = result.stdout.decode()

    for event in list(perf_events):
        if event not in stdout:
            print(f'Remove unsupported perf event: {event}')
            perf_events.remove(event)

    print('perf event: ', ' '.join(perf_events))


check_events()


def make_perf_command():
    perf_commands = ['perf', 'stat', '-j']

    if perf_events:
        perf_commands += ['-e', ','.join(perf_events)]

    perf_commands = ' '.join(perf_commands)
    return perf_commands


def parse_perf(perf: str):
    fields = {}

    for line in perf.split('\n'):
        if not line.strip():
            continue

        field = json.loads(line)

        if 'event' in field:
            value = field['counter-value']
            name = field['event'].replace(':u', '')

            if value == '<not counted>':
                continue
        else:
            value = field['metric-value']
            name = field['metric-unit']
            name = name.replace('%  ', '').replace(':u', '')

            if value == '<not counted>':
                continue

        fields[name] = value

    return fields
