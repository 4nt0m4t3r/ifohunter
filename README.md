# ifohunt

# What is ifohunt

ifohunt is a tool designed to keep an eye on crypto exchanges, and notify the user whether one of the exchanges has introduced a new IFO project in their launchpad so that you never miss an IFO again!

# How it works?

ifohunt starts by following all the users that already followed the ifohunter instagram account (you can choose whatever account you want in the .env file), and did not yet get a follow back.After that, it will start  taking a screenshot of a specific section for every exchange websites written in `exchanges.txt` (last ifo header) in the IFO page. It will compare the hash of the screenshot with the hash of the previous screenshot taken. If they match, it will pass to the next exchange. If not, it will send an instagram notification to all the accounts that are followed by ifohunter. In summary, to receive a message from ifohunter when a new IFO is out, all you have to do is follow the ifohunter instagram account, and wait for a follow back, and of course accept it. And that's it! you will start receiving messages

# Requirements

## Functional requirements:

- Create a dummy instagram account that will be controled by the script.


## Technical requirements:

You have to provide the `INSTAGRAM_USERNAME` and  `INSTAGRAM_PASSWORD` variables in a .env file

Some packages to be installed:

- **google-chrome**  https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
- **chromedriver**   https://chromedriver.chromium.org/downloads
- **xvfb**
- **unzip**
- **pip3**


**Install additional libraries:**

```console
sudo apt update
sudo apt install libxss1 libappindicator1 libindicator7
sudo apt install -y unzip xvfb libxi6 libgconf-2-4
```

**Install pip3:**

```console
sudo apt install python3-pip
```


**Install chrome:**

```console
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt -y update
sudo apt -y install google-chrome-stable
```

**Install chromedriver:**

```console
unzip chromedriver_linux64.zip
chmod +x chromedriver
sudo mv -f chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```


**Note**

In case of a problem occuring, the script will take a screenshot of the browser upon exiting (error.png) and will place it in the screenshots directory 

**How to launch it?**

After installing all the above packages, all you have to do is:

```console
cd ifohunt/
pip3 install pipenv --upgrade
pipenv install
pipenv shell
python3 ifohunter.py
```

If you want to add it to a cronjob, a run.sh was included (need to modify paths). What you have to do is to add the following job to cron so it runs every 2 hours:

`0 */2 * * *  /bin/bash /[change this to project path]/run.sh`



