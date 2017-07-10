If you don't have Python installed, via the Ninite installer provided in the zip file.
It will automatically install Python on your system.

This script should be compatible with both Python 2 and Python 3, but I primarily write in Python 2 so there may be some discrepancies if you run it in Python 3.
Let me know if that's the case.

First run the setup.bat file in the Open HOTSLogs Page folder as Administrator.
The batch file needs Administrator access to create a task in Task Scheduler.

Then the script will download & silently install Autohotkey from https://autohotkey.com/
This allows you to access the script by pressing Ctrl + Windows Key + H.

The setup file will then set up a task in Task Scheduler to run the AutoHotkey Script by importing the xml file in the folder.
This task will cause the AutoHotKey (AHK} script to run at startup.

Next, let's set up the script.

When you run the script for the first time, you'll need to enter your Pushpullet API credentials.

You can get them by going to pushbullet.com on your desktop.
Then go to Settings.
Then you should see the Access Tokens heading aand a button that says Create Token.

Copy that token.

When you start the batch file (Open_HOTSLogs_Page.bat) for the first time, it will ask you for these api credentials.
Paste the API token into the command prompt.

Now select the devices thath correspond to your phone and tablet.
These only need to be filled in to use their respective capabilities.

You can always reset these options by typing ?setup into the script when it says "Enter Hero Name:" and it will rerun the setup process and recreate the variables.txt file.

Once you're completed these steps you should be good to go.