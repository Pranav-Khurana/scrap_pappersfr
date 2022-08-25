import pandas as pd
from selenium import webdriver

# Method to get innerHTML
def Inner_Html(value):
    return value.get_attribute('innerHTML')

# Method to remove spaces
def Remove_Spaces(string):
    return string.replace(" ", "")

# Method to Input Company Name/SIREN and generate URL
def Search_String():
    name = input("Please Enter Company Name/SIREN to search for the company:-")
    searchUrl = "https://www.pappers.fr/recherche?q=" + name
    name = Remove_Spaces(name)
    if name.isnumeric() == True and len(name) == 9:
        return True, searchUrl
    else:
        return False, searchUrl

# Method to retrieve all the companies with Similar Name
def Total_Companies(searchUrl):
    driver.get(searchUrl)
    try:
        numberOfCompanies = Inner_Html(
            driver.find_element_by_css_selector('.color-entreprises'))
    except:
        try:
            path = '/html/body/div[1]/div/div[3]/div[1]/div[1]/p[2]'
            numberOfCompanies = Inner_Html(driver.find_element_by_xpath(path))
        except:
            numberOfCompanies = "Data Not Available"
    numberOfCompanies = numberOfCompanies.split('<')[0]
    return numberOfCompanies

# Get details of company having SIREN number
def Get_Data_Siren(searchUrl):
    company = {}
    try:
        company['NAME'] = Inner_Html(
            driver.find_element_by_css_selector('.big-text')).strip()
        company['SIREN'] = Inner_Html(
            driver.find_element_by_css_selector('.siren'))
        otherData = driver.find_elements_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/table/tbody/tr/td')
        company['ADDRESS'] = Inner_Html(otherData[0])
        company['ACTIVITY'] = Inner_Html(otherData[1])
        company['SINCE'] = Inner_Html(otherData[3])
        company['LEGAL FORM'] = Inner_Html(driver.find_element_by_xpath(
            '/html/body/div[1]/div[3]/section[1]/div[2]/table/tbody/tr[3]/td'))
        company['CONTACT'] = Inner_Html(driver.find_element_by_xpath(
            '/html/body/div[1]/div[3]/section[3]/div/table/tbody/tr[1]/td/span')).strip()
        url = company['NAME'].replace(" ","-") + '-' + Remove_Spaces(company['SIREN'])
        company['LINK'] = 'https://www.pappers.fr/entreprise/' + url
    except:
        return False, "Please try again. We are currently facing issue"
    return True, [company]

# Get Details of company without SIREN
def Get_Data():
    allCompanies = []
    try:
        listCompanies = driver.find_elements_by_css_selector('.gros-nom')
    except:
        return False, "Please try again. We are currently facing issue"
    for i in listCompanies:
        company = {}
        company['NAME'] = Inner_Html(i).strip()
        href = i.get_attribute('href')
        company['LINK'] = href
        company['SIREN'] = href.split('-')[-1]
        allCompanies.append(company)
    return True, allCompanies

if __name__ == "__main__":

    # SET UP NETWORK PROXY
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    isSiren, searchUrl = Search_String()
    totalCompanies = Total_Companies(searchUrl)

    if totalCompanies == '0 entreprise':
        print("Incorrect Details. Please make sure to enter correct details.")
    elif not isSiren:
        if totalCompanies == 'Data Not Available':
            print("Please try again. We are currently facing issue")
        else:
            print("Total companies matching your search Criteria are", totalCompanies)
            detailsRetrieved, details = Get_Data() 
            print("Some of the companies which match your search criteria are:-\n")
    else:
        detailsRetrieved, details = Get_Data_Siren(searchUrl)
        print("Details of Company are:-\n")
    if not detailsRetrieved:
        print(details)
    else:
        for company in details:
            for key,value in company.items():
                print(key,':',value)
            print()
    driver.quit()

   # /html/body/div[1]/div/div[3]/div[2]/div[1]
   # div.container-resultat:nth-child(1)

   # RANDOM-LAB.IO
   # <a data-v-0180e8d0="" href="/entreprise/random-holding-908680713" class="gros-nom" style="color: white;" data-x-bergamot-id="0">RANDOM HOLDING</a>
   # html body.body-gris div#app div.page-recherche.body div.min-height-100vh div div.container-resultat div.nom-entreprise a.gros-nom
   # html body.body-gris div#app div.page-recherche.body div.min-height-100vh div div.container-resultat div.nom-entreprise a.gros-nom

   # div.container-resultat:nth-child(1) > div:nth-child(2) > a:nth-child(1)
   # div.container-resultat:nth-child(3) > div:nth-child(2) > a:nth-child(1)

   # /html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/a
   # /html/body/div[1]/div/div[3]/div[2]/div[2]/div[1]/a
   # /html/body/div[1]/div/div[3]/div[2]/div[3]/div[1]/a
   # /html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/a
