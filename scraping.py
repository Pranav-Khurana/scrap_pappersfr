from selenium import webdriver

# Method to get innerHTML
def Inner_Text(value):
    return value.get_attribute('innerText')

# Method to remove spaces
def Remove_Spaces(string):
    return string.replace(" ", "")

# Method to generate URL
def Generate_Search_Url(name):
    searchUrl = "https://www.pappers.fr/recherche?q=" + name
    name = Remove_Spaces(name)
    if name.isnumeric() == True and len(name) == 9:
        return True, searchUrl
    else:
        return False, searchUrl

# Get details of company 
def Get_Data(searchUrl):
    driver.get(searchUrl)
    company = {}
    try:
        company['NAME'] = Inner_Text(
            driver.find_element_by_css_selector('.big-text')).strip()
        company['SIREN'] = Inner_Text(
            driver.find_element_by_css_selector('.siren'))
        otherData = driver.find_elements_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/table/tbody/tr/td')
        company['ADDRESS'] = Inner_Text(otherData[0])
        company['ACTIVITY'] = Inner_Text(otherData[1])
        company['SINCE'] = Inner_Text(otherData[3])
        company['LEGAL FORM'] = Inner_Text(driver.find_element_by_xpath(
            '/html/body/div[1]/div[3]/section[1]/div[2]/table/tbody/tr[3]/td'))
        company['CONTACT'] = Inner_Text(driver.find_element_by_xpath(
            '/html/body/div[1]/div[3]/section[3]/div/table/tbody/tr[1]/td/span')).strip()
        url = company['NAME'].replace(
            " ", "-") + '-' + Remove_Spaces(company['SIREN'])
        company['LINK'] = 'https://www.pappers.fr/entreprise/' + url
    except:
        return False, "Please try again. We are currently facing issue"
    return True, company

# Get list of companies matching search criteria
def Get_Company_List(searchUrl):
    companies = {}
    try:
        driver.get(searchUrl)
        listCompanies = driver.find_elements_by_css_selector('.gros-nom')
    except:
        return False, "Please try again. We are currently facing issue"
    for i in listCompanies:
        name = Inner_Text(i).strip()
        href = i.get_attribute('href')
        companies[name] = href
    return True, companies


if __name__ == "__main__":

    # Establish Connection
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    # Input the Search String and Call Generate_Search_Url to get the search url
    companyName = input(
        "Please Enter Company/SIREN Name to search for the company:-").upper()
    isSiren, searchUrl = Generate_Search_Url(companyName)

    # Check if the exact company is retrieved otherwise check for company in generated list
    if not isSiren:
        detailsRetrieved, allCompanies = Get_Company_List(searchUrl)
        if not detailsRetrieved:
            print(allCompanies)
            driver.quit()
            exit()
        print(allCompanies.keys())
        if companyName in allCompanies.keys():
            searchDone, companyDetails = Get_Data(
                allCompanies[companyName])
        else:
            searchDone, companyDetails = False, "Not able to find Company. Please try to search with SIREN"
    else:
        searchDone, companyDetails = Get_Data(searchUrl)

    if not searchDone:
        print(companyDetails)
    else:
        print("Details of Company are:-\n")
        for key, value in companyDetails.items():
            print(key, ':', value)
        print()

    driver.quit()
