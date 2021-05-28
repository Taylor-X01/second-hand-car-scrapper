import time
from selenium import webdriver
import requests
from requests_html import HTML
from selenium.webdriver.remote.errorhandler import ErrorCode
from scrap import get_page

browser = webdriver.Chrome(executable_path="C:\\chromedriver\\chromedriver.exe")

context_search = {
    "mark"  :"audi",
    "model" :"q7",
    "city"  :"rabat",
    "year"  :"2017",

}


"""
Google search :

<input class="gLFyf gsfi" jsaction="paste:puy29d;" maxlength="2048" name="q" type="text" 
aria-autocomplete="both" aria-haspopup="false" autocapitalize="off" autocomplete="off" 
autocorrect="off" autofocus="" role="combobox" spellcheck="false" title="Rechercher" value="" 
aria-label="Rech." data-ved="0ahUKEwjApJrcj9vwAhVV4OAKHTlgAxYQ39UDCAQ" wfd-id="61"/>
"""
def search_moteur_ma(browser,context):

    url = "https://www.moteur.ma/fr/voiture/achat-voiture-occasion/"
    browser.get(url)
    time.sleep(0.5)

    ## SEARCH SECTION

    # form = browser.find_element_by_css_selector("form")
    marque = browser.find_element_by_xpath(f"//option[contains(@title,'{context_search['mark']}')]")
    marque.click()
    time.sleep(0.4)

    modele = browser.find_element_by_xpath(f"//option[contains(@title,'{context_search['model']}')]")
    modele.click()
    time.sleep(0.4)

    year = browser.find_element_by_xpath(f"//option[contains(@value,'{context_search['year']}')]")
    year.click()
    time.sleep(0.4)


    # city_check = browser.find_element_by_xpath("//select[contains(@id,'regions_cities')]")
    # city_check.click()
    # time.sleep(0.4)

    city_check = browser.find_element_by_xpath("//option[contains(text(),'Ville')]")
    city_check.click()
    time.sleep(0.4)

    ville = browser.find_element_by_xpath(f"//option[contains(@title,'{context_search['city']}')]")
    ville.click()
    time.sleep(0.4)

    search_btn = browser.find_element_by_xpath("//button[contains(text(),'recherche')]")
    search_btn.click()
    time.sleep(3)

def search_wandaloo(browser,context):
    url = "https://www.wandaloo.com/occasion/"
    browser.get(url)
    ##  time.sleep(1)

    # Get car city
    city_name = context_search['city'].capitalize()
    print("City Name : ",city_name)
    city_el = browser.find_element_by_xpath(
        f"//label[text()=' {city_name} ']/input[@name='ville']")
    city_el.click()
    # time.sleep(0.4)

    # Get car mark
    mark_name = context_search['mark'].upper()
    mark = browser.find_element_by_xpath(f"//label[text()=' {mark_name} ']/input[@name='marque']")
    mark.click()
    # time.sleep(1)

    # Get car model
    model_name = context_search['model'].upper()
    mark = browser.find_element_by_xpath(
        f"//label[text()=' {model_name} ']/input[@name='modele']")
    mark.click()
    # time.sleep(1)


def get_items_links(browser):
    """
    Return a list of URLs from the current web page according to moteur.ma model
    """

    try:
        if "moteur.ma" in browser.current_url:
            items = browser.find_elements_by_xpath("//h3[@class='title_mark_model']/a")
            links = []
            for item in items:
                links.append(item.get_attribute('href'))
            print("Results found : ",len(links))
            print("\n ------------------------------------------- \n")
            print(" ------------------------------------------- \n")
            return links
        elif "wandaloo" in browser.current_url:
            print("You're in Wandaloo.ma")
            items = browser.find_elements_by_xpath(
                "//ul[@class='items']/li/a[@target='_blank'][@class='img']")
            links = []
            for item in items:
                links.append(item.get_attribute('href'))
            return links
    except:
        print("ERROR fetching URLs")
        return None
    
def scrap_pages(browser,links):

    try:
        current_url = browser.current_url
        if "moteur.ma" in current_url:
            for i,url in enumerate(links):
                browser.get(url)
                html_text = get_page(url)

                if html_text == None:
                    return None

                r_html = HTML(html=html_text)
                r_option_table = r_html.find(".box")
                print(f"\nitem {i} ------------------------------------------- \n")
                print(r_option_table[0].text)
                
        elif "wandaloo" in current_url:
            # print("you're in Wandaloo")
            for i,url in enumerate(links):
                browser.get(url)
                html_text = get_page(url)
                if html_text == None:
                    return None

                r_html = HTML(html=html_text)

                ## PARSING HEADER TEXT
                r_details   = r_html.find("div#details",first=True)
                mark_name   = context_search['mark'].upper()
                model_name  = context_search['model'].upper()
                r_header1   = mark_name + " " + model_name
                r_header2   = r_details.find("h4", first=True)
                r_price     = r_details.find("p.prix",first=True)

                ## PARSING VENDOR CONTACT
                r_vendor = r_html.find("div#vendeur",first=True)
                vendor_name = r_vendor.find("p.name", first=True)
                vendor_phonenbr = r_vendor.find("p.mobile", first=True)

                ## PARSING GALLERY IMAGES
                r_gallery = browser.find_elements_by_xpath(
                    "//div[@class='popup-gallery']/ul[@class='items clearfix']/li/a[@class='img']")
                imgs_list = [img.get_attribute('href') for img in r_gallery]

                ## PARSING DESCRIPTION TABLE
                r_option_table = r_html.find("ul.icons")
                item_desc = r_option_table[0].find("li")
                print(f"\nitem {i} ------------------------------------------- \n")
                print("Car pictures list :")
                print(imgs_list)
                print(r_header1,"\n",r_header2.text,"\n","à ",r_price.text,"\n")
                print("Contact vendeur : ")
                print("\t",vendor_name.text)
                print("\t",vendor_phonenbr.text,"\n")
                for line in item_desc:
                    title = line.find("p.titre")
                    tag   = line.find("p.tag")
                    print(title[0].text,"   \t: ",tag[0].text)
    except:
        print("Error parsing car data")
        return None



## Google search related

"""
# url = "https://google.com"
# browser.get(url)

# search_el  = browser.find_element_by_name("q") # find the element that matchs the name 
# search_el1 = browser.find_element_by_css_selector("input")
# print(search_el == search_el1) # True

# search_el1.send_keys("What is a REST API ?") 
"""

"""
Google search : 

Find a way to submit our search text
    Find one of these elements:
        <input type="submit" ... />
        <button type="submit" ... />
Found :

<input class="gNO89b" value="Recherche Google" aria-label="Recherche Google" 
name="btnK" type="submit" data-ved="0ahUKEwjApJrcj9vwAhVV4OAKHTlgAxYQ4dUDCAs" wfd-id="58">



# time.sleep(0.5)
# submit_btn = browser.find_element_by_css_selector('input[type="submit"]')
# submit_btn.click()
"""

try:
    search_wandaloo(browser,context_search)
    print("Base URL : ",browser.current_url)
    links = get_items_links(browser)
    print(links)
    scrap_pages(browser, links)
    time.sleep(1)

    search_moteur_ma(browser, context_search)
    print("Base URL : ", browser.current_url)
    links = get_items_links(browser)
    print(links)
    scrap_pages(browser, links)
    time.sleep(1)
    
    browser.quit()
except:

    print("ERROR")
    browser.quit()


