from django.shortcuts import render
from .models import Search, Results
from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen
from requests.utils import requote_uri as requote
from statistics import mean,mode

raw_url='https://www.jumia.com.ng/catalog/?q={}'
# Create your views here.


def home(requests):
    return render(requests, 'base.html')

def search(requests):
    search_text=requests.POST.get('search')
    Search.objects.create(search_text=search_text)
    final_url=raw_url.format(requote(search_text))
    req_url=Request(final_url, headers={'user-agent':'XYZ-3.0'})
    open_url= urlopen(req_url,timeout=30).read()
    soup=BS(open_url,'html.parser')


    product_container= soup.find_all('a',{'class':'core'})

    product_total=[]
    price_list=[]

    for container in product_container:

        product_name_raw = container.find('h3', {'class': 'name'})
        product_price_raw = container.find('div', {'class': 'prc'})
        product_image_raw = container.find('img',{'class':'img'}).get('data-src')



        if len(product_name_raw.text)>1 and len(product_price_raw.text)>1:
            price=product_price_raw.text.split(' ')
            price=price[1].split(',')
            price_raw=price[0]+price[1]
            price=int(price_raw)
            price_list.append(price)

            product_link_raw = 'https://jumia.com.ng{}'.format(container.get('href'))



            product_total.append((product_name_raw.text, product_price_raw.text,product_image_raw,product_link_raw))

    # print(sorted(price_list)[-5:])

    print(mode(price_list))
    print(mean(price_list))

    context={'search_text':search_text,

             'product_total':product_total
             }
    return render(requests, 'scrapper/search.html',context)