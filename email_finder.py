import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import logging
from threading import Thread, Lock
from queue import Queue
from datetime import datetime
import re
import os


INPUT_FILE_NAME = "emails_final_final.csv"
ALREADY_DONE_FILE = "emails_final_final_results_20230328_035546.csv"
WEBSITE_PAGE_LIMIT = 20
NO_OF_THREADS = 20


logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)
os.environ['WDM_LOG'] = str(logging.NOTSET)


def search_for_emails(driver, emails_found=None):
    if emails_found is None:
        emails_found = []
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    try:
        for text in driver.find_element(By.TAG_NAME, "body").text.split():
            text = text.strip(".,?-/()|")
            if re.search(regex, text) and text not in emails_found:
                emails_found.append(text)
    except:
        pass
    return emails_found


def shuffle_array(array):
    i = 0
    j = len(array) - 1
    new_array = []
    while i <= j:
        new_array.append(array[i])
        if i < j:
            new_array.append(array[j])
        i += 1
        j -= 1
    return new_array


def scrape_url(url, driver, pid, chromedriver_path):

    if type(url) != str:
        logging.error(f"Thread {pid}: Invalid URL: " + str(url))
        return [], driver
    url = url.rstrip("/")
    try:
        domain = url.split("://www.")[1]
    except:
        try:
            domain = url.split("://")[1]
        except:
            try:
                domain = url.split("www.")[1]
                url = "http://" + url
            except:
                domain = url
                url = "https://" + domain

    logging.info(f"Thread {pid}: Searching on " + url)
    try:
        driver.get(url)
    except TimeoutException:
        return [], driver
    except:
        try:
            driver.quit()
        except:
            pass
        driver = get_driver(chromedriver_path)
        return [], driver
    emails_found = search_for_emails(driver)
    if emails_found:
        return emails_found, driver
    links = []
    for link in driver.find_elements(By.TAG_NAME, "a"):
        try:
            href = link.get_attribute("href").rstrip("/").strip()
            if href:
                links.append(href)
        except:
            pass

    links_done = [url.split("://")[1]]
    slash_count = len(url.split("/"))
    links = shuffle_array(links)
    for link in links:
        if link.startswith("mailto:"):
            if link.replace("mailto:", "") not in emails_found:
                emails_found.append(link.replace("mailto:", ""))
        if link[0] == "/":
            link = url + link
        elif "http" not in link:
            continue
        if len(link.split("/")) > slash_count + 1:
            continue
        try:
            link_without_http = link.split("://")[1]
        except:
            continue
        if link_without_http in links_done or domain not in link:
            continue

        logging.info(f"Thread {pid}: Searching on " + link)

        try:
            driver.get(link)
        except TimeoutException:
            continue
        except:
            try:
                driver.quit()
            except:
                pass
            driver = get_driver(chromedriver_path)
            continue
        emails_found = search_for_emails(driver, emails_found)
        if emails_found:
            return emails_found, driver
        links_done.append(link_without_http)
        if len(links_done) == WEBSITE_PAGE_LIMIT:
            break

    return emails_found, driver


def worker(pid, q, lock, output_file, chromedriver_path):

    driver = get_driver(chromedriver_path)
    index = 0
    while q.qsize():
        row = q.get()
        if row["Input domain name"] == "":
            continue
        result_df = pd.DataFrame()
        if row["Email 1"] == "":
            emails, driver = scrape_url(
                row["Input domain name"], driver, pid, chromedriver_path)
            logging.info(
                f"Thread {pid}: Done for " + str(row["Input domain name"]) + ". Total Emails found: " + str(len(emails)))
            if len(emails) == 0:
                emails = [""]
            for i, email in enumerate(emails):
                result_df.loc[0,
                              "Input domain name"] = row["Input domain name"]
                result_df.loc[0, f"Email {i+1}"] = email
        else:
            logging.info(f"Already have email for {row['Input domain name']}")
            result_df.loc[0, "Input domain name"] = row["Input domain name"]
            for i in range(1, 101):
                try:
                    result_df.loc[0, f"Email {i}"] = row[f"Email {i}"]
                except:
                    break

        with lock:
            result_df.to_csv(output_file, index=False,
                             header=False, mode="a")
        index += 1

    driver.quit()


def get_driver(chromedriver_path):

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('ignore-certificate-errors')
    driver = webdriver.Chrome(service=Service(
        chromedriver_path), options=options)
    driver.set_page_load_timeout(30)
    return driver


if __name__ == "__main__":

    if INPUT_FILE_NAME.endswith(".csv"):
        df = pd.read_csv(INPUT_FILE_NAME)
        output_file = INPUT_FILE_NAME.removesuffix(
            ".csv")
    elif INPUT_FILE_NAME.endswith(".xlsx"):
        output_file = INPUT_FILE_NAME.removesuffix(
            ".xlsx")
        df = pd.read_excel(INPUT_FILE_NAME)
    else:
        raise Exception(
            "Invalid Input file. Please enter a file that ends with .csv or .xlsx")
    output_file += "_results_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
    df = df.fillna("")

    # just to create a file with headers
    columns = list(df.columns.copy())
    for i in range(1, 101):
        if f"Email {i}" not in columns:
            columns.append(f"Email {i}")
    start_df = pd.DataFrame(columns=columns)
    start_df.to_csv(output_file, index=False)

    if ALREADY_DONE_FILE:
        already_done_df = pd.read_csv(ALREADY_DONE_FILE)
        already_done_df.to_csv(output_file, index=False,
                               mode="a", header=False)

    no_of_threads = NO_OF_THREADS if len(df) >= NO_OF_THREADS else len(df)
    threads = []
    q = Queue(len(df))
    for row in df.to_dict("records"):
        if not ALREADY_DONE_FILE or row["Input domain name"] not in list(already_done_df["Input domain name"]):
            q.put(row)
    print(q.qsize())
    lock = Lock()
    chromedriver_path = ChromeDriverManager().install()
    for i in range(no_of_threads):
        threads.append(
            Thread(target=worker, args=(i+1, q, lock, output_file, chromedriver_path, )))
        threads[-1].start()
    for thread in threads:
        thread.join()

    # remove duplicates and extra columns
    result_df = pd.read_csv(output_file, low_memory=False)
    result_df.dropna(axis=1, how='all', inplace=True)
    result_df.drop_duplicates(inplace=True)
    result_df.to_csv(output_file, index=False)
