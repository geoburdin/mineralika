import bs4
import requests
import  os, shutil

url = 'https://www.minerals.net/MineralMain.aspx'
html = requests.get(url).text
soup = bs4.BeautifulSoup(html, 'html.parser')

minerals_links = []
for link in soup.find_all("a", {"class": "bluelink"}):
    site = 'https://www.minerals.net/' + link.get('href')

    response = requests.get(site)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')


    os.mkdir('./image/'+str(link.get_text()))
    i=0
    for img in images:

        if img.has_attr('src') and img.has_attr('style') and img.has_attr('id') and img.has_attr('alt'):
            if img['src'][0:14] == 'MineralImages/':
                i = i + 1
                big_pic=img['src'].replace('-t.', '.')
                big_pic = big_pic.replace('-thb.', '.')
                images_link = 'https://www.minerals.net/thumbnail.aspx?image='+big_pic+'&size=500'
                print(images_link)
                r = requests.get(images_link, stream=True)
                if r.status_code == 200 and i!=1:  # 200 status code = OK
                    with open('./image/'+str(link.get_text())+'/'+str(i-1)+'.jpg', 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
