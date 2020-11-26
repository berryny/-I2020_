from flask import Flask, request, redirect, url_for, render_template, session, jsonify
# Use `render_template` to send user to a different page; Redirect 301
# Use `request` to GET or POST from HTML form.
# Use `session` to pass server-side information/request

from flask_assets import Environment, Bundle
# Initialize the app by creating an Environment instance, and registering your assets with it in the form of so called bundles.

from bs4 import BeautifulSoup
import requests, json, urllib3
from urllib.parse import urlparse, urljoin, urlunparse

# Install  Pillow 8.0.1 [https://pypi.org/project/Pillow/] to find time image size (h,w)
# pip install Pillow / py -m pip install Pillow
from PIL import Image
from urllib.request import urlopen

jsonLinksList = 'data.json'

class WebPagesPreview(object):
    """docstring for WebPagesPreview."""
    data = ''
    catgData = ''

    def __init__(self, jsonFile):
        self.jsonFile = jsonFile

    # def openJSON(self):
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
                    # dataDict = {}
                    # dataDict['category'] = l['category']
                    # dataDict['website'] = l['website']
                    categoriesLst.append(l['website'])
                    categoryDict[c] = categoriesLst
        return categoryDict

    def dataCategory(self, catg):
        self.catg = catg
        catItems = self.catgData
        for k,val in catItems.items():
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
                if tagTitle is not None:
                    dataMeta['title'] = tagTitle.text

                # Site Meta information
                tagMetaDescription = soup.find('meta', attrs={'property' : 'og:description'})
                if tagMetaDescription is not None:
                    dataMeta['metadescription'] = tagMetaDescription.text

                tagMetaImage = soup.find('meta', attrs={'property' : 'og:image'})
                if tagMetaImage is not None and 'content' in tagMetaImage.attrs:
                    dataMeta['metaimage'] = urljoin(urlBase, tagMetaImage['content'])

                tagRelImage = soup.find('rel', attrs={'property' : 'shortcut icon'})
                if tagRelImage is not None and 'href' in tagRelImage.attrs:
                    dataMeta['relimage'] = urljoin(urlBase, tagRelImage['href'])

                tagBody = soup.find('body')
                tagDescription = tagBody.find('p')
                if tagDescription is not None:
                    dataMeta['description'] = tagDescription.text

                tagImage = tagBody.find('img')
                # im = []
                # for ig in tagBody.find_all('img'):
                #     # im = Image.open(urljoin(urlBase, ig['src']))
                #     filename = urljoin(urlBase, ig['src'])
                #     req = requests.get(filename)
                #     if req.status_code == 200:
                #         im.append(ig)

                if tagImage is not None and 'src' in tagImage.attrs:
                    dataMeta['image'] = urljoin(urlBase, tagImage['src'])

                siteMeta.append(dataMeta)
        # print('dataMeta',siteMeta)
        return siteMeta

app = Flask(__name__)

bundles = {

    'all_js': Bundle(
        'scripts.js',
        output='gen/all.js'),

    'all_css': Bundle(
        'css/style.css',
        output='gen/all.css'),
}
assets = Environment(app)
assets.register(bundles)

@app.route("/", methods=["GET", "POST"])
@app.route("/index/", methods=["GET", "POST"])
# Define the website pages
def home():
    d = WebPagesPreview(jsonLinksList)
    return render_template("index.html", catgData=d.catgData.keys())

@app.route("/category/<string:categoryItem>")
# Define the category page
def nav(categoryItem):
    l = WebPagesPreview(jsonLinksList)
    catLinks = l.dataCategory(categoryItem.lower())
    sitepreview = l.scrapSite(catLinks)
    print('sitepreview',sitepreview)
    return render_template("category.html", title=categoryItem, sitepreview=sitepreview)

@app.errorhandler(404)
def page_not_found(e):
    # set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)
