import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from threading import Thread

# these are the chosen websites to collecting violines prices 
sazkala_url = "https://sazkala.com/product-category/%D8%B2%D9%87%DB%8C/%D9%88%DB%8C%D9%88%D9%84%D9%86/"
parspiano_url = "https://pianopars.ir/product-category/violin/"

# the prices of the supplier are the values of the our_products dictionary. all the keys are spaceless and lower case, in order to be found easily in the other dictionaries.
our_products={'amati100': 3500000, 'amati150': 5500000, 'amati160': 5800000, 'amati200': 9000000,"muller1421":37500000 ,'amati220': 21000000, 'amatiprofessional': 9000000, 'tf142': 6800000, 'tfstudent': 4000000, 'tf800': 19000000, 'tf132': 5500000, 'tf148': 9000000, 'phoenixvs201': 95000000, 'phoenixvt101': 11000000, 'phoenixvz101': 86000000, 'richardbounelhv-550': 13000000, 'richardbounelrb-2352': 6500000, 'richardbounelrb-101': 5200000, 'renato120': 4000000, 'renato220': 9000000, 'richmanvs800': 30000000}


def clean_text(text):
    text = text.lower()
    text = re.sub(r'ویولن|سایز|مدل|4/4|3/4|2/4|1/4|تومان|\xa0|-|,', '', text)
    text= text.replace("۰","0").replace("۱","1").replace("۲","2").replace("۳","3").replace("۴","4").replace("۵","5").replace("۶","6").replace("۷","7").replace("۸","8").replace("۹","9")
    return text

# sazkala.com crawler function as below:  
def sazkala_crawler(sazkala_url):
    try:
        response = requests.get(sazkala_url)
        # if do not use the code below, we can not see the dataframe in a legible format and we see some symbols only!
        response.encoding = 'utf-8'  
    
        soup = BeautifulSoup(response.text, "html.parser")
        violins = soup.find_all("li", class_="product")
        sazkala_result={}
        for violin in violins:
            name_tag = violin.find("span", class_="woocommerce-loop-product__title")
            name = clean_text(name_tag.text.strip())
            name=name.replace(" ","")
            price_tag = violin.find("span", class_="woocommerce-Price-amount amount")
            price = clean_text(price_tag.text.strip())
            sazkala_result[name]=price
        return pd.DataFrame(list(sazkala_result.items()), columns=["Violin Model", "saz_price"])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data from Pianopars: {e}")
        return pd.DataFrame(columns=["Violin Model", "saz_price"])  # Empty DataFrame on error
saz_df=sazkala_crawler(sazkala_url)


# pianopars.ir crawler function as below:    
def pianopars_crawler(parspiano_url):
    try:
        response = requests.get(parspiano_url)
        soup = BeautifulSoup(response.text, "html.parser")
        violins = soup.find_all("li", class_="product")
        parspiano_result = {}
        for violin in violins:
            name_tag = violin.find("h2", class_="woocommerce-loop-product__title")
            # Check if name_tag exists before accessing text
            if name_tag:
                name = clean_text(name_tag.text.strip())
                name=name.replace("یاماها","yamaha").replace("مبتدی","playwood").replace("اماتی","amati").replace("آماتی","")
                name = re.sub(r"[\u0600-\u06FF]", "", name)
                name=name.replace(" ","")
            # Check if price_tag exists before accessing text
            price_tag = violin.find("span", class_="woocommerce-Price-amount amount")
            if price_tag:
                price = clean_text(price_tag.text.strip())
                parspiano_result[name] = price
        return pd.DataFrame(list(parspiano_result.items()), columns=["Violin Model", "pars_price"])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data from Pianopars: {e}")
        return pd.DataFrame(columns=["Violin Model", "pars_price"])  
pars_df=pianopars_crawler(parspiano_url)
# pars_df

#  concurrence data collecting from 2 websites
def fetch_prices():
    sazkala_thread = Thread(target=sazkala_crawler, args=(sazkala_url,))
    pianopars_thread = Thread(target=pianopars_crawler, args=(parspiano_url,))
    
    sazkala_thread.start()
    pianopars_thread.start()
    
    sazkala_thread.join()
    pianopars_thread.join()

    saz_result = sazkala_crawler(sazkala_url)
    pars_result = pianopars_crawler(parspiano_url)
    
    return saz_result, pars_result

 #  compatitive price calculation for our products
def price_evaluation (our_products):
    saz, pars = fetch_prices()

    # assume the marketing cost is about 500,000 tomans & the shipping cost is about 150,000 for all location in iran. 
    marketing_cost = 1000000
    shipping_cost = 150000
    our_final_prices = {}
    
    for product in our_products:
        # our_products[product] is the price of the supplier, and the base price is the price without any profit
        base_price = our_products[product] + shipping_cost + marketing_cost
        # when the target product is existed in both choosen websites
        if product in pars and product in saz:
            # criteria is the least price of two other websites
            criteria = min(pars[product], saz[product])
            # price_diff: is the difference between the least price and the base price
            price_diff = criteria - base_price
            # final price is obtained from 50% of the price diff and the base price
            final_price = base_price + (price_diff * 0.3)
            #the final price is added to the dictionay which has our products as its keys
            our_final_prices[product] = int(final_price)
        # when the target product is existed in only one of the choosen websites
        elif product in pars:
            price_diff = pars[product] - base_price
            final_price = base_price + (price_diff * 0.3)
            our_final_prices[product] = int(final_price)
        elif product in saz:
            price_diff = saz[product] - base_price
            final_price = base_price + (price_diff * 0.3)
            our_final_prices[product] = int(final_price)
        # when the target product is existed in none of them
        else:
            final_price = base_price + (base_price * 0.24)
            our_final_prices[product] = int(final_price)
    final_df = pd.DataFrame(list(our_final_prices.items()), columns=["Violin Model", "sale_price"])
 
    return final_df


def transaction_evaluation(our_products):
    final_prices = price_evaluation(our_products)
    df_products=pd.DataFrame(list(our_products.items()), columns=["Violin Model", "purchase_price"])
    a = pd.merge(df_products, final_prices, on="Violin Model", how="left")
    b = pd.merge(pars_df, saz_df, on="Violin Model", how="left") 
    merged_df = pd.merge(a, b, on="Violin Model", how="left") 
    merged_df["profit_percent"]=round((((merged_df.sale_price-merged_df.purchase_price)/merged_df.sale_price)*100),2)
    merged_df["profitable_transaction"]= merged_df.profit_percent>=24.00
    return merged_df