from app import db, PreviewDB, WebPagesPreview

# json attributes category defining sections and website to scrap for preview layout
jsonLinksList = 'data.json'

# this `main` function to scrap a web page 
def main():
    db.drop_all()
    db.create_all()
    wpp = WebPagesPreview(jsonLinksList)
    wpp.createPreviewDB()
    db.session.commit()

if __name__ == '__main__':
    main()
