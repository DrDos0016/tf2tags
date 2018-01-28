#!/usr/bin/python
import json, urllib, codecs
from datetime import datetime
from bs4 import BeautifulSoup

def main():
    # Find out how many results there are
    count = json.loads(urllib.urlopen("http://steamcommunity.com/market/search/render/?query=killstreak&search_descriptions=0&start=0&count=1").read())["total_count"]

    # Load the rest
    start = 0
    show = 50
    names = []
    quantities = []
    prices = []
    links = []
    data = []

    while count > (start + show):
        raw = json.loads(urllib.urlopen("http://steamcommunity.com/market/search/render/?query=killstreak&search_descriptions=0&start="+str(start)+"&count="+str(show)).read())
        if not raw["success"]:
            break
        raw = raw["results_html"]
        soup = BeautifulSoup(raw)
        # Item Name
        items = soup.find_all("span", {"class":"market_listing_item_name"})
        for item in items:
            names.append(item.string)

        # Item Quantity
        items = soup.find_all("span", {"class":"market_listing_num_listings_qty"})
        for item in items:
            quantities.append(item.string)

        # Item Prices
        #items = soup.find_all("div", {"class":"market_listing_right_cell"})
        items = soup.find_all("div", {"class":"market_listing_their_price"})
        for item in items[1:]: # There's one in the header that says QUANTITY, skip it.
            temp = str(item.span)
            temp = temp[temp.rfind("<br/>")+32:-15].strip()
            prices.append(temp)

        # Links
        raw_links = soup.find_all("a")
        for link in raw_links:
            links.append(link.get("href"))

        start += show

    if not (len(quantities) == len(names) and len(prices) == len(links) and len(names) == len(prices)):
        meta = {"success":0, "message":"Count mismatch! Quantity/Names/Prices/Links = {}/{}/{}/{}".format(len(quantities), len(names), len(prices), len(links)), "time":str(datetime.now())}
    else:
        meta = {"success":1, "count":len(names), "time":str(datetime.now())}
        for x in xrange(0, len(names)):
            data.append({"name":names[x], "quantity":quantities[x], "price":prices[x], "link":links[x]})

    results = {"meta":meta, "data":data}

    text = json.dumps(results)
    fh = codecs.open("/var/projects/tf2tags//assets/data/streak_search.json", encoding='utf-8', mode='w')
    fh.write(text)
    fh.close()

if __name__ == "__main__": main()
