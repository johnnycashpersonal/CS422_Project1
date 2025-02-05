import time
import requests
from bs4 import BeautifulSoup

class WebScraper:
    """
    A web scraper class to fetch and parse HTML content from web pages.

    Attributes:
        base_url (str): The base URL of the website to scrape.

    Methods:
        get_code(url, retries=3, delay=60):
            Fetches the HTML content of a webpage.
        
        get_departments(soup):
            Extracts department URLs from the main page's HTML content.
        
        get_faculty(soup):
            Extracts faculty names from a department page's HTML content.
    """
    def __init__(self, base_url):
        self.base_url = base_url
        self.natural_sciences = ["anthropology",
                    "biology",
                    "chemistry",
                    "computerandinfoscience",
                    "geography",
                    "geologicalsciences",
                    "humanphysiology",
                    "mathematics",
                    "physics", 
                    "psychology"]

    def get_code(self, url, retries=3, delay=60):
        """
        Fetches the HTML content of a webpage.

        Args:
            url (str): The URL of the webpage to fetch.
            retries (int, optional): The number of times to retry fetching the webpage in case of failure. Defaults to 3.
            delay (int, optional): The delay in seconds between retries. Defaults to 60.
            Added 60 seconds to the delay each retry.

        Returns:
            BeautifulSoup: A BeautifulSoup object containing the parsed HTML content of the webpage if the request is successful.
            None: If the request fails after the specified number of retries.
        """
        for i in range(retries):
            #this website limits the amount of HTTP requests that can be made in a certain amount of time so I added a delay 60 seconds
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    return soup
                else:
                    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url}: {e}")
                if i < retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay += 60
                else:
                    print("Max retries exceeded.")
                    return None

    def get_departments(self, soup):
        ul_element = soup.find("ul", {"class": "nav", "id": "/arts_sciences/"})
        links = ul_element.find_all("a", href=True)
        urls = [self.base_url + link['href'] for link in links]
        return urls #finds the links to the departments and strips HTML tags

    def get_faculty(self, soup):
        faculty_div = soup.find_all('p', {'class': 'facultylist'})
        random_text = "The date in parentheses at the end of each entry is the first year on the University of Oregon faculty."
        faculty_list = [] #that random text is marked as part of thre faculty list so I removed it
        for faculty in faculty_div:
            if faculty.text != random_text:
                faculty_list.append(faculty.text)
        return faculty_list #finds the faculty names and strips useless info

    def strip_name(self, text):
        # Find the position of the first '<' character
        pos = text.find('<')
        if pos != -1:
            # Slice the text to remove everything after and including '<'
            text = text[:pos]
        return text.strip()
    
    def strip_fac_name(self, text):
        pos = text.find(',')
        if pos != -1:
            text = text[:pos]
        return text.strip() #strips the faculty names of any extra info

def main():
    base_url = 'https://web.archive.org'
    start_url = base_url + '/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/'
    scraper = WebScraper(base_url)
    
    soup = scraper.get_code(start_url)
    if soup:
        dep = scraper.get_departments(soup)
        natural_dep =[]
        for department in dep:
                for science in scraper.natural_sciences:
                    if science in department:
                        natural_dep.append(department)

        fac_list = {}
        for department in natural_dep:
            dep_soup = scraper.get_code(department)
            if dep_soup:
                dep_name = dep_soup.find('title').text
                dep_name = scraper.strip_name(dep_name)  # Clean up the department name
                print(dep_name) 
                faculty = scraper.get_faculty(dep_soup)
                fac_list[dep_name] = [scraper.strip_fac_name(fac) for fac in faculty]
            else:
                print(f"Failed to fetch content for {department}")
                break  # Stop the loop if a request fails

        with open('faculty_list.txt', 'w', encoding='utf-8') as file:
            for dep, faculty in fac_list.items():
                file.write(f"{dep}:\n")
                for fac in faculty:
                    file.write(f"{fac}\n")
                file.write("\n")
    else:
        print("Failed to fetch the main page.")

if __name__ == "__main__":
    main()