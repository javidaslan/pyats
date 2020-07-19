# this simple script loads testbed file and connects to devices in this testbed
# after connection it issues 'show version' command and parses the output to JSON
# all available parser can be found here
# https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers

from genie import testbed
import json
# from pyats.topology import testbed

def save_output(results):
    """
    Save the output into JSON file
    """
    with open("results.json", "w") as f:
        f.write(json.dumps(results, indent=3))

def main():
    results = []
    try:
        # load testbed file
        testbed_object = testbed.load('testbed_markup.yaml')
        devices = testbed_object.devices
        for device in devices:
            # disable initial config init_exec_commands=[], init_config_commands=[]
            devices[device].connect(init_exec_commands=[], init_config_commands=[])
            output = devices[device].parse('show version')
            results.append(output)
        save_output(results)
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()

