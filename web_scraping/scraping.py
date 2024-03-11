import logging
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



# Initialize Chrome
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install())
                          , options = options)

# Open URL
link = 'put-your-link-in-here'
driver.get(link)

# Choosing Province
provinces = driver.find_elements(By.XPATH, '//a[@class = "sitemap-link"]')

for province in range(len(provinces)):
    with open(f"house_scraping_pagination_{province}.csv", "w") as file:
        file.write(
            "judul; lokasi; kamar_tidur; kamar_mandi; luas_bangunan; luas_tanah; harga \n"
        )

    # Logging Config
    logging.basicConfig(filename=f'logs_house_scraping_{province}.log'
                        , format='%(asctime)s: %(levelname)s: %(message)s'
                        , datefmt='%d/%m/%y %H:%M:%S'
                        , level=logging.INFO
                        , filemode='w')

    # Maximize Windows
    driver.maximize_window()
    logging.info("Website was opened and the window was maximized successfully")
    driver.implicitly_wait(10)

    actions = ActionChains(driver)

    actions.key_down(Keys.CONTROL).click(provinces[province]).key_up(Keys.CONTROL).perform()
    logging.info("The province has been successfully selected.")
    driver.implicitly_wait(10)

    # Switch to Province's Windows
    province_windows = driver.window_handles[1]
    driver.switch_to.window(province_windows)
    logging.info("The transition to the Province's window was executed successfully.")
    driver.implicitly_wait(10)

    # Dropdown The City List
    dropdown_button = driver.find_element(By.XPATH, '//a[@class = "CrosslinkFilter-dropdown icon-dropdown-closed"]')
    dropdown_button.click()
    logging.info("The dropdown button was clicked successfully")
    driver.implicitly_wait(10)

    # Choosing City
    cities = driver.find_elements(By.XPATH, '//a[@class = "subLinks"]')

    for city in range(len(cities)):
        actions.key_down(Keys.CONTROL).click(cities[city]).key_up(Keys.CONTROL).perform()
        logging.info("The city has been successfully selected.")
        driver.implicitly_wait(10)

        # Switch to City's Windows
        city_windows = driver.window_handles[2]
        driver.switch_to.window(city_windows)
        logging.info("The transition to the city's window was executed successfully.")
        driver.implicitly_wait(10)

        pagination = True

        while pagination:
            with open(f"house_scraping_pagination_{province}.csv", "a", encoding="utf-8", errors='ignore') as file:
                # Selecting House
                houses = driver.find_elements(By.XPATH, '//h3[@class = "ListingCell-KeyInfo-title"]')
                # Selecting Address
                address = driver.find_elements(By.XPATH, '//span[@class = "ListingCell-KeyInfo-address-text"]')
                # Selecting price
                price = driver.find_elements(By.XPATH, '//div[@class = "ListingCell-KeyInfo-price"]/div[1]')
                for i in range(len(houses)):
                    # Extracting Title
                    judul = houses[i].text
                    logging.info("The title of the house was extracted successfully")

                    # Extracting Location
                    lokasi = address[i].text
                    logging.info("The address of the house was extracted successfully")

                    # Extracting Price
                    harga = price[i].text
                    logging.info("The price of the house was extracted successfully")

                    # Choose the House
                    houses[i].click()
                    logging.info("The house on the list was selected successfully")
                    driver.implicitly_wait(10)

                    # Switch to Property's Windows
                    property_windows = driver.window_handles[3]
                    driver.switch_to.window(property_windows)
                    logging.info("The transition to the property's window was executed successfully.")
                    driver.implicitly_wait(10)

                    # Extracting Amount of Bedrooms
                    try:
                        bedrooms = driver.find_element(By.XPATH, '//div[@data-attr-name = "bedrooms"]//following-sibling::div[contains(@class, "last")]')
                        kamar_tidur = bedrooms.text
                        logging.info("The amount of bedrooms in this house was extracted successfully")
                        driver.implicitly_wait(10)
                    except:
                        kamar_tidur = "0"
                        logging.info("There is no data on the number of bedrooms in this house, hence it is replaced with the digit 0.")
                        driver.implicitly_wait(10)

                    # Extracting Amount of Bathrooms
                    try:
                        bathrooms = driver.find_element(By.XPATH, '//div[@data-attr-name = "bathrooms"]//following-sibling::div[contains(@class, "last")]')
                        kamar_mandi = bathrooms.text
                        logging.info("The amount of bathrooms in this house was extracted successfully")
                        driver.implicitly_wait(10)
                    except:
                        kamar_mandi = "0"
                        logging.info("There is no data on the number of bathrooms in this house, hence it is replaced with the digit 0.")
                        driver.implicitly_wait(10)

                    # Extracting Building Size
                    try:
                        building_size = driver.find_element(By.XPATH, '//div[@data-attr-name = "building_size"]//following-sibling::div[contains(@class, "last")]')
                        luas_bangunan = building_size.text
                        logging.info("The building size in this house was extracted successfully")
                        driver.implicitly_wait(10)
                    except:
                        luas_bangunan = "0"
                        logging.info("There is no data on the building size of this house, hence it is replaced with the digit 0.")
                        driver.implicitly_wait(10)

                    # Extracting Land Size
                    try:
                        land_size = driver.find_element(By.XPATH,'//div[@data-attr-name = "land_size"]//following-sibling::div[contains(@class, "last")]')
                        luas_tanah = land_size.text
                        logging.info("The land size in this house was extracted successfully")
                        driver.implicitly_wait(10)
                    except:
                        luas_tanah = "0"
                        logging.info("There is no data on the land size of this house, hence it is replaced with the digit 0.")
                        driver.implicitly_wait(10)

                    # Close Property's Windows
                    driver.close()
                    logging.info("The property's window was closed successfully")
                    driver.implicitly_wait(10)

                    # Switch to City's Windows
                    city_windows = driver.window_handles[2]
                    driver.switch_to.window(city_windows)
                    logging.info("The transition to the city's window was executed successfully.")
                    driver.implicitly_wait(10)

                    file.write(judul + ";" + lokasi + ";" + kamar_tidur + ";" + kamar_mandi + ";" + luas_bangunan + ";" + luas_tanah + ";" + harga + "\n")
                    logging.info("The data has been inserted successfully into the file.")

                try:
                    # Click Next
                    next_button = driver.find_element(By.XPATH, '//div[@class = "next "]')
                    next_button.click()
                    logging.info("The next button was clicked successfully")
                    driver.implicitly_wait(10)
                except:
                    # Close City's Windows
                    logging.info("No page left")
                    driver.implicitly_wait(10)
                    driver.close()
                    logging.info("The city's window was closed successfully")
                    driver.implicitly_wait(10)
                    pagination = False

        # Switch to Province's Windows
        province_window = driver.window_handles[1]
        driver.switch_to.window(province_window)
        logging.info("The transition to the province's window was executed successfully.")
        driver.implicitly_wait(10)

    # Close Province's Windows
    driver.close()
    logging.info("The province's window was closed successfully")
    driver.implicitly_wait(10)

    # Switch to Parent's Windows
    parent_window = driver.window_handles[0]
    driver.switch_to.window(parent_window)
    logging.info("The transition to the province's window was executed successfully.")
    driver.implicitly_wait(10)

file.close()
logging.info("The Scraping Process is Done")

# Close Parent Windows
driver.close()
print("Scraping is Done!!")