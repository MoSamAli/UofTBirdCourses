from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options




def course_eval_scraper():
    """
    Web Scrapes UofTs past course evaluations.
    """
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    driver = webdriver.Chrome(chrome_options=chrome_options)
    html = driver.get("https://course-evals.utoronto.ca/BPI/fbview.aspx?blockid=aRhZxxtkJnXYgKD7Yu&userid=TCQfI0jRi3IuyV6ZtCgP92DvlivsVQ3PB0Vi&lng=en")

    #for tr in driver.find_elements_by_tag_name("tr"):
        #for td in tr.find_elements_by_tag_name("td"):
            #print(td.get_attribute("innerText"))

    html_soup = BeautifulSoup(html, 'html.parser')
    course_containers = html_soup.find_all('div', class_ = 'gData')
    print(type(course_containers))
    print(len(course_containers))
    #type(html_soup)
    #return simple_get('https://course-evals.utoronto.ca/BPI/fbview.aspx?blockid=aRhZxxtkJnXYgKD7Yu&userid=TCQfI0jRi3IuyV6ZtCgP92DvlivsVQ3PB0Vi&lng=en')

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

if __name__ == '__main__':
    print(course_eval_scraper())
