# this simple script loads testbed file and connects to devices in this testbed
# script performs following on devices

# Routers:

# 1. parse show interfaces and save resutls
# 2. create loopback interface and save results
# 3. find difference between two configurations

# Switches:

# 1. parse show interfaces and save results
# 2. create vlan interface and save results
# 3. find difference between two configurations

from genie import testbed
import json
import os

# from pyats.topology import testbed
from genie.utils.diff import Diff


def save_output(destination_dir, destination_file, results):
    """
    Save the output into JSON file
    """
    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)
    with open(os.path.join(destination_dir, destination_file), "w") as f:
        if '.json' in destination_file:
            f.write(json.dumps(results, indent=3))
        else:
            f.write(results)

def process_commands(device, configure_commands, cleanup_commands, snapshot_command):
    """
    This function takes device object and list of commands.
    It takes pre and post snapshots from device and returns them.
    """
    try:
        pre_snapshot = device.parse(snapshot_command)
        device.configure(configure_commands)
        post_snapshot = device.parse(snapshot_command)
        device.configure(cleanup_commands)
        return pre_snapshot, post_snapshot
    except Exception as ex:
        print(ex)
        return None


def main():
    try:
        print(os.getcwd())
        # load testbed file
        testbed_object = testbed.load('testbed/testbed_markup.yaml')
        devices = testbed_object.devices
        configure_commands = None
        snapshot_command = 'show interfaces'
        cleanup_commands = None
        for device in devices:
            # disable initial config init_exec_commands=[], init_config_commands=[]
            devices[device].connect(init_exec_commands=[], init_config_commands=[], log_stdoud=False)
            if device.startswith('R'):
                configure_commands = ['interface Loopback 0', 'ip address 10.2.2.2 255.255.255.255', 'no shut']
                cleanup_commands = ['no interface Loopback 0']
            elif device.startswith('S'):
                configure_commands = ['interface vlan30', 'shut']
                cleanup_commands = ['no interface vlan30']

            pre_snapshot, post_snapshot = process_commands(device=devices[device], configure_commands=configure_commands,
                                                           cleanup_commands=cleanup_commands,
                                                           snapshot_command=snapshot_command)

            save_output(destination_dir='pre_snapshots',destination_file=f'{device}_interfaces_pre.json', results=pre_snapshot)
            save_output(destination_dir='post_snapshots',destination_file=f'{device}_interfaces_post.json', results=post_snapshot)

            diff = Diff(pre_snapshot, post_snapshot)
            diff.findDiff()
            print(diff)
            save_output(destination_dir='diffs', destination_file=f'diff_{device}_interfaces.txt', results=str(diff))

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()

