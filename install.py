#!/usr/bin/python3
import os
import sys
import shutil
import configparser

config = configparser.ConfigParser()
config.read('app.ini')

HOME = os.path.expanduser('~')
APPS_DIR = os.path.join(HOME,'.app')
APP_NAME = config.get('Config','AppName')

try:
    NAME = config.get('Config', 'Name')
except configparser.NoOptionError:
    NAME = APP_NAME    
try:
    CATEGORIES = config.get('Config','Categories')
except configparser.NoOptionError:
    CATEGORIES = "Utility"
try:
    APP_VERSION = config.get('Config','Version')
except configparser.NoOptionError:
    APP_VERSION = '1.0'
EXEC = config.get('Config','Exec')

def generate_desktop_file():
    
    desktop_file = configparser.ConfigParser()
    desktop_file.optionxform = str
    desktop_file.add_section("Desktop Entry")
    desktop_file.set("Desktop Entry", "Version", APP_VERSION)
    desktop_file.set("Desktop Entry", "Type", 'Application')
    desktop_file.set("Desktop Entry", "Name", NAME)
    desktop_file.set("Desktop Entry", "Exec", os.path.join(APPS_DIR,APP_NAME,EXEC)) #TODO add app path 
    desktop_file.set("Desktop Entry", "Icon", APP_NAME+'.png')
    desktop_file.set("Desktop Entry", "Terminal", 'False')
    desktop_file.set("Desktop Entry", "StartupNotify", 'False')
    desktop_file.set("Desktop Entry", "Categories", CATEGORIES)

    with open(os.path.join(HOME,'.local/share/applications/'+APP_NAME+'.desktop'), "w") as file:
        desktop_file.write(file)

def install():
    if not os.path.exists(APPS_DIR):
        os.mkdir(APPS_DIR)

    shutil.copytree(APP_NAME,os.path.join(APPS_DIR,APP_NAME))
    # shutil.copyfile(APP_NAME+'.desktop',os.path.join(HOME,'.local/share/applications/'+APP_NAME+'.desktop'))
    shutil.copyfile(APP_NAME+'/assets/icon.png', os.path.join(HOME,'.local/share/icons/',APP_NAME+'.png'))
    generate_desktop_file()
    os.chmod(os.path.join(APPS_DIR,APP_NAME,EXEC), 0o755)

def uninstall():
    if os.path.exists(os.path.join(APPS_DIR,APP_NAME)):
        shutil.rmtree(os.path.join(APPS_DIR,APP_NAME))

    if os.path.exists(os.path.join(HOME,'.local/share/applications/',APP_NAME+'.desktop')):
        os.remove(os.path.join(HOME,'.local/share/applications/',APP_NAME+'.desktop'))

    if os.path.exists(os.path.join(HOME,'.local/share/icons',APP_NAME+'.png')):
        os.remove(os.path.join(HOME,'.local/share/icons',APP_NAME+'.png'))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '-u':
            uninstall()
            print('Удаление завершено!')
    else:
        install()
        print('Установка завершена!')
    