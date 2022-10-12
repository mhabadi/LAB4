import yaml
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader
hosts=yaml.load(open('hosts.yml'),Loader=yaml.SafeLoader)
env=Environment(loader=FileSystemLoader('.'),trim_blocks=True, autoescape=True)
template=env.get_template('Routers_Template.j2')
for router in hosts['hosts']:
    file=open(f"{router['name']}_config.txt",'w')
    output_config=template.render(host=router)
    file.write(output_config)
    file.close()
    net_connect=Netmiko(host=router['ip'],
                        username=router['username'],
                        password=router['password'],
                        port=router['port'],
                        device_type=router['type'])
    print(f"Logged into {router['name']} successfully")
    net_connect.send_config_set(output_config.split("\n"))
    net_connect.disconnect()

