# This file shows an example of how the system can be used.
# I think this should provide lots of flexibility for 
# different studies.

# Import the scraper and the scraper services required
# for the given study.
from .scraper import Scraper
#from .frreqscrapeservice import FrReqScrapeService
#from .profscrapeservice import ProfScrapeService
from .friendsscrapeservice import FriendScrapeService
from .profscrapeservice import ProfScrapeService
from .past_events_scrape_service import PastEventsScrapeService
from .event_friends_scrape_service import EventFriendsScrapeService
from .cache_backend import CacheBackend

# Initialize the scraper with the credentials for the
# study participant (one-time passwords only!!!)
# Here, we read the credentials from env vars so that creds
# aren't being pushed to the public repo

def buildAndRunScraper(username, password):
    scraper = Scraper(username, password)
    # attach the backend to the scraper
    scraper.attach_backend(CacheBackend())

    scraper.attach_scraper(ProfScrapeService())
    scraper.attach_scraper(EventFriendsScrapeService())


    scraper.scrape()

    del scraper.user_dto.user_data["password"] # strip user's password before sending it back
    return scraper.user_dto.user_data