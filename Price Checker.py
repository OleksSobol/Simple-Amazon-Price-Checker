from bs4 import BeautifulSoup
import requests
import lxml
import smtplib

URL = "https://www.amazon.com/DJI-Mini-Ultralight-Quadcopter-Transmission/dp/B08JGX61H7?th=1"
TARGET_PRICE = 600.0
headears_data = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/93.0.4577.82 '
                  'Safari/537.36 '
                  'Edg/93.0.961.52',
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(url=URL, headers=headears_data)
response.raise_for_status()
r_text = response.text

soup = BeautifulSoup(r_text, "lxml")
price = float(soup.find(id="priceblock_ourprice").get_text().split("$")[1])
productTitle = soup.find(id="productTitle").get_text().replace("\n", "")[:20]
print(productTitle)
# Sending email about price change
if price <= TARGET_PRICE:
    sender = "sender@example.com"
    sender_pass = "p@ssword"
    receiver = "receiver@example.com"

    msg = f""" From: Price Drop <{sender}>
    \nTo: person <{receiver}>
    \nSubject: Item - {productTitle}

    \nPrice dropped. Current price ${price}. 
    """
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as smtpObj:
            smtpObj.starttls()
            smtpObj.login(user=sender, password=sender_pass)
            smtpObj.sendmail(sender, receiver, msg)
            print(msg)
            print("Email sent")
    except:
        print("Error: unable to send email")
else:
    print(f"Price haven't reach target price ${TARGET_PRICE}")