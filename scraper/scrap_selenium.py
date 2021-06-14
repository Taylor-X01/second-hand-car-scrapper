from logging import addLevelName
import os
import time
from selenium import webdriver
import pandas as pd
import requests
from requests_html import HTML
# from selenium.webdriver.remote.errorhandler import ErrorCode
import json
from scraper.scrap import get_page

THIS_FILE = os.path.dirname(__file__)


def getHeadlessDriver():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
    opts = webdriver.ChromeOptions()
    opts.headless = True
    opts.add_argument(f'user-agent={user_agent}')
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument('--ignore-certificate-errors')
    opts.add_argument('--allow-running-insecure-content')
    opts.add_argument("--disable-extensions")
    opts.add_argument("--proxy-server='direct://'")
    opts.add_argument("--proxy-bypass-list=*")
    opts.add_argument("--start-maximized")
    opts.add_argument('--disable-gpu')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path="C:\\chromedriver\\chromedriver.exe",options=opts)
    return driver

browser = getHeadlessDriver()

# context_search = {
#     "mark"  :"dacia",
#     "model" :"logan",
#     "city"  :"rabat",
#     "year"  :"2009",

# }


"""
Google search :

<input class="gLFyf gsfi" jsaction="paste:puy29d;" maxlength="2048" name="q" type="text" 
aria-autocomplete="both" aria-haspopup="false" autocapitalize="off" autocomplete="off" 
autocorrect="off" autofocus="" role="combobox" spellcheck="false" title="Rechercher" value="" 
aria-label="Rech." data-ved="0ahUKEwjApJrcj9vwAhVV4OAKHTlgAxYQ39UDCAQ" wfd-id="61"/>
"""


def search_moteur_ma(browser, context_search):

    url     = "https://www.moteur.ma/fr/voiture/achat-voiture-occasion/"
    browser.get(url)
    time.sleep(0.5)

    ## SEARCH SECTION

    # form = browser.find_element_by_css_selector("form")
    marque  = browser.find_element_by_xpath(f"//option[contains(@value,'{context_search['mark']}')]")
    marque.click()
    time.sleep(1)

    modele  = browser.find_element_by_xpath(f"//option[contains(@value,'{context_search['model']}')]")
    modele.click()
    time.sleep(1)

    year    = browser.find_element_by_xpath(f"//option[contains(@value,'{context_search['year']}')]")
    year.click()
    time.sleep(1)

    # km    = browser.find_element_by_xpath(f"//option[contains(@value,'{context_search['year']}')]")
    # km.click()
    # time.sleep(0.4)


    # city_check = browser.find_element_by_xpath("//select[contains(@id,'regions_cities')]")
    # city_check.click()
    # time.sleep(0.4)

    city_check  = browser.find_element_by_xpath("//option[contains(text(),'Ville')]")
    city_check.click()
    time.sleep(0.4)

    ville       = browser.find_element_by_xpath(f"//option[contains(@value,'{context_search['city']}')]")
    ville.click()
    time.sleep(0.4)

    search_btn  = browser.find_element_by_xpath("//button[contains(text(),'recherche')]")
    search_btn.click()
    time.sleep(3)

def get_pages_moteur(browser):
    pages = browser.find_elements_by_xpath("//div[@id='filter-pager']/div/div/div/ul/li/a")
    if pages != []:
        if len(pages) != 1:
            pages = pages[:-1]
        list =  [url.get_attribute('href') for url in pages]
    else:
        print("Current URL: ",browser.current_url)
        list = [browser.current_url]
    return list
def get_pages_wandaloo(browser):
    try:
        a = browser.find_elements_by_xpath("//ul[@class='pages']/li")
        if len(a)==1:
            list = [browser.current_url]
            return list
        pages = browser.find_elements_by_xpath("//ul[@class='pages']/li/a[@class = 'page']")
        if len(pages) != 1:
            pages = pages[:-1]
        list = [url.get_attribute('href') for url in pages]
        list += [browser.current_url]
        return list
    except:
       list = [browser.current_url]
       return list

def search_wandaloo(browser, context_search):
    url = "https://www.wandaloo.com/occasion/"
    browser.get(url)
    ##  time.sleep(1)

    # Get car city
    try:
        city_name = context_search['city'].capitalize()
        print("City Name : ",city_name)
        city_el = browser.find_element_by_xpath(
            f"//label[text()=' {city_name} ']/input[@name='ville']")
        city_el.click()
    except:
        pass
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
    

