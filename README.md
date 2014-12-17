# ACM eLibrary

### To setup the server:

    sudo apt-get update
    sudo apt-get install screen
    sudo apt-get install python-pip
    sudo pip install virtualenv
    cd location/of/acm-elibrary
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate

edit application/config.json
- **SCRIBD_API_KEY** and **SCRIBD_API_SECRET** are found at https://www.scribd.com/account-settings/api
- **AUTH_SERVER_APP_NAME** and **AUTH_SERVER_APP_PASSWORD** are the Crowd server credentials given by admin@acm.illinois.edu


### To run the server:

    screen
    sudo ./start.sh
    Ctrl-a d
