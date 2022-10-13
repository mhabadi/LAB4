import yaml
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader
hosts=yaml.load(open('hosts.yml'),Loader=yaml.SafeLoader)
for router in hosts['hosts']:
    print(f'Routing table of {router["name"]}:)
    net_connect=Netmiko(host=router['ip'],
                           username=router['username'],
                           password=router['password'],
                           port=router['port'],
                           device_type=router['type'])
    output=net_connect.send_command("show ip route",use_textfsm=True)
    print(output)