def scrap_pages(browser, links, context_search):
    table = []
    try:
        current_url = browser.current_url
        if "moteur.ma" in current_url:
            table1 = []
            header_col1= ["URL","Modele","Option","Prix","Vendeur","Ville","Kilometrage","Annee","Transmission","Carburant","Main","Img"]
            for i,url in enumerate(links):
                browser.get(url)
                html_text = get_page(url)

                if html_text == None:
                    return None
                r_html          = HTML(html=html_text)
                alert           = browser.find_elements_by_xpath("//div[@class='alert alert-warning']")
                # alert = r_html.find(".alert-warning")
                print("ALERT---->",alert)
                
                if alert!=[]:
                    break
                else:
                        row =[]
                        row.append(browser.current_url)
                        model_name1 = browser.find_element_by_xpath("//h1/span[@class='text_bold']")
                        row.append(model_name1.text)
                        row.append('-')
                        try:
                            price1 = browser.find_element_by_xpath("//h1/div")
                            row.append(price1.text.split()[0]+price1.text.split()[1])
                        except:
                            row.append('0')
                        vendor_name = browser.find_element_by_xpath("//div[@class='overview']/div/div/div/div[@class='actions block_tele']/ul/li/a")
                        row.append(vendor_name.text)
                        city_name = browser.find_element_by_xpath("//div[@id='overview']/div[2]/ul[1]/li[5]/a[1]")
                        row.append(city_name.text)
                        title_list = browser.find_elements_by_xpath("//div[@class='box']/div[@class='detail_line']/span[@class='col-md-6 col-xs-6']")
                        tag_list = browser.find_elements_by_xpath( "//div[@class='box']/div[@class='detail_line']/span[@class='text_bold']")
                        print(f"\nitem {i} ------------------------------------------- \n")
                        tag_list_txt = [tag.text for tag in tag_list]
                        title_list_txt = [title.text for title in title_list]
                        
                        print(tag_list_txt)
                        print(title_list_txt)

                try:
                        j = int(title_list_txt.index('Kilométrage'))
                        row.append(tag_list_txt[j].split()[0]+tag_list_txt[j].split()[1])
                except:
                        row.append('-')

                try:
                        j = int(title_list_txt.index('Année'))
                        row.append(tag_list_txt[j])
                except:
                        row.append('-')

                try:
                        j = int(title_list_txt.index('Boite de vitesses'))
                        row.append(tag_list_txt[j])
                except:
                        row.append('-')

                try:
                        j = int(title_list_txt.index('Carburant'))
                        row.append(tag_list_txt[j])
                except:
                        row.append('-')

                try:
                        j = int(title_list_txt.index('Première main'))
                        row.append(tag_list_txt[j])
                except:
                        row.append('-')
                    
                try:
                        img = browser.find_element_by_xpath("//img[@data-u='image']").get_attribute('src')
                        if img == []:
                            img = "/static/img/annonce-sans-photo.jpg"
                            row.append(img)
                        else:
                            print("XOXOXOXOXO : ",img)
                            row.append(img)
                            
                except:
                        img = "/static/img/annonce-sans-photo.jpg"
                        row.append(img)
                table1.append(row)

            if alert==[]:
                print("DATA:",table1)
                return [True,table1,header_col1]
            else:
                print("DATA:", table1)
                return [False,table1,header_col1]
                
        elif "wandaloo" in current_url:
            print("you're in Wandaloo")
            header_col = ["URL","Modele", "option", "Prix", "Vendeur", "Annee", "Ville", "Premiere main", "Kilometrage", "Carburant", "Transmission","Img"]
            for i,url in enumerate(links):
                browser.get(url)
                html_text = get_page(url)
                if html_text == None:
                    return None

                r_html = HTML(html=html_text)

                # GENERATE A LIST DESCRIBING THE ITEM
                item_columns = []
                # FOR EACH ITEM WE PARSE:
                ## PARSING HEADER TEXT {r_header1; r_header2; r_price}
                try:
                    print("\n1.Parsing header text\n")
                    r_details   = r_html.find("div#details",first=True)
                    item_columns.append(browser.current_url)
                    mark_name   = context_search['mark'].upper()
                    model_name  = context_search['model'].upper()
                    r_header1   = mark_name + " " + model_name
                    item_columns.append(r_header1)
                    r_header2   = r_details.find("h4", first=True)
                    item_columns.append(r_header2.text)
                    r_price1     = r_details.find("p.prix",first=True).text
                    r_price = r_price1.split()[0].split('.')[0]+r_price1.split()[0].split('.')[1]
                    if "VENDUE" in r_price1: continue
                    item_columns.append(r_price)
                except:
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    continue

                ## PARSING VENDOR CONTACT  {vendor_name; vendor_phonenbr}
                print("\n2.Parsing vendor contact\n")
                print(r_html.find("div#vendeur-pro", first=True))
                if r_html.find("div#vendeur-pro", first=True) != None:
                    vendor_name = browser.find_element_by_xpath("//p[@class='adress']")
                    item_columns.append(vendor_name.text)
                else:
                    r_vendor        = r_html.find("div#vendeur",first=True)
                    vendor_name     = r_vendor.find("p.name", first=True)
                    vendor_phonenbr = r_vendor.find("p.mobile", first=True)
                    item_columns.append(vendor_name.text)
                    # item_columns.append(vendor_phonenbr.text)

                ## PARSING GALLERY IMAGES {imgs_list}
                print("\n3.Parsing gallery images\n")
                r_gallery = browser.find_elements_by_xpath(
                    "//div[@class='popup-gallery']/ul[@class='items clearfix']/li/a[@class='img']")
                imgs_list = [img.get_attribute('href') for img in r_gallery]

                ## PARSING DESCRIPTION TABLE {[[title, tag], ..., ..., [title_k, tag_k]]}
                print("\n4.Parsing description table\n")
                r_option_table  = r_html.find("ul.icons")
                item_desc       = r_option_table[0].find("li")
                print(f"\nitem {i} ------------------------------------------- \n")
                print("Car pictures list :")
                print(imgs_list)
                print(r_header1,"\n",r_header2.text,"\n","à ",r_price,"\n")
                print("Contact vendeur : ")
                print("\t",vendor_name.text)
                print("\t",vendor_phonenbr.text,"\n")
                for i,line in  enumerate(item_desc):
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    if i==2: continue
                    else:
                        title = line.find("p.titre")
                        tag   = line.find("p.tag")
                        if i==3:
                            if tag[0].text == "Première":
                                item_columns.append('oui')
                            else: 
                                item_columns.append('-')
                        
                        else:
                            item_columns.append(tag[0].text)
                        print(title[0].text,"   \t: ",tag[0].text)
                
                if imgs_list == []:
                    img = "/static/img/annonce-sans-photo.jpg"
                    item_columns.append(img)
                else:    
                    item_columns.append(imgs_list)
                
                ## ADD THIS ITEM TO THE TABLE LIST 
                table.append(item_columns)
        return [table, header_col]
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


