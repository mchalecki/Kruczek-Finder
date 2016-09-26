# Kruczek Finder
![Kruczek Finder - logo](http://i.imgur.com/kcav5B6.png)
---
## About
---
Kruczek finder is an app that lets You find find loopholes in your contracts, arrangemend, deals and other documents.
It basicly finds "all" potential threats for you. Simple!

Just:
1) Scan a page or take a picture of that document. You can also upload multi-page document from a single pdf file.
2) Type your email and give a check.

And that's all !

After a few minutes you'll receive a email signaling that work is done and you can review it. You will have a link to your document with marked suspicious fragments.
![Kruczek Finder - review](http://i.imgur.com/xpfxO8K.png)

This project was created by TmpTeam during hackathon by [Polish Ministry of Digital Affairs](https://mc.gov.pl/).

#### How does It works?

* [Dane Publiczne API](https://danepubliczne.gov.pl/) is used to search for loopholes. You can select a category and then it checks for every clauses connected (over 8k all of them).
* [Tesseract-ocr](https://github.com/tesseract-ocr/tesseract) is used as a main ocr, to convert image to text.
* Levenshtein algorithm to check text similarity with clauses.

---
# For devs
### Requirements

* python3.4 or above
* python3.4-dev or above
* tesseract-ocr


---
### Running app
Create "secrets.json" file in project base dir (directory where manage.py file is located)
This file must contain "SECRET_KEY", so django project would run. Then run ```manage.py runserver```
