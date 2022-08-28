from selenium import webdriver

# Method to get innerHTML
def Inner_Text(value):
    return value.get_attribute('innerText')

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
    totalCompanies = ""
    try:
        numberOfCompanies = Inner_Text(
            driver.find_element_by_css_selector('.color-entreprises'))
    except:
        try:
            path = '/html/body/div[1]/div/div[3]/div[1]/div[1]/p[2]'
            numberOfCompanies = Inner_Text(driver.find_element_by_xpath(path))
        except:
            return "Data Not Available"
    for i in numberOfCompanies.split():
        if i.isnumeric():
            totalCompanies += i
    return totalCompanies

# Get details of company having SIREN number
def Get_Data_Siren(searchUrl):
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
            " ", "-").split('\n')[0] + '-' + Remove_Spaces(company['SIREN'])
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
        company['NAME'] = Inner_Text(i).strip()
        href = i.get_attribute('href')
        company['LINK'] = href
        company['SIREN'] = href.split('-')[-1]
        allCompanies.append(company)
    return True, allCompanies


if __name__ == "__main__":

    # Establish Connection
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    isSiren, searchUrl = Search_String()
    totalCompanies = Total_Companies(searchUrl)

    # Check if input is correct and we are getting any details
    if totalCompanies == '0':
        print("Incorrect Details. Please make sure to enter correct details.")
        driver.quit()
        exit()

    if not isSiren:
        if totalCompanies == 'Data Not Available':
            print("Please try again. We are currently facing issue")
            driver.quit()
            exit()
        else:
            print("Total companies matching your search Criteria are", totalCompanies)
            detailsRetrieved, details = Get_Data()
    else:
        detailsRetrieved, details = Get_Data_Siren(searchUrl)

    if not detailsRetrieved:
        print(details)
    else:
        print("Scrapped data is :- \n")
        for company in details:
            for key, value in company.items():
                print(key, ':', value)
            print()
    driver.quit()
