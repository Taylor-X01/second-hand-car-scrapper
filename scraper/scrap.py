import os
import sys
import requests
import datetime
from requests_html import HTML
import pandas as pd

THIS_FILE = os.path.dirname(__file__)

def get_page(url, filename = None, save = False):
    r = requests.get(url)
    if r.status_code == 200:    # 200 : Success return code
        html = r.text     # Get the source code as a string
        if save:        # Save the source code if it's requested {save = True}
            with open(filename,"w") as f:
                f.write(html)
    else:
        print("Page not found !")
        return None
    return html

def run(year_start = None,year_end = None):
    if year_end == None:
        now = datetime.datetime.now()
        year_end = now.year
    if year_start == None:
        year_start = year_end-10

    assert isinstance(year_start,int)
    assert isinstance(year_end, int)



    # url = "https://www.imdb.com/chart/boxoffice/?ref_=nv_ch_cht"
    for year in range(year_start,year_end+1):
        url = f"https://www.boxofficemojo.com/year/world/{year}"

        html_text = get_page(url)

        if html_text == None:
            return None

        r_html = HTML(html = html_text)
        r_table = r_html.find(".imdb-scroll-table")
        # print(r_table)

        if len(r_table) == 0:
            return None

        if len(r_table) == 1:
            table = r_table[0]
            rows = table.find("tr")
            header = rows[0]
            header_col = header.find("th")
            header_names = [x.text for x in header_col]

            table_data = []
            for i , row in enumerate(rows[1:]):
                # print("\n",i," --------------------------------- \n")
                row_data = []
                elmnts = row.find("td")
                # print(elmnts.text)
                for j, elmt in enumerate(elmnts):
                    
                    # if (j == 5) or (j == 0):
                    #     continue
                    # print(elmt.text)
                    row_data.append(elmt.text)

                table_data.append(row_data)

            # print(header_names)
            # print(table_data)
        
        path = os.path.join(THIS_FILE,'data')
        os.makedirs(path,exist_ok=True)
        filepath = os.path.join(path, f"boxOffice {year}.csv")
        filepathX = os.path.join(path, f"boxOfficeX {year}.xlsx")

        df = pd.DataFrame(table_data,columns=header_names)
        df.to_csv(filepath,index=False)
        df.to_excel(filepathX, index=False)
        print(f"Finished {year}")
    print("!! FINISHED !!")





if __name__ == "__main__":
    start , end = sys.argv[1],sys.argv[2]

    try:
        start = int(start)
    except:
        start = None
    try:
        end = int(end)
    except:
        end = None

    if start>end:
        start,end = end,start
        
    print("Start:",start)
    print("End:", end)
    run(start,end)



    # with open("result.txt","w") as f:
    #     f.write(r_table[0].text)
    # print("Results is stored in a txt file!")
    



