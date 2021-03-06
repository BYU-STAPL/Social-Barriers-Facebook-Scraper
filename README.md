# Social-Barriers-Facebook-Scraper


## To get started on a new computer (locally)

### macOS Instructions
#### Install Chrome Driver for macOS
Navigate to `https://chromedriver.chromium.org/downloads` (download the driver corresponding to your CPU architecture (i.e. intel vs. M1))

Unzip the downloaded folder. Navigate to the directory where the `chromedriver` file was unzipped to.

Move the chromedriver to your bin directory:

`mv chromedriver /usr/local/bin`

#### Clone the repository
Navigate to where you would like to store the scraping code. Run

`git clone https://github.com/BYU-STAPL/Social-Barriers-Facebook-Scraper.git`

#### Install virtual environment packages
`python3 -m pip install --user virtualenv`

Create a virutal Python environment:

`python3 -m venv environment`

Activate the environment:

`source ./environment/bin/activate`

Install the Python module dependencies:

`pip install -r requirements.txt`

Set the FLASK_APP virtual environment variable:

`export FLASK_APP=server`

Start the flask server:

`flask run
`

### Windows Instructions

#### Install Chrome Driver for Windows
Install Google Chrome.
Determine what version of Chrome you have (https://www.digitalcitizen.life/version-google-chrome/)
Then, navigate to https://chromedriver.chromium.org/downloads and download the corresponding chrome driver.
Create a global PATH environment variable pointing to the chromedriver (if you don't know how to do that, see this video: https://www.youtube.com/watch?v=dz59GsdvUF8)

#### Clone the Repository
Open the File explorer and navigate to the folder you'd like to store the scraper in, e.g.,
`cd Users\STaPL\Desktop\FB-prototype\`
Right click inside the folder and click:
`Git Bash Here` (assumes Git Bash is installed)
Then clone the repository.
`git clone https://github.com/BYU-STAPL/Social-Barriers-Facebook-Scraper.git`
You can now close out of Git Bash.

#### Enable and Run Flask
Next, open cmd and navigate to the folder just created, e.g.
`cd Users\STaPL\Desktop\FB-prototype\Social-Barriers-Facebook-Scraper`
Create a virutal Python environment:
`python3 -m venv environment`
Activate the environment:
`environment\Scripts\activate`
Install the Python module dependencies:
`pip install -r requirements.txt`
Set the FLASK_APP virtual environment variable:
`setx FLASK_APP "server.py"`
Start the flask server:
`flask run`

You should now see that the flask server is running. This will handle calls to scrape data.
#### Install Selenium for Windows:

## Notes about project structure

### Flask server
The file `server.py` catches HTTP requests and listens on port localhost:5000. It expends a logIn POST request containing a Facebook username and password. It then calls `buildAndRunScraper(username, password)` from the `BuildSocialBarriersScraper.py` file. This creates an instance of Scraper (defined in `scraper.py`). The implementation is simple. The backend defines how the data scraped will be stored. In our case, we are simply caching this data in computer memory before sending it back to the Vue app.

Scraper services are also attached to the scraper. A scraper service is a class that implements an abstract class requiring a `scrape(self, user_dto, browser)` method.

`user_dto` is a class that wraps a Python dictionary where all data scraped can be stored. `browser` is basically a reference to the chrome driver.

Data can be scraped by calling methods on the `browser` and then storing desired data in `user_dto`. After the scraper's `scrape()` function has finished calling all of the scrape service's `scrape(self, user_dto, browser)` methods, `buildAndRunScraper` returns the `user_data` from the `user_dto` object.


## Experiments with a server computer:

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
