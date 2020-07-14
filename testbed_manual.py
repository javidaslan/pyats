from pyats.topology import Testbed, Device, Interface, Link

# create your testbed
testbed = Testbed('manuallyCreatedTestbed',
                  alias = 'iWishThisWasYaml',
                  passwords = {
                    'tacacs': 'lab',
                    'enable': 'lab',
                  },
                  servers = {
                    'tftp': {
                        'name': 'my-tftp-server',
                        'address': '10.1.1.1',
                    },
                  })

# create your devices
device = Device('tediousProcess',
                alias = 'gimmyYaml',
                connections = {
                    'a': {
                        'protocol': 'telnet',
                        'ip': '192.168.1.1',
                        'port': 80
                    }
                })

# create your interfaces
interface_a = Interface('Ethernet1/1',
                        type = 'ethernet',
                        ipv4 = '1.1.1.1')
interface_b = Interface('Ethernet1/2',
                        type = 'ethernet',
                        ipv4 = '1.1.1.2')

# create your links
link = Link('ethernet-1')

# now let's hook up everything together
# define the relationship.
device.testbed = testbed
device.add_interface(interface_a)
device.add_interface(interface_b)
interface_a.link = link
interface_b.link = link

print(dir(testbed))