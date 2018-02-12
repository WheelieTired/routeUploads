from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse
import re


#Load all the relations from the WikiProject page
resp = urllib.request.urlopen('https://wiki.openstreetmap.org/wiki/WikiProject_U.S._Bicycle_Route_System')
soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))

tablecount = 0;
for table in soup.find_all("table"):
    if (tablecount <= 1):
        tablecount += 1;
    else:
        if(tablecount == 2):
            tablecount += 1;
            confirmedRoutes = [];
            afterSymbol = False
            for link in table.find_all('a', href=True):
                if (afterSymbol):
                    afterSymbol = False
                    confirmedRoutes.append(link['href'])
                    print(link['href'])
                else:
                    if (link['href'] == '/wiki/Elements#Relation'):
                        afterSymbol = True;
        else:
            if (tablecount == 3):
                tablecount += 1;
                propsedRoutes = [];
                afterSymbol = False
                for link in table.find_all('a', href=True):
                    if (afterSymbol):
                        afterSymbol = False
                        propsedRoutes.append(link['href'])
                        print(link['href'])
                    else:
                        if (link['href'] == '/wiki/Elements#Relation'):
                            afterSymbol = True;

print(confirmedRoutes)
print(propsedRoutes)

routes = []

for relation in confirmedRoutes:
    url = "http:" + relation
    print(url)
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    subRelations = soup.findAll("li", {"class": "relation"})

    if (subRelations == []):
        rel = re.findall('\d+', link['href'])
        print(rel)
        for route in rel:
            routes.append(route)

    #Get all the subrelation links
    for subRelation in subRelations:
        for link in subRelation.find_all('a', href=True):
            print(link['href'])
            #save the relation numbers
            #rel = link['href']
            rel = re.findall('\d+', link['href'])
            for route in rel:
                routes.append(route)

print(routes)

#Use overpass turbo to convert xml to geojson
for relation in routes:
    payload = "[out:json]; (relation(" + str(relation) + "););out body;>;out skel qt;"
    #data = urllib.parse.urlencode(payload)

    req = urllib.request.Request("https://lz4.overpass-api.de/api/interpreter", payload.encode('utf-8'))
    response = urllib.request.urlopen(req)
    #print(response.read())


    #create a json file for the
    filename = str(relation) + ".geojson"
    file = open(filename, "wb")
    file.write(response.read())
    file.close()
