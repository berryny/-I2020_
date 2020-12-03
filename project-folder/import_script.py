from app import db, PreviewDB, WebPagesPreview

jsonLinksList = 'data.json'

# this `main` function should run your scraping when
# this script is ran.
def main():
    db.drop_all()
    # db.session.query(PreviewDB).delete()
    db.create_all()
    wpp = WebPagesPreview(jsonLinksList)
    wpp.createPreviewDB()
    db.session.commit()

if __name__ == '__main__':
    main()
