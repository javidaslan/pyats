from netmiko import ConnectHandler

def connect(host, username, password):
    """
    Connect to device via SSH
    :param host:
    :param username:
    :param password:
    :return: connection object
    """
    connection_details = {'host':host, 'device_type': 'cisco_ios', 'username': username, 'password': password}
    try:
        print('-' * 50)
        print(f"Connecting to {host}")
        connection_object = ConnectHandler(**connection_details)
        print(f"Connection to {host} is SUCCESSFUL")
        return connection_object
    except Exception as ex:
        print(ex)
        return None

hosts = ['10.20.1.2']
username = "admin"
password = "admin"

for host in hosts:
    connection_object = connect(host=host, username=username, password=password)
    if connection_object:
        output = connection_object.send_config_set(["no username test"])
        if 'confirm' in output:
            connection_object.send_config_set(["\n"])
        print(output)
        connection_object.disconnect()
        print(f"Disconnected from {host}")