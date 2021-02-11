from bs4 import BeautifulSoup
import requests


url= "https://www.screener.in/screens/265380/Good-Solvent-Growth-companies"

def MakeSoup(object):
    soup = BeautifulSoup(object,'lxml')
    return soup

# print(type(html))


# tb = soup.find_all('table')
companies = []

c = 0

def FillNames(url):
    html = requests.get(url).content
    soup = MakeSoup(html)
    input_tag = soup.find_all('tr')
    for a in input_tag:
        company_name = a.get('data-row-company-name')
        if(company_name == None):
            pass    
        else:
            companies.append(company_name)
    global c
    print(c)
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
        print(op)

        try:
            if(len(op) == 3):
                a = op[1].find_all('a')
                NextPage = a[0]['href']
                print(NextPage)
                GoNextPage(NextPage,url)
            else:
                print("ending loop ")
                GoNextPage(0)
        except Exception as e:
            print("Cant find page or pages are ended " + str(e))
        
def GoNextPage(page,*url):
    if(page == 0):
        print("no more values found")
    else:
        FillNames(url[0] + "/" + page)



FillNames(url)
for e in range(len(companies)):
    print(str(e) + " - "  + companies[e])