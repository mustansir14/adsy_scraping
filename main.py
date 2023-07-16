import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import pandas as pd
import random
import os
import logging
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)


def get_element_text(parent, by, value):
    try:
        return parent.find_element(by, value).text
    except:
        return ""


# def get_url(country_id, page):
#     return f"https://cp.adsy.com/marketer/platform/verified-publishers?SiteSearch%5BsitePriceMin%5D=&SiteSearch%5BsitePriceMax%5D=&SiteSearch%5BsiteDaMin%5D=&SiteSearch%5BsiteDaMax%5D=&SiteSearch%5BsiteDrMin%5D=&SiteSearch%5BsiteDrMax%5D=&SiteSearch%5BsiteSpamScoreMin%5D=&SiteSearch%5BsiteSpamScoreMax%5D=&SiteSearch%5BsiteServiceType%5D=&SiteSearch%5Bsite_traffic%5D=&SiteSearch%5Bsite_linktype_id%5D=&SiteSearch%5Bsite_country_id%5D=&SiteSearch%5Bsite_country_id%5D%5B%5D={country_id}&SiteSearch%5Bsite_language_id%5D=&SiteSearch%5BsiteCategory%5D=&SiteSearch%5Bsite_disclosuretype_id%5D=&SiteSearch%5BsiteGoogleNewsSurfacing%5D=&SiteSearch%5BsiteAddedToAdsy%5D=&SiteOptionSearch%5Boption_tat%5D=&SiteOptionSearch%5Brating%5D=&SiteSearch%5Boption_security_deposit%5D=&SiteOptionSearch%5BcompletionRate%5D=7&SiteOptionSearch%5Blifetime_invites_rate%5D=7&SiteOptionSearch%5Breplace_invites_rate%5D=7&per-page=100&SiteSearch%5BsiteWorkedWith%5D=&SiteSearch%5Bpublisher_id%5D=&sort=price_marketer&SiteSearch%5Bsite_url%5D=&page={page}"

# def get_url(traffic_id, page):
#     return f"https://cp.adsy.com/marketer/platform/verified-publishers?SiteSearch%5BsitePriceMin%5D=&SiteSearch%5BsitePriceMax%5D=&SiteSearch%5BsiteDaMin%5D=&SiteSearch%5BsiteDaMax%5D=&SiteSearch%5BsiteDrMin%5D=&SiteSearch%5BsiteDrMax%5D=&SiteSearch%5BsiteSpamScoreMin%5D=&SiteSearch%5BsiteSpamScoreMax%5D=&SiteSearch%5BsiteServiceType%5D=&SiteSearch%5Bsite_traffic%5D=&SiteSearch%5Bsite_traffic%5D%5B%5D={traffic_id}&SiteSearch%5Bsite_linktype_id%5D=&SiteSearch%5Bsite_country_id%5D=&SiteSearch%5Bsite_language_id%5D=&SiteSearch%5BsiteCategory%5D=&SiteSearch%5Bsite_disclosuretype_id%5D=&SiteSearch%5BsiteGoogleNewsSurfacing%5D=&SiteSearch%5BsiteAddedToAdsy%5D=&SiteOptionSearch%5Boption_tat%5D=&SiteOptionSearch%5Brating%5D=&SiteSearch%5Boption_security_deposit%5D=&SiteOptionSearch%5BcompletionRate%5D=7&SiteOptionSearch%5Blifetime_invites_rate%5D=7&SiteOptionSearch%5Breplace_invites_rate%5D=7&per-page=100&SiteSearch%5BsiteWorkedWith%5D=&SiteSearch%5Bpublisher_id%5D=&sort=price_marketer&SiteSearch%5Bsite_url%5D=&page={page}"

