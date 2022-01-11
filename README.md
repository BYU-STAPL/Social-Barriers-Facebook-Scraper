# Social-Barriers-Facebook-Scraper


## To get started on a new computer
Alright, to get this running on Digital Ocean, this is what I did:
I followed the instructions found here: https://keeganleary.com/setting-up-chrome-and-selenium-with-python-on-a-virtual-private-server-digital-ocean/
(note that after step 11, you need to unzip the .zip file that you download). If the link doesn't work for some reason, I've copied and pasted the instrucitons below.

Next, I cloned this repository to the Digital Ocean Droplet using:

`cd /var/www`

`git clone https://github.com/BYU-STAPL/Social-Barriers-Facebook-Scraper.git`

Then, I followed these instructions to be able to serve from a Flask Server: https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps

Note: instead of setting up a virtual environment, use: 

`pip3 install -r requirements.txt` to install dependencies. Then run

`export FLASK_APP=server`

`flask run`

To begin running the server.




### Setting up Chrome And Selenium with Python on a Virtual Machine Instructions (https://keeganleary.com/setting-up-chrome-and-selenium-with-python-on-a-virtual-private-server-digital-ocean/):
SSH into your VPS
In the terminal on your remote machine, update the package index
sudo apt update
sudo apt upgrade
Install wget if not installed already
wget --version skip to next step if you get a version number
sudo apt install wget if not found
Download Chrome with wget
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
Install the downloaded package
sudo dpkg -i google-chrome-stable_current_amd64.deb
Fix errors during install
sudo apt-get install -f
Test your intall
type google-chrome
If you receive error Unable to open X display. don't worry, we don't want a display!
Screen-Shot-2020-11-29-at-9.25.52-AM
Verify your version of Chrome
google-chrome --version
Mine is 87.0.4280.66.
Screen-Shot-2020-11-29-at-9.25.59-AM
On your local machine, go to https://chromedriver.chromium.org/downloads to get the link for the chrome driver for your installed version of Chrome on the remote machine.
Since mine is 87, I clicked the link that says "If you are using Chrome version 87, please download ChromeDriver 87.0.4280.20"
You may have a later vesion of Chrome when reading this.
You should now be on a page that looks like this:
Screen-Shot-2020-11-29-at-9.24.13-AM

Copy the link address to your clipboard

right click > Copy Link Address for chromedrive_linux64.zip
Address for mine was https://chromedriver.storage.googleapis.com/87.0.4280.20/chromedriver_linux64.zip
Download the chromedriver to your remote machine

wget {link you copied above}
for me: wget {https://chromedriver.storage.googleapis.com/87.0.4280.20/chromedriver_linux64.zip}
Move and adjust permissions for chromedrive (Yes, you must do this).

sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
Verify chromedriver is working

chromedriver --url-base=/wd/hub
terminal should tell you ChromeDriver was started successfully
quit
