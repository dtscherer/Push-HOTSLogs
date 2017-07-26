
# coding: utf-8

# In[ ]:

import webbrowser
from pushbullet import Pushbullet
import pickle
import os
import requests
from bs4 import BeautifulSoup
import datetime


#Resources
#https://github.com/randomchars/pushbullet.py


# In[ ]:

# Declare variables

# Modifier options dictionary.

options = {'!' : 'phone' , '#' : 'tablet', '$' : 'browser'}

# Store api_key and other variables in a text file
# I Know it's insecure, I'll figure out how to fix that later
# Creates a dictionary with empty strings, we will replace the values later.
variables = {'api_key' : '' , 'phone' : '', 'tablet' : '', 'browser' : 'Chrome', 'last_updated' : datetime.date(2015,06,02), 'hero_list' : []}

# Set the directory of the python file.
directory =  os.path.dirname(os.path.realpath(__file__)) + '\\' #os.getcwd() + '\\'
file_name = 'variables.txt'
target_file = directory + file_name

# Determine files in directory
directory_files = os.listdir( os.path.dirname(os.path.realpath(__file__)))

def write_variables(variables, file_name):
    """Writes variables to a text file.
    Insecure, but gets the job done."""
    with open(file_name, 'wb') as handle:
        pickle.dump(variables, handle)

def load_variables(file_name):
    """Loads the variables from the text file."""
    with open(file_name, 'rb') as handle:
        variables = pickle.loads(handle.read())
    return variables
    
def strip_device(device):
    """Strips the Device('Device Name') wrapper from the device."""
    device = str(device)
    start = device.find("'")
    end = device[start +1 :].find("'")
    return device[start+1: start+1+ end]


    
def get_hero_list(variables):
    url = 'https://www.hotslogs.com/Default'
    heroes = []
    # get website content
    today = datetime.datetime.today().date()
    difference = (today - variables['last_updated']).days
    if difference >= 7:
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'lxml')
        #print soup
        table = soup.find(class_='rgMasterTable')
    
        for row in table.find_all('tr')[1:]:
            #print row
            col = row.find_all('td')
            column = col[1].string.strip()
            heroes.append(column)
        sorted_heroes = sorted(heroes)
        variables['hero_list'] = sorted_heroes
    else:
        sorted_heroes = variables['hero_list']
    
    return sorted_heroes, variables

def update_hero_list(variables):
    variables['last_updated'] = datetime.date(2015,06,02)
    sorted_heroes, variables = get_hero_list(variables)
    return variables

def request_variables(variables, file_name):
    """Requsests the variables from the user."""
    
    variables['api_key'] = raw_input('Enter Pushbullet API Key:')
    pb = Pushbullet(variables['api_key'])
    variables['last_updated'] = datetime.datetime.today().date()
    devices = pb.devices
    #print devices
    for i in range(0,len(devices)):
        print str(i) + ': ' + str(devices[i])
    variables['phone'] = strip_device(devices[int(raw_input('Select Phone: Enter Item Number in list 0 to %s\n' % len(devices)))])
    #print variables['phone']
    variables['tablet'] = strip_device(devices[int(raw_input('Select Tablet: Enter Item Number in list 0 to %s\n' % len(devices)))])
    #print variables['tablet']
    variables = update_hero_list(variables)
    write_variables(variables, file_name)
    return variables



def parse_hero_name(hero):
    """Parses the hero's name to correctly account for proper capitalization 
    as the hero names in the urls for HOTSLogs are case sensitive."""
    name = ''
    hero = hero.lower()
    for i in range(0,len(hero)):
        if i == 0:
            name = hero[i].upper()
        elif hero[i-1] == ' ':
            name += hero[i].upper()
        elif hero[i-1] == '.':
            name += hero[i].upper()
        elif hero[i-1] == '-':
            name += hero[i].upper()
        else:
            name += hero[i]
    return name



def parse_device_options(hero_string, options):
    if hero_string[0] in options:
        device = options[hero_string[0]]
        hero = hero_string[1:]
    else:
        device = None
        hero = hero_string
    return hero, device

#parse_device_options('D.Va', options)

def enter_hero_name(hero_list, options, variables):
    """Prompts for hero name."""
    print ("Enter Exact Hero Name Or Type ?help for more options.")
    
    hero, device = parse_device_options( raw_input('Enter Hero:'), options)
    hero = parse_hero_name(hero)
    if hero.lower() == '?help':
        print ('\nTyping the correct capitalization is unnecessary, but exact names with punctuation are.\n')
        print ('Type ?list For A List Of Heroe Names.\n')
        print ('Type ?update to manually update the list of hero names. Automatically performed weekly.\n')
        print ("Type a modifier before the hero name or ?list command to send to a Pushbullet device.\n")
        print ('! to send to your phone or # to your tablet. Use no modifier to send to your browser.\n')
        print ("For example type !D.Va to send D.Va's guide to your phone or #D.Va to send to your tablet.")
        print ('Or type #?list to select a hero from the list then send it to your tablet.\n')
        print ('Type ?setup to remove the current configuration files and re-enter the api_key and devices\n.')
        enter_hero_name(hero_list, options, variables)
    elif hero.lower() == '?setup':
        print('Configuring variables.')
        os.remove(os.getcwd() + '\\' + file_name)
        request_variables(variables, target_file)
        enter_hero_name(hero_list, options, variables)
    elif hero.lower() == '?list':
        hero = select_hero(hero_list)
        return hero, device
    elif hero.lower() == '?update':
        print ('Updating hero list.\n')
        update_hero_list(variables)
        print ('Hero list updated.\n')
        enter_hero_name(hero_list, options, variables)
    elif hero.lower() == 'exit':
        exit()
    elif hero in hero_list:
        return hero, device
    else:
        print('\nIncorrect hero name. Please try again or select from the list of heroes using the ?list command.\n')
        enter_hero_name(hero_list, options, variables)

def select_hero(hero_list):
    for i in range(0,len(hero_list)):
        print str(i) + ': ' + hero_list[i]
    hero_index = int(raw_input('Select Hero Number:'))
    return hero_list[hero_index]
    


def parse_hero_for_url(hero):
    name = ''
    for i in range(0,len(hero)):
        if hero[i] == ' ':
            name += '%20'
        elif hero[i] == "'":
            name += '%27'
        else:
            name += hero[i]
    return name    
 



# In[ ]:

if __name__ == "__main__":
    if file_name not in directory_files:
        variables = request_variables(variables, target_file)
    
    else:
        variables = load_variables(target_file)
        if variables['hero_list'] == []:
            variables = update_hero_list(variables)
    
    pb = Pushbullet(variables['api_key'])
    write_variables(variables, target_file)
    api_key = variables['api_key']
    
    hero_list, variables = get_hero_list(variables)
    
    hero, device = enter_hero_name(hero_list, options,variables)

    write_variables(variables, target_file)
    
    hero = parse_hero_for_url(hero)
    
    hotslogs_string = 'https://www.hotslogs.com/Sitewide/HeroDetails?Hero='

    hero_query = hotslogs_string + hero

    if device != None:
        device = pb.get_device(variables[device])
        push = pb.push_link("HOTSLogs: " + hero, hero_query, device = device)
    else:
        webbrowser.open(hero_query)

