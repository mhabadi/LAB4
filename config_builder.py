import yaml
import logging
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader
logger=logging.getLogger(__name__)
f_handler=logging.FileHandler('file.log')
f_handler.setLevel(logging.DEBUG)
f_format=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
try:
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
        logger.debug(f"Logged into {router['name']} successfully")
        output=net_connect.send_config_set(output_config.split("\n"))
        logger.debug(output)
        net_connect.disconnect()
except:
    logger.exception("An Error Occured")
