import time
import pandas
from selenium import webdriver
from bs4 import BeautifulSoup

# Function to click the button on the page and wait a few seconds
def click_button():
    # Must redefine button to avoid stale error:
    button.click()
    time.sleep(3)  # Time allows the page to load (may depend on internet speeds)

# Function to write csv files with a pandas dataframe
def write_csv(dataframe, file_name):
    dataframe.to_csv(f"{file_name}.csv", encoding='UTF-8')

review_titles = []
authors = []
dates = []
reviews = []

for page in range(1, 50):
    print(page)
    try:
        url = "https://www.bestbuy.com/site/reviews/lg-4-5-cu-ft-he-smart-front-load-washer-and-7-4-cu-ft-electric-dryer-washtower-with-steam-and-built-in-intelligence-black-steel/6420312?variant=A&skuId=6420312&page="

        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")  # Fresh start every time so no interference
        #options.add_argument("--headless") # The chrome window won't pop up on screen and show animations

        driver = webdriver.Chrome(options=options, executable_path='./chromedriver.exe') # Initialize driver with chrome options defined above
        driver.get(url + str(page)) # Bring the browser to the url specified above
        driver.set_window_size(1200, 900) # Set window resolution so that all elements can still load on page
        print(driver.title)

        time.sleep(3)  # Give time to load full page

        while True:  # If the button exists, click it
            try:
                # Finding the "Show More" button at the bottom of the page
                button = driver.find_element_by_class_name("more-details")

                click_button()
                print("\"Show more\" buttton has been clicked")
                driver.back()
                time.sleep(2)
                print("\"Show more\" buttton has been clicked")

            except:
                break

        html = driver.page_source  # Once the full page with products is loaded, get the html data
        driver.quit()  # Close our automated browser
        print("Driver has been quit")

        html_soup = BeautifulSoup(html, "lxml")  # Parse the html data for analysis and sorting
        # print(html_soup)
        containers = html_soup.find_all('li', attrs={'class': 'review-item'})  # Find the containers that review
        # print(containers)

        # Create lists to be added to
        for contain in containers:  # Go through each on page
            # review_titles
            review_title = contain.find("h4", attrs={'class': 'c-section-title review-title heading-5 v-fw-medium'}).text
            print(review_title)
            review_titles.append(review_title)
            # authors
            author = contain.find("div", attrs={'class': 'ugc-author v-fw-medium body-copy-lg'}).text
            print(author)
            authors.append(author)
            # dates
            date = contain.find("div", attrs={'class': 'posted-date-ownership disclaimer v-m-right-xxs'}).text
            print(date)
            dates.append(date)
            # reviews
            review = contain.find("p", attrs={'class': 'pre-white-space'}).text
            print(review)
            reviews.append(review)
    except:
        pass

# Dictionary with headers and values of data
washtower_dict = {
    "Review_title": review_titles,
    "Author": authors,
    "Date": dates,
    "Review": reviews,
}

# Create structured dataframe of dictionary data for easy access and use
review_df = pandas.DataFrame(washtower_dict)

# Finally write file to csv for external use and print end statement
write_csv(review_df, "best_buy_washtower")
print("Web Scraping and CSV file writing complete!")
