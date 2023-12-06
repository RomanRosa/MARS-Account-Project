import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import concurrent.futures
from bs4 import BeautifulSoup
import threading
from time import sleep
import pandas as pd

def extract_text_intermedia(url):
    driver = None
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(r"C:\Users\roman\OneDrive - OneWorkplace\Desktop\chromedriver.exe", chrome_options=chrome_options) #cambiar la ruta a donde se encuentre el chromedriver
        driver.get(url)
        element = driver.find_element(By.XPATH, '//img[@src="../imagen/botonimpreso.png"]')
        element.click()
        driver.implicitly_wait(2)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()
        print(f"Successfully extracted text from {url}")
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        text = None
    finally:
        if driver is not None:
            driver.close()
    return text

def parallel_extract_text_intermedia(url):
    return (url, extract_text_intermedia(url))


mars_intermedia = pd.read_excel(r'C:\github_repos\mars_quater_report\project\mars_acumulated_intermedia_21042023.xlsx')
print(mars_intermedia.shape)
mars_intermedia.head()

# Extract Content - Intermedia Data Source
start_time = time.time()

results = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(parallel_extract_text_intermedia, url) for url in mars_intermedia['URL_TESTIGO']]
    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())

elapsed_time = time.time() - start_time
elapsed_mins, elapsed_secs = divmod(elapsed_time, 60)
print(f"Elapsed time: {elapsed_mins:.0f} minutes, {elapsed_secs:.2f} seconds")

mars_intermedia['extracted_content'] = [r[1] for r in results]
print(mars_intermedia.shape)
mars_intermedia.head()