def run_scraper(context_search):
    try:

        ### WANDALOO.COM ###

        search_wandaloo(browser,context_search)
        pages_list = get_pages_wandaloo(browser)
        print("Links Pages : ",pages_list)
        data_wandaloo = []
        for page in pages_list:
            browser.get(page)
            print("Base URL : ",browser.current_url)
            links = get_items_links(browser)
            print(links)
            [data_w, header_col] = scrap_pages(browser, links,context_search)
            data_wandaloo += data_w

        # SAVE SEARCH RESULTS IN A CSV FILE
        path = os.path.join(THIS_FILE, 'data')
        os.makedirs(path, exist_ok=True)
        filepath = os.path.join(path, "search_result_wandaloo.csv")
        filepath_json = os.path.join(path, "search_result_wandaloo.json")
        
        # print("\nSaving data in a csv file\n")
        
        df = pd.DataFrame(data_wandaloo,columns=header_col)
        df.to_csv(filepath, index=False)
        df.to_json(filepath_json)

        time.sleep(1)

        ### MOTEUR.MA ###
        print("starting moteur.ma")
        search_moteur_ma(browser, context_search)
        pages_list = get_pages_moteur(browser) # must return links of other search pages
        print("Base URL : ", browser.current_url)
        print("Pages URLs :",pages_list)
        data_moteur =[]
        for page in pages_list:
            print("------>",page)
            browser.get(page)
            links = get_items_links(browser)
            print("Links --->",links)
            [stop, new_data, header_col1] = scrap_pages(browser, links,context_search)
            data_moteur += new_data
            if stop==False: break # Handle out-dated offers
        
         # SAVE SEARCH RESULTS IN A CSV FILE
        path = os.path.join(THIS_FILE, 'data')
        os.makedirs(path, exist_ok=True)
        filepath = os.path.join(path, "search_result_moteur.csv")
        filepath_json = os.path.join(path, "search_result_moteur.json")

        # print("\nSaving data in a csv file\n")

        df = pd.DataFrame(data_moteur,columns=header_col1)
        df.to_csv(filepath, index=False)
        df.to_json(filepath_json)

        time.sleep(1)
        browser.quit()

        # path = os.path.join(THIS_FILE, 'data')
        # os.makedirs(path, exist_ok=True)
        # filepath = os.path.join(path, "search_result_wandaloo.json")
        # filepath1 = os.path.join(path, "search_result_moteur.json")
        # print("PATH:", filepath)
        # with open(filepath, "r") as json_file:
        #     json_str = json_file.read()
        #     # print(json_str)
        #     data_wandaloo = json.loads(json_str)
        # print("DATA ------------------->", data_wandaloo)

        # with open(filepath1, "r") as json_file:
        #     json_str1 = json_file.read()
        #     # print(json_str1)
        #     data_moteur = json.loads(json_str1)

        # print("DATA 2------------------->", data_moteur)
        # browser.close()
        # return [data_wandaloo, data_moteur]


    except:
        print("ERROR")
        browser.quit()
        browser.close()

    
