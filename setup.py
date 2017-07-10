
# coding: utf-8

# In[15]:

import os
import pip


# In[16]:

# Establish constants

file_name = 'Open_HOTSLogs_Page.py'

# Name of the batch file
batch_file = 'Open_HOTSLogs_Page.bat'

# Name of the AutoHotkey File
ahk_file = "Open_HOTSLogs_Page.ahk"

# Name of xml file that can be imported to task scheduler
xml_file = "Open_HOTSLogs_Hotkey.xml"
xml_name = "Push HOTSLogs Hotkey"
# List of modules to install
modules = ['requests', 'lxml', 'bs4', 'pushbullet.py', 'requests']


# Determine the directory the python file is contained in.
directory = os.path.dirname(os.path.realpath(__file__))


# In[17]:

# Specify the contents of the batch file and the autohotkey file.

batch_content = """@echo off
cd C:\Python Files
python "%s" """ % (directory + "\\" + file_name)


ahk_content = """; This script runs the Open HOTSLogs Page Python script
; Edit it to match the directory
; If you already have a 
^#h::Run "%s"
;------------------------------------------------------------------------------------""" % (directory + "\\" + batch_file)

xml_content = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2016-03-03T09:15:05.0155213</Date>
    <Author>Domain\User</Author>
    <URI>%s</URI>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
    <CalendarTrigger>
      <Repetition>
        <Interval>PT3H</Interval>
        <Duration>P1D</Duration>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>2016-09-08T06:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>false</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <DisallowStartOnRemoteAppSession>false</DisallowStartOnRemoteAppSession>
    <UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>20</Count>
    </RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>"C:\Program Files\AutoHotkey\AutoHotkey.exe"</Command>
      <Arguments>"%s"</Arguments>
    </Exec>
  </Actions>
</Task>""" % (xml_name, directory + "\\" + ahk_file)


# In[18]:

def install(package):
    pip.main(['install', package])

def write_file(file_name, content):
    print("Writing content to %s" % file_name)
    with open(file_name, "w") as handle:
        handle.write(content)


# In[19]:

write_file(directory + "\\" + batch_file, batch_content)
write_file(directory + "\\" + ahk_file, ahk_content)
write_file(directory + "\\" + xml_file, xml_content)


# In[7]:

# Iterate over the modules list and install each module using pip
for module in modules:
    print ('Installing module %s' % module)
    install(module)


# In[14]:

import requests

#https://dzone.com/articles/how-download-file-python
# http://masnun.com/2016/09/18/python-using-the-requests-module-to-download-large-files-efficiently.html

# URL To Download Entire EOD Database
ahk = {'url' : "https://autohotkey.com/download/ahk-install.exe", 
'target_path' : directory + "\\ahk.exe", 'file_name' : 'ahk.exe'}



def download_file(url, target_path, file_name):
    print "Downloading %s to %s" % (file_name, target_path)
    response = requests.get(url, stream=True)
    #print file_name[-4:]
    if file_name[-4:] in ['.zip', '.exe']:
        print ("Writing binary %s file...") % (file_name[-3:])
        handle = open(target_path, "wb")
    else:
        handle = open(target_path, "w")
        print ("Writing file...")
    for chunk in response.iter_content(chunk_size=10240):
        if chunk:
            handle.write(chunk)
    #urllib.urlretrieve(url, "F:\Equity Data\EOD.zip")
    print "Downloaded %s" % file_name
    
# Install AHK silently
# https://autohotkey.com/board/topic/8403-installing-autohotkey-itself-silently/
download_file(ahk['url'], ahk['target_path'], ahk['file_name'])
ahk_install = "%s /S /D=C:\Program Files\AutoHotkey" % ('"' + ahk['target_path' ] + '"')
print ('Installing AutoHotkey')
os.system(ahk_install)
print ('AutoHotkey Installed')
os.remove(ahk['target_path'])
print ('Temporary Files removed.')
print ('Setup complete.')


# In[27]:

# Create a Task Scheduler task.
# https://stackoverflow.com/questions/26079021/windows-create-task-schedule-from-command-prompt-with-modified-power-condition
def create_task(xml_name, xml_file):
    print('Creating task %s...' % (xml_name)) 
    os.system('schtasks /create /XML %s /TN %s' % ('"' + directory + '\\'+ xml_file + '"', '"' + xml_name +'"'))
    print('Successfully created task %s.' % (xml_name))
    
create_task(xml_name, xml_file)    


# In[26]:

#To uninstall use os.system("'C:\Program Files\AutoHotkey\uninst.exe' /S")
'schtasks /create /XML %s /TN %s' % (directory + '\\'+ xml_file, '"' + xml_name +'"')

