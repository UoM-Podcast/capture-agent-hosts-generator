# Capture Agent Hosts Generator
## Generate an Ansible-compatible hosts file from a Google Sheet

This is used to generate an ansible inventory file for use with https://github.com/UoM-Podcast/capture-agent-ansible
There was an existing Google Sheets for keeping Capture Agent information in and it was the days before ansible dynamic
inventories. This script will generate a static ansible inventory from a google sheet.
Its important to note the script is based on the position of the cells in each row. Using the sheet below as an example
will ensure it works:
https://docs.google.com/spreadsheets/d/1g1sRqUJXVejfOj0WcHnc_6MO5jQ3kCl5JzlSDcBIDBY/edit?usp=sharing

### Install the dependencies:
```markdown
sudo apt-get install python-pip
sudo pip install --upgrade google-api-python-client oauth2client
sudo pip install yaml
```

### Get the google credentials
Generate yourself an Oauth client credential in the google cloud api:
https://console.cloud.google.com/apis/credentials
download the json and save in this directory as `credentials.json`

### Install the configuration
```markdown
cp conf.yaml.example conf.yaml
```

### Execute the script:
```markdown
chmod 775 updateAnsibleHosts.py
python updateAnsibleHosts.py
```
The script will attempt to open a new window or tab in your default browser. If this fails, copy the URL from the console and manually open it in your browser.

If you are not already logged into your Google account, you will be prompted to log in. If you are logged into multiple Google accounts, you will be asked to select one account to use for the authorization.

Click the Accept button.
The sample will proceed automatically, and you may close the window/tab.