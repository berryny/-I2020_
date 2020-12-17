from bs4 import BeautifulSoup
import requests, json, urllib3, os, random, sys, uuid
from urllib.parse import urlparse, urljoin, urlunparse

from app import db, PreviewDB

# json attributes category defining sections and website to scrap for preview layout
jsonLinksList = 'data.json'

class WebPagesPreview(object):
    """docstring for WebPagesPreview."""
    data = ''
    catgData = ''

    def __init__(self, jsonFile):
        self.jsonFile = jsonFile

        f = open (self.jsonFile, "r")
        self.data = json.loads(f.read())
        f.close()
        self.catgData = self.dataJSON()

    def dataJSON(self):
        sortedLinks = sorted(self.data, key=lambda k: k['category'], reverse=False)
        categories = [k['category'] for k in sortedLinks]
        categoryDict = {}
        for c in categories:
            categoriesLst = []
            for l in sortedLinks:
                if c == l['category']:
                    categoriesLst.append(l['website'])
                    categoryDict[c] = categoriesLst
        return categoryDict

    def createPreviewDB(self):
        previewsLst = []
        for catgItems in self.catgData:
            getPreviews = self.dataCategory(catgItems.lower())
            scrapPreviews = self.scrapSite(getPreviews)
            for gsp in scrapPreviews:
                gsp['category'] = catgItems.lower()
                previewsLst.append( gsp )

        if previewsLst:
            for pLst in previewsLst:
                try:
                    newentry = PreviewDB(category=pLst['category'], title=pLst['title'], description=pLst['description'], image=pLst['image'])
                    db.session.add(newentry)
                    db.session.commit()
                except:
                    print("Unexpected error:", sys.exc_info()[0])

    def dataCategory(self, catg):
        self.catg = catg
        self.catItems = self.catgData
        for k,val in self.catItems.items():
            if k.lower() == self.catg:
                return val

    def scrapSite(self,site):
        self.site = site
        siteMeta = []

        for s in set(site):
            # parse the site base url to create image src
            urlInfo = urlparse(s)
            if len(urlInfo.scheme) == 0 or len(urlInfo.netloc) == 0:
                raise RuntimeError('please use complete URL starting with http:// or https://')
            urlBase = urlInfo.scheme + '://' + urlInfo.netloc

            # Check if request was sucessful
            req = requests.get(s)
            if req.status_code == 200:
                soup = BeautifulSoup(req.content, "html.parser")
                dataMeta = {}
                tagTitle = soup.find('title')
                tagBody = soup.find('body')
                if tagTitle:
                    dataMeta['title'] = tagTitle.text

                # Site Meta or Description information
                if soup.find('body'):
                    # tagDescription = tagBody.find('p')
                    tagDescriptionAll = tagBody.find_all('p')
                    tagDescriptionMax = [len(p.text) for p in tagDescriptionAll]
                    if tagDescriptionMax:
                        tagDescriptionSelect = max(enumerate(tagDescriptionMax), key=(lambda x: x[1]))
                        tagDescription = tagDescriptionAll[tagDescriptionSelect[0]]
                    else:
                        tagDescription = None

                    tagMetaDescription = soup.find('meta', attrs={'property' : 'og:description'})

                    if tagDescription:
                        dataMeta['description'] = tagDescription.text
                    elif tagMetaDescription:
                        dataMeta['description'] = tagMetaDescription.text
                    else:
                        dataMeta['description'] = ''

                    tagMetaImage = soup.find('meta', attrs={'property' : 'og:image'})
                    tagRelImage = soup.find('rel', attrs={'property' : 'shortcut icon'})
                    tagImage = tagBody.find('img')

                    if tagImage and 'src' in tagImage.attrs:
                        dataMeta['image'] = urljoin(urlBase, tagImage['src'])
                    elif tagMetaImage is not None and 'content' in tagMetaImage.attrs:
                        dataMeta['image'] = urljoin(urlBase, tagMetaImage['content'])
                    elif tagRelImage is not None and 'href' in tagRelImage.attrs:
                        dataMeta['image'] = urljoin(urlBase, tagRelImage['href'])
                    else:
                        dataMeta['image'] = ''

                siteMeta.append(dataMeta)
        return siteMeta

# this `main` function to scrap a web page 
def main():
    db.drop_all()
    db.create_all()
    wpp = WebPagesPreview(jsonLinksList)
    wpp.createPreviewDB()

if __name__ == '__main__':
    main()
