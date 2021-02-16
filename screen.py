from bs4 import BeautifulSoup
import requests



def MakeSoup(object):
    soup = BeautifulSoup(object,'lxml')
    return soup

print("Processing....")


# tb = soup.find_all('table')
companies = []
urls = []
main= []
full_company = []
url = input("Enter screener url: ")

# url= "https://www.screener.in/screens/265380/Good-Solvent-Growth-companies"
# url= "https://www.screener.in/screens/282622/Solvency-Screen/"
# url= "https://www.screener.in/screens/178/Growth-Stocks/"
# url= "https://www.screener.in/screens/59/Magic-Formula/"
c = 0
# z= 0

def Fill_data(url):
    FillNames(url)
    try:
        for e in urls:
            html = requests.get("https://www.screener.in" + e).content
            soup = MakeSoup(html)
            top = soup.findChild("div",{"id":"top"})
            # print(top)
            top_div = MakeSoup(str(top))
            top_div_str = top_div.find_all("div",{'class': 'flex-row'})
            top_h1 = MakeSoup(str(top_div_str))
            ful_com = top_h1.find("h1",{'class':'margin-0'}).text
            # print(ful_com)
            full_company.append(ful_com)

    except Exception as e:
        print(e)
    main.append(companies)
    main.append(urls)
    main.append(full_company)
    # print(full_company)
    # print("len of full company: " + str(len(full_company)))
    # print("len of company: "+ str(len(companies)))
    # print("len of urls: " + str(len(urls)) )
    
    print("Got all the names from screener")

    return main

def GoNextPage(page,*url):
    if(page == 0):
        pass
    else:
        # print(url[0] + "/" + page)
        FillNames(url[0] + "/" + page)



def FillNames(url):
    html = requests.get(url).content
    soup = MakeSoup(html)
    input_tag = soup.find_all('tr')
    for a in input_tag:
        company_name = a.get('data-row-company-name')
        tr_soup = MakeSoup(str(a))
        # print(tr_soup)
        company_url  = tr_soup.find('a').get('href')
        com = str(company_url).strip('/')
        com = com.split('/')[0]
        # print(com)
        if(com == "company"):
            urls.append(company_url)
        else:
            pass
        if(company_name == None):
            pass    
        else:
            companies.append(company_name)
    global c
    # print(c)
    if(c == 0):

        op = soup.find('div',{'class': 'options'})
        # print(bytes(op))

        try:
            a = op.find_all('a')
            NextPage = a[0]['href']
            # FillNames(url+NextPage)
            # return NextPage
            c+=1
            GoNextPage(NextPage,url)
        except Exception as e:
            print("Cant find page or pages are ended " + str(e))
            GoNextPage(0)

            # return 0
        
    else:
        op = soup.find_all('div',{'class': 'options'})
        # print(op)

        try:
            if(len(op) == 3):
                a = op[1].find_all('a')
                NextPage = a[0]['href']
                # print(NextPage)
                url = url.split("?")
                url = url[0]
                url = url[:-1]
                GoNextPage(NextPage,url)
            else:
                # print("ending loop ")
                GoNextPage(0)
        except Exception as e:
            print("Cant find page or pages are ended " + str(e))
def GatherData():
    d = Fill_data(url)
    return d

# d = FillNames(url)
# print(len(d[0]))
# print(len(d[1]))

# for e in range(len(companies)):
#     print(str(e+1) + " - "  + companies[e])

