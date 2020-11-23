# pip install pandas
from bs4 import BeautifulSoup
import re, requests, pandas as pd

# scrapes the following webpage:
scrape_url = 'https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data'

class CovidData:

    # parses the html for the table of covid data
    def __init__(self,url):
        self.url = url
        req = requests.get(self.url)
        self.table_header = []
        self.scrap_covid_data = []

        if req.status_code == 200:
            soup = BeautifulSoup(req.content, "html.parser")
            div = soup.find(id="covid19-container")

            label = div['aria-label']
            table_body = div.findAll('tbody')

            print(label)
            table_soup = BeautifulSoup(str(table_body), "html.parser")
            for tbl_tr in table_soup.find_all('tr'):
                if tbl_tr.attrs.get("class") and ('covid-sticky' in tbl_tr.attrs.get("class")):
                    # regex using python's re module
                    self.table_header = [re.sub(r'\[.*\]\n', '', t.get_text()) for t in tbl_tr.findAll('th')]
                else:
                    tbl_th_arr = []
                    tbl_td_arr = []
                    if len(tbl_tr.findAll('th', {'scope':'row'})):
                        # get the "World" data within the th tags
                        for tbl_th in tbl_tr.findAll('th'):
                            if tbl_th.findAll('img'):
                                country_flag = tbl_th.findAll('img')[0]['src']
                                tbl_th_arr.append(country_flag)
                            else:
                                # regex using python's re module
                                tbl_th_arr.append(re.sub(r'\[.*\]\n', '', tbl_th.get_text()))
                        # grabs the individual country's data in td tags
                        for tbl_td in tbl_tr.findAll('td'):
                            # fills missing values with None
                            if tbl_td.get_text().replace("\n", "") == "No data":
                                tbl_td_arr.append("None")
                            else:
                                tbl_td_arr.append(tbl_td.get_text().replace("\n", ""))
                            
                        # merge the list for each data
                        self.scrap_covid_data.append(tbl_th_arr + tbl_td_arr)

    # Your csv file should contain the following "header" (and corresponding data):
    # country,cases,deaths,recoveries,death_rate,recovery_rate
    def create_csv(self):
        csv_headers = ['Flag'] + self.table_header + ['Death Rate','Recovery Rate']
#         csv_headers = ['Flag'] + self.table_header
        if len(self.scrap_covid_data) > 0 :
            covid_data_rates = []
            for rates in self.scrap_covid_data:
                if rates[2] != 'None' and ''.join(rates[3].split (',')).isnumeric() == True and ''.join(rates[4].split (',')).isnumeric() == True:
                    # regex for commas and periods from int values
                    death_rate = int(re.sub(r',|\.', '',rates[3])) / float(int(re.sub(r',|\.', '',rates[2]))) * 100
                    recovery_rate = int(re.sub(r',|\.', '',rates[4])) / float(int(re.sub(r',|\.', '',rates[2]))) * 100
                    # merge the data list with the calculated rates rounded to the second place
                    covid_data_rates.append(rates + [round(death_rate, 2) , round(recovery_rate)])
                else:
                    covid_data_rates.append(rates + [0 , 0])
            data = pd.DataFrame(covid_data_rates, columns=csv_headers)
            # writes the data in csv format to a file called:{your-name}-covid-report.csv
            data.to_csv('judi-covid-report.csv')
        else:
            print("Error")
            return False
        
cd = CovidData(scrape_url)
cd.create_csv()