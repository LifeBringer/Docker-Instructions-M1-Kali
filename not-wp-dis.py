#!/usr/bin/python3
# ADAPTED FROM: https://github.com/0xrutvij/wpVSkali/
# Alternative to WPDistillery for M1 Macs
"""Modify Compose File.

Usage:
  not-wp-dis.py [--wordpress=<ver>] [--wpPort=<port>]
  not-wp-dis.py (-h | --help)
  not-wp-dis.py (-v | --version)
  not-wp-dis.py (--listWpVer)

Options:
  -h --help            Show this screen.
  -v --version         Show version.
  --wordpress=<ver>    Wordpress version to use [default: latest].
  --wpPort=<port>      Port at which the Wordpress website is served [default: 8080].
  --listWpVer          List Wordpress versions available.

"""
import os
import os.path
import shutil
import stat
import yaml

from yaml import SafeDumper

from src.docopt import docopt

WORDPRESS_DIR = 'kaliFolder'
VER_LIST = 'vers'


class quoted(str):
    pass

def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)

def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

SafeDumper.add_representer(quoted, quoted_presenter)
SafeDumper.add_representer(
    type(None),
    lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', '')
  )

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Modify Compose File 0.3.0')
    #print(arguments)
    if arguments['--listWpVer']:
        if not os.path.exists(VER_LIST):
            if os.name == 'nt':
                os.system('python3 ./src/generateWpList.py')
            else:
                os.system('./src/generateWpList.sh')

        if os.path.exists(VER_LIST):
            listFile = VER_LIST
        else:
            print("Where are the versions?")
            exit

        with open(listFile) as list:
            vers = list.readlines()
            vers = [ver.strip() for ver in vers]
            print("Wordpress Versions available on Docker Hub: ")
            print(vers)

    else:
        with open("docker-compose.yml") as f:
            y=yaml.safe_load(f)

            if arguments['--wpPort'] == '8080':
                newPortMapping = '8080:80'
            else:
                newPortMapping =  arguments['--wpPort'] + ':80'

            if newPortMapping != y['services']['wordpress']['ports'][0]:
                opt = input('Changing the mapping of wordpress port to {}, continue [y/n]? '.format(newPortMapping))
                if opt in {'y', 'Y', 'yes', 'Yes'}:
                    y['services']['wordpress']['ports'][0] = newPortMapping
                else:
                    print("Operation aborted: Port mapping wasn't changed.")
            else:
                print("No change in port mapping detected.")

            if arguments['--wordpress'] == 'latest':
                newVer = 'wordpress'
            else:
                newVer = 'wordpress:'+arguments['--wordpress']

            if y['services']['wordpress']['image'] != newVer:
                # delete word press directory and change version logic, confirm with user
                opt = input('Changing Versions: This will delete the wordpress docker volume and wpFolder are you sure [y/n]: ')
                if opt in {'y', 'Y', 'yes', 'Yes'}:
                    y['services']['wordpress']['image'] = quoted(newVer)
                    prefix = os.path.basename(os.getcwd())
                    cmd = "docker volume rm {}_db".format(prefix.lower())
                    retVal = os.system(cmd)
                    if retVal != 0:
                        print('\nThe wordpress db volume was non-existent, thus the error. \nBut it is safe to proceed with docker compose up...')
                    else:
                        print('Wordpress db was deleted successfully.')
                    if os.name == 'nt':
                        shutil.rmtree(WORDPRESS_DIR, onerror=remove_readonly)
                    else:
                        shutil.rmtree(WORDPRESS_DIR)
                    os.mkdir(WORDPRESS_DIR)
                else:
                    print("Operation aborted: Wordpress version wasn't changed.")
            else:
                print("No change in Wordpress version detected.")

        with open("docker-compose.yml", 'w') as output:
            yaml.safe_dump(y, output, indent=2, default_flow_style=False, sort_keys=False)
