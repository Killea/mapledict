from bs4 import BeautifulSoup
import os




soup = BeautifulSoup(open( os.path.join(os.path.dirname(__file__),  "temp/dict.html"))  )

print(soup.prettify())


print(soup.find_all('a'))


for link in soup.find_all('a'):
    print(link.get('href'))
for link in soup.find_all('img'):
    print(link.get('src'))