# def get_url(tat, page):
#     return f"https://cp.adsy.com/marketer/platform/verified-publishers?SiteSearch%5BsitePriceMin%5D=&SiteSearch%5BsitePriceMax%5D=&SiteSearch%5BsiteDaMin%5D=&SiteSearch%5BsiteDaMax%5D=&SiteSearch%5BsiteDrMin%5D=&SiteSearch%5BsiteDrMax%5D=&SiteSearch%5BsiteSpamScoreMin%5D=&SiteSearch%5BsiteSpamScoreMax%5D=&SiteSearch%5BsiteServiceType%5D=&SiteSearch%5Bsite_traffic%5D=&SiteSearch%5Bsite_linktype_id%5D=&SiteSearch%5Bsite_country_id%5D=&SiteSearch%5Bsite_language_id%5D=&SiteSearch%5BsiteCategory%5D=&SiteSearch%5Bsite_disclosuretype_id%5D=&SiteSearch%5BsiteGoogleNewsSurfacing%5D=&SiteSearch%5BsiteAddedToAdsy%5D=&SiteOptionSearch%5Boption_tat%5D={tat}&SiteOptionSearch%5Brating%5D=&SiteSearch%5Boption_security_deposit%5D=&SiteOptionSearch%5BcompletionRate%5D=7&SiteOptionSearch%5Blifetime_invites_rate%5D=7&SiteOptionSearch%5Breplace_invites_rate%5D=7&per-page=100&SiteSearch%5BsiteWorkedWith%5D=&SiteSearch%5Bpublisher_id%5D=&sort=price_marketer&SiteSearch%5Bsite_url%5D=&page={page}"

def get_url(sorter, page):
    return f"https://cp.adsy.com/marketer/platform/verified-publishers?per-page=100&sort={sorter}&page={page}"


if __name__ == "__main__":

    results_file = "adsy_data.csv"

    if os.path.isfile(results_file):
        urls_done = list(set(list(pd.read_csv(results_file)['Website'])))
    else:
        urls_done = []

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    driver = uc.Chrome(desired_capabilities=caps)

    logging.info("Logging in...")
    # login
    driver.get(get_url("price_creation_long_marketer", 1))
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginform-email"))
    ).send_keys("dean@dinosdigital.com")
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login-pass"))
    ).send_keys("Gdxsw)4m")
    time.sleep(1)
    driver.execute_script("arguments[0].click()", driver.find_element(
        By.XPATH, '//*[@id="w0"]/button'))

    logging.info("Waiting for popup to appear")
    time.sleep(5)
    # close popup if appears
    try:
        close_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="modal_preferred_receiving_notifications"]/div/button'))
        )
        driver.execute_script('arguments[0].click();', close_btn)
        time.sleep(1)
        logging.info("Popup closed")
    except:
        pass

    prev_records_first = ""

    flag = False
    sorters = ["price_creation_long_marketer",
               "-price_marketer", "-price_creation_mini_marketer", "-price_creation_medium_marketer",
               "-price_creation_long_marketer", "site_da", "-site_da", "site_traffic", "-site_traffic",
               "site_dr", "-site_dr", "cr", "-cr", "best"]
    for sorter in sorters:

        for page in range(1, 101):

            logging.info(f"Scraping sorter {sorter} page {page}")
            driver.get(get_url(sorter, page))
            time.sleep(2)
            records = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.ID, 'w0'))
            ).find_elements(By.CLASS_NAME, "table__item")
            time.sleep(2)
            dict_records = []
            if not records or records[0].find_element(By.CLASS_NAME, "link").get_attribute("href") == prev_records_first:
                break
            prev_records_first = records[0].find_element(
                By.CLASS_NAME, "link").get_attribute("href")

            for record in records:
                data = {"Website": record.find_element(
                    By.CLASS_NAME, "link").get_attribute("href")}
                if data['Website'] in urls_done:
                    break
                urls_done.append(data['Website'])
                data["Tags"] = ", ".join([x.text.strip() for x in record.find_elements(
                    By.CLASS_NAME, "badge.badge--category")])
                data["Number of available performers on the site"] = get_element_text(
                    record, By.CLASS_NAME, "badge.badge--options.badge--options__common")

                divs = record.find_element(
                    By.CLASS_NAME, "table__summary.table__summary--inventory-verified").find_elements(By.TAG_NAME, "div")

                for div in divs:
                    try:
                        span = div.find_element(By.TAG_NAME, "span")
                        inner_div = div.find_element(By.TAG_NAME, "div")
                    except:
                        continue
                    data[span.text.strip(' :')] = inner_div.text.strip()

                dict_records.append(data)

            if dict_records:
                df = pd.DataFrame(dict_records)

                if not os.path.isfile(results_file):
                    df.to_csv(results_file, index=False)
                else:
                    df.to_csv(results_file, index=False,
                              header=False, mode='a')
