'''

This short program utilizes the tools of requests and beautiful soup in order to web scrape information from the
products page of Newegg and parses it into a useful CSV data file for analysis.

'''
import re
import secrets
import pymysql
import json
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from os.path  import basename
import csv
import mysql.connector
from mysql.connector.cursor import MySQLCursor

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="food_parse"
)


def get_html(url):
    '''
        Accepts a single URL argument and makes an HTTP GET request to that URL. If nothing goes wrong and
        the content-type of the response is some kind of HTMl/XML, return the raw HTML content for the
        requested page. However, if there were problems with the request, return None.
    '''
    headers = {'Accept-Language': 'en-US,en;q=0.8'}
    try:
        with closing(get(url, headers=headers, stream=True)) as resp:
            if quality_response(resp):
                return resp.content
            else:
                return None
    except RequestException as re:
        print(f"There was an error during requests to {url} : {str(re)}")
        return None

def dbconnect():
    try:
        db = pymysql.connect(
            host='localhost',
            user='root',
            passwd='',
            db='food_parse'
        )
    except Exception as e:
        sys.exit("Can't connect to database")
    return db

def quality_response(resp):
    '''
        Returns true if response seems to be HTML, false otherwise.
    '''
    content_type = resp.headers["Content-Type"].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find("html") > - 1)

def get_products_url_one(url):
    ''' 
        Downloads the webpage, iterates over <div> elements and picks out the brand, product name, product
        price and shipping costs into a list.
    '''

    base_url = "https://www.carrefouruae.com"
    # print(url)
    # url = "https://www.carrefouruae.com/mafuae/en/bio-organic-food/c/F1200000?&qsort=relevance&pg=1"
    response = get_html(url)
    # print(response)

    items_desc = []
    if response is not None:
        soup = BeautifulSoup(response, "html.parser")
        # html = response.read().decode(encoding="iso-8859-1")
        # soup = BeautifulSoup(html, 'html.parser')
        products = soup.find_all("div", {"class": "plp-list__item"})
        for product in products:

            product_url = product.find("a", {"class": "js-gtmProdData"}).get('href')
            items_desc.append(product_url)

            # print(product_url)

        return items_desc
    # else:
    #     return 
    raise Exception(f"There was an error retrieving contents at {url}")

def generate_unique_key(size=15):
    return secrets.token_urlsafe(size)[:size]

# item_name = ''

# calories = 0
# proteins = 0
# carbohydrate = 0
# sugars = 0
# fats = 0

# saturated_fat = 0
# cholesterol = 0
# sodium = 0
# dietary_fiber = 0
# water = 0

# lycopene = 0      
# vitaminA = 0
# vitaminB = 0
# vitaminB1 = 0
# vitaminB2 = 0

# vitaminB3_niacin = 0   
# vitaminB5 = 0
# vitaminB6 = 0
# folic_acid_vitaminB9 = 0
# vitaminC = 0

# vitaminE = 0   
# vitaminK = 0
# iron = 0
# calcium = 0
# magnesium = 0

# phosphorus = 0    
# zinc = 0
# potassium = 0
# polyunsaturated_fatty_acids = 0
# alpha_linolenic_acid_omega = 0

# linoleic_acid_omega = 0    
# monounsaturated_fatty_acids = 0
# oleic_omega_fatty_acid = 0
# trans_fat = 0


def insertDb(item_name, calories, proteins, carbohydrate, sugars, fats, saturated_fat, cholesterol, sodium, dietary_fiber, water, lycopene, vitaminA, vitaminB, vitaminB1, vitaminB2, vitaminB3_niacin, vitaminB5, vitaminB6, folic_acid_vitaminB9, vitaminC, vitaminE, vitaminK, calcium, iron, magnesium, phosphorus, zinc, potassium, polyunsaturated_fatty_acids, alpha_linolenic_acid_omega, linoleic_acid_omega, monounsaturated_fatty_acids, oleic_omega_fatty_acid, trans_fat):
    # try:
    #     with db.cursor() as cursor:
    #         cursor = db.cursor()
    #         print(brandname, itemname, price, packsize, origin, ingredients, allergy, imagenames)
    #         add_item  = ("INSERT INTO foods "
    #                     "(brandname, itemname, price, packsize, origin, allergy) "
    #                     "VALUES (%s, %s, %s, %s, %s, %s,%s,%s)")
    #         data_item = (brandname, itemname, price, packsize, origin, allergy)
    #         print(cursor.execute(add_item,data_item))
    #         db.commit()
    #         cursor.close()
    # except Exception as e:
    #     print (e)

    # try:
    #     with db.cursor() as cursor:
    #         # sql = "INSERT INTO `food_parse` (`item_name`,`calories`,`proteins`,`carbohydrate`,`sugars`,`fats`,`saturated_fat`,`cholesterol`,`sodium`,`dietary_fiber`,`water`,`lycopene`,`vitaminA`,`vitaminB`,`vitaminB1`,`vitaminB2`,`vitaminB3_niacin`,`vitaminB5`,`vitaminB6`,`folic_acid_vitaminB9`,`vitaminC`,`vitaminE`,`vitaminK`,`calcium`,`iron`,`magnesium`,`phosphorus`,`zinc`,`potassium`,`polyunsaturated_fatty_acids`,`alpha_linolenic_acid_omega`,`linoleic_acid_omega`,`monounsaturated_fatty_acids`,`oleic_omega_fatty_acid`,`trans_fat`) VALUES (%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)"
    #         sql = "INSERT INTO `food_parse` (`item_name`,`calories`,`proteins`,`carbohydrate`,`sugars`,`fats`,`saturated_fat`,`cholesterol`,`sodium`,`dietary_fiber`,`water`,`lycopene`,`vitaminA`,`vitaminB`,`vitaminB1`,`vitaminB2`,`vitaminB3_niacin`,`vitaminB5`,`vitaminB6`,`folic_acid_vitaminB9`,`vitaminC`,`vitaminE`,`vitaminK`,`calcium`,`iron`,`magnesium`,`phosphorus`,`zinc`,`potassium`,`polyunsaturated_fatty_acids`,`alpha_linolenic_acid_omega`,`linoleic_acid_omega`,`monounsaturated_fatty_acids`,`oleic_omega_fatty_acid`,`trans_fat`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #         val = (item_name, calories, proteins, carbohydrate, sugars, fats, saturated_fat, cholesterol, sodium, dietary_fiber, water, lycopene, vitaminA, vitaminB, vitaminB1, vitaminB2, vitaminB3_niacin, vitaminB5, vitaminB6, folic_acid_vitaminB9, vitaminC, vitaminE, vitaminK, calcium, iron, magnesium, phosphorus, zinc, potassium, polyunsaturated_fatty_acids, alpha_linolenic_acid_omega, linoleic_acid_omega, monounsaturated_fatty_acids, oleic_omega_fatty_acid, trans_fat)
    #         cursor.execute(sql, val)
    #         db.commit()
    #         cursor.close()
    # except Exception as e:
    #     print ("e=", e)

    cursor = db.cursor()
    sql = "INSERT INTO `food_parse` (`item_name`,`calories`,`proteins`,`carbohydrate`,`sugars`,`fats`,`saturated_fat`,`cholesterol`,`sodium`,`dietary_fiber`,`water`,`lycopene`,`vitaminA`,`vitaminB`,`vitaminB1`,`vitaminB2`,`vitaminB3_niacin`,`vitaminB5`,`vitaminB6`,`folic_acid_vitaminB9`,`vitaminC`,`vitaminE`,`vitaminK`,`calcium`,`iron`,`magnesium`,`phosphorus`,`zinc`,`potassium`,`polyunsaturated_fatty_acids`,`alpha_linolenic_acid_omega`,`linoleic_acid_omega`,`monounsaturated_fatty_acids`,`oleic_omega_fatty_acid`,`trans_fat`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (item_name, calories, proteins, carbohydrate, sugars, fats, saturated_fat, cholesterol, sodium, dietary_fiber, water, lycopene, vitaminA, vitaminB, vitaminB1, vitaminB2, vitaminB3_niacin, vitaminB5, vitaminB6, folic_acid_vitaminB9, vitaminC, vitaminE, vitaminK, calcium, iron, magnesium, phosphorus, zinc, potassium, polyunsaturated_fatty_acids, alpha_linolenic_acid_omega, linoleic_acid_omega, monounsaturated_fatty_acids, oleic_omega_fatty_acid, trans_fat)
    print("val=", val)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()

    # INSERT INTO food_parse(item_name,calories,proteins,carbohydrate,sugars,fats,saturated_fat,cholesterol,sodium,dietary_fiber,water,lycopene,vitaminA,vitaminB,vitaminB1,vitaminB2,vitaminB3_niacin,vitaminB5,vitaminB6,folic_acid_vitaminB9,vitaminC,vitaminE,vitaminK,calcium,iron,magnesium,phosphorus,zinc,potassium,polyunsaturated_fatty_acids,alpha_linolenic_acid_omega,linoleic_acid_omega,monounsaturated_fatty_acids,oleic_omega_fatty_acid,trans_fat)
    # VALUES (item_name, calories, proteins, carbohydrate, sugars, fats, saturated_fat, cholesterol, sodium, dietary_fiber, water, lycopene, vitaminA, vitaminB, vitaminB1, vitaminB2, vitaminB3_niacin, vitaminB5, vitaminB6, folic_acid_vitaminB9, vitaminC, vitaminE, vitaminK, calcium, iron, magnesium, phosphorus, zinc, potassium, polyunsaturated_fatty_acids, alpha_linolenic_acid_omega, linoleic_acid_omega, monounsaturated_fatty_acids, oleic_omega_fatty_acid, trans_fat);


def get_item(url):
    response = get_html(url)
    # print("response=", response)
    items = []
    if response is not None:
        # soup = BeautifulSoup(response, "html.parser")
        html = response.decode(encoding="iso-8859-7")
        soup = BeautifulSoup(html, 'html.parser')
        # soup = BeautifulSoup(open(response, 'r'),"html.parser",from_encoding="iso-8859-1")
        item_name_table = soup.find(id = "main-inner-body-table main-second-inner-table")
        if(item_name_table.find("div", {"class": "column-right"})):
            item_name = item_name_table.find("div", {"class": "column-right"}).h1.text
        else:
            item_name = ''
        print((item_name))
        
        item_table = soup.find('table', {"class": "nv-table"})

        if(item_table.find(id = 'currentValue0')):
            calories = (item_table.find(id = 'currentValue0').text.strip())
        else:
            calories = "0"

        # calories = item_table.find(id = 'currentValue0').text.strip() 

        if(item_table.find(id = 'currentValue1')):
            proteins = (item_table.find(id = 'currentValue1').text.strip())
        else:
            proteins = "0"

        # proteins = item_table.find(id = 'currentValue1').text.strip() 
 
        if(item_table.find(id = 'currentValue2')):
            carbohydrate = (item_table.find(id = 'currentValue2').text.strip())
        else:
            carbohydrate = "0"

        # carbohydrate = item_table.find(id = 'currentValue2').text.strip() 

        if(item_table.find(id = 'currentValue3')):
            sugars = (item_table.find(id = 'currentValue3').text.strip())
        else:
            sugars = "0"

        # sugars = item_table.find(id = 'currentValue3').text.strip() insertDb(item_name, calories, proteins, carbohydrate, )

        if(item_table.find(id = 'currentValue4')):
            fats = (item_table.find(id = 'currentValue4').text.strip())
        else:
            fats = "0"

        # fats = item_table.find(id = 'currentValue4').text.strip()

        if(item_table.find(id = 'currentValue5')):
            saturated_fat = (item_table.find(id = 'currentValue5').text.strip())
        else:
            saturated_fat = "0"

        # saturated_fat = item_table.find(id = 'currentValue5').text.strip()

        if(item_table.find(id = 'currentValue6')):
            trans_fat = (item_table.find(id = 'currentValue6').text.strip())
        else:
            trans_fat = "0"

        # trans_fat = item_table.find(id = 'currentValue6').text.strip()

        if(item_table.find(id = 'currentValue7')):
            cholesterol = (item_table.find(id = 'currentValue7').text.strip())
        else:
            cholesterol = "0"

        # cholesterol = item_table.find(id = 'currentValue7').text.strip()

        if(item_table.find(id = 'currentValue8')):
            sodium = (item_table.find(id = 'currentValue8').text.strip())
        else:
            sodium = "0"

        # sodium = item_table.find(id = 'currentValue8').text.strip()

        if(item_table.find(id = 'currentValue9')):
            dietary_fiber = (item_table.find(id = 'currentValue9').text.strip())
        else:
            dietary_fiber = "0"

        # dietary_fiber = item_table.find(id = 'currentValue9').text.strip()

        if(item_table.find(id = 'currentValue10')):
            water = (item_table.find(id = 'currentValue10').text.strip())
        else:
            water = "0"

        # water = item_table.find(id = 'currentValue10').text.strip()

        if(item_table.find(id = 'currentValue11')):
            lycopene = (item_table.find(id = 'currentValue11').text.strip())
        else:
            lycopene = "0"

        # lycopene = item_table.find(id = 'currentValue11').text.strip()

        if(item_table.find(id = 'currentValue12')):
            vitaminA = (item_table.find(id = 'currentValue12').text.strip())
        else:
            vitaminA = "0"

        # vitaminA = item_table.find(id = 'currentValue12').text.strip()

        if(item_table.find(id = 'currentValue13')):
            vitaminB = (item_table.find(id = 'currentValue13').text.strip())
        else:
            vitaminB = "0"

        # vitaminB = item_table.find(id = 'currentValue13').text.strip()

        if(item_table.find(id = 'currentValue14')):
            vitaminB1 = (item_table.find(id = 'currentValue14').text.strip())
        else:
            vitaminB1 = "0"

        # vitaminB1 = item_table.find(id = 'currentValue14').text.strip()

        if(item_table.find(id = 'currentValue15')):
            vitaminB2 = (item_table.find(id = 'currentValue15').text.strip())
        else:
            vitaminB2 = "0"

        # vitaminB2 = item_table.find(id = 'currentValue15').text.strip()

        if(item_table.find(id = 'currentValue16')):
            vitaminB3_niacin = (item_table.find(id = 'currentValue16').text.strip())
        else:
            vitaminB3_niacin = "0"

        # vitaminB3_niacin = item_table.find(id = 'currentValue16').text.strip()

        if(item_table.find(id = 'currentValue17')):
            vitaminB5 = (item_table.find(id = 'currentValue17').text.strip())
        else:
            vitaminB5 = "0"

        # vitaminB5 = item_table.find(id = 'currentValue17').text.strip()

        if(item_table.find(id = 'currentValue18')):
            vitaminB6 = (item_table.find(id = 'currentValue18').text.strip())
        else:
            vitaminB6 = "0"

        # vitaminB6 = item_table.find(id = 'currentValue18').text.strip()


        if(item_table.find(id = 'currentValue20')):
            folic_acid_vitaminB9 = (item_table.find(id = 'currentValue20').text.strip())
        else:
            folic_acid_vitaminB9 = "0"

        # folic_acid_vitaminB9 = item_table.find(id = 'currentValue20').text.strip()

        if(item_table.find(id = 'currentValue22')):
            vitaminC = (item_table.find(id = 'currentValue22').text.strip())
        else:
            vitaminC = "0"

        # vitaminC = item_table.find(id = 'currentValue22').text.strip()

        if(item_table.find(id = 'currentValue24')):
            vitaminE = (item_table.find(id = 'currentValue24').text.strip())
        else:
            vitaminE = "0"

        # vitaminE = item_table.find(id = 'currentValue24').text.strip()

        if(item_table.find(id = 'currentValue25')):
            vitaminK = (item_table.find(id = 'currentValue25').text.strip())
        else:
            vitaminK = "0"

        # vitaminK = item_table.find(id = 'currentValue25').text.strip()

        if(item_table.find(id = 'currentValue26')):
            calcium = (item_table.find(id = 'currentValue26').text.strip())
        else:
            calcium = "0"

        # calcium = item_table.find(id = 'currentValue26').text.strip()

        if(item_table.find(id = 'currentValue27')):
            iron = (item_table.find(id = 'currentValue27').text.strip())
        else:
            iron = "0"

        # iron = item_table.find(id = 'currentValue27').text.strip()

        if(item_table.find(id = 'currentValue28')):
            magnesium = (item_table.find(id = 'currentValue28').text.strip())
        else:
            magnesium = "0"

        # magnesium = item_table.find(id = 'currentValue28').text.strip()

        if(item_table.find(id = 'currentValue29')):
            phosphorus = (item_table.find(id = 'currentValue29').text.strip())
        else:
            phosphorus = "0"

        # phosphorus = item_table.find(id = 'currentValue29').text.strip()

        if(item_table.find(id = 'currentValue30')):
            zinc = (item_table.find(id = 'currentValue30').text.strip())
        else:
            zinc = "0"

        # zinc = item_table.find(id = 'currentValue30').text.strip()

        if(item_table.find(id = 'currentValue31')):
            potassium = (item_table.find(id = 'currentValue31').text.strip())
        else:
            potassium = "0"

        # potassium = item_table.find(id = 'currentValue31').text.strip()

        if(item_table.find(id = 'currentValue32')):
            polyunsaturated_fatty_acids = (item_table.find(id = 'currentValue32').text.strip())
        else:
            polyunsaturated_fatty_acids = "0"

        # polyunsaturated_fatty_acids = item_table.find(id = 'currentValue32').text.strip()

        if(item_table.find(id = 'currentValue33')):
            alpha_linolenic_acid_omega = (item_table.find(id = 'currentValue33').text.strip())
        else:
            alpha_linolenic_acid_omega = "0"

        # alpha_linolenic_acid_omega = item_table.find(id = 'currentValue33').text.strip()

        if(item_table.find(id = 'currentValue34')):
            linoleic_acid_omega = (item_table.find(id = 'currentValue34').text.strip())
        else:
            linoleic_acid_omega = "0"

        # linoleic_acid_omega = item_table.find(id = 'currentValue34').text.strip()

        if(item_table.find(id = 'currentValue35')):
            monounsaturated_fatty_acids = (item_table.find(id = 'currentValue35').text.strip())
        else:
            monounsaturated_fatty_acids = "0"

        # monounsaturated_fatty_acids = item_table.find(id = 'currentValue35').text.strip()

        if(item_table.find(id = 'currentValue36')):
            oleic_omega_fatty_acid = (item_table.find(id = 'currentValue36').text.strip())
        else:
            oleic_omega_fatty_acid = "0"

        # oleic_omega_fatty_acid = item_table.find(id = 'currentValue36').text.strip()

        # print("trans_fat=", trans_fat, type(trans_fat))
        # print("item_name=", item_name, type(item_name))
        # print("oleic_omega_fatty_acid=", oleic_omega_fatty_acid, type(oleic_omega_fatty_acid))

        insertDb(item_name, calories, proteins, carbohydrate, sugars, fats, saturated_fat, cholesterol, sodium, dietary_fiber, water, lycopene, vitaminA, vitaminB, vitaminB1, vitaminB2, vitaminB3_niacin, vitaminB5, vitaminB6, folic_acid_vitaminB9, vitaminC, vitaminE, vitaminK, calcium, iron, magnesium, phosphorus, zinc, potassium, polyunsaturated_fatty_acids, alpha_linolenic_acid_omega, linoleic_acid_omega, monounsaturated_fatty_acids, oleic_omega_fatty_acid, trans_fat)
        

        # .p.a.text 

        # item_name = item.find("h1", {"class": "productinfo__name"}).text

        # print(item_name)
        # price_init = item.find("h2", {"class": "productinfo__price"}).text 
        # price = " ".join(price_init.split())       

        # print(price)

        # item1 = soup.find("div", {"class": "hidden-sm g-xs-nopad productinfo__header"})
        # if(item1.find(text = re.compile('Pack size\d*'))):
        #     pack_size = item1.find(text = re.compile('Pack size\d*')).split(':')[1]
        # else:
        #     pack_size = ''
        # print(pack_size) 

        # if(len(item1.find_all('span', {"class": "c--flex--wide"})) > 1):
        #     origin = item1.find_all('span', {"class": "c--flex--wide"})[1].find('strong').text
        # else:
        #     origin = ''
        # # origin = item1.find_all('span')
        # # , text = re.compile('Origin:\d*')
        # print(origin)
        # if(soup.find('h3', text = 'Ingredients')):
        #     ingredients = soup.find('h3', text = 'Ingredients').parent.p.text.split(', ')
        # else:
        #     ingredients = []
        # ingredients_json = json.dumps(ingredients)
        # print(ingredients_json)
        # if(soup.find('h3', text = 'Allergy Information')):
        #     allergy = soup.find('h3', text = 'Allergy Information').parent.p.text
        # else:
        #     allergy = ''

        # print(allergy)

        # insertDb(brand_name, item_name, price, pack_size, origin, ingredients_json, allergy, imagenames_json)
        # return True
    else:
        return False
    #     return 
    # raise Exception(f"There was an error retrieving contents at {url}")






        

def read_products():
    ''' 
        Accepts a single item list as an argument, proceses through the list and writes all the products into
        a single CSV data file.
    '''
    headers = "itemurls\n"
    filename = "itemurls.csv"
    itemlll = []
    try: 
        f = open(filename, "r")
        items = f.read()
        itemlll = items.split('\n')
        f.close()

        return itemlll
    except:
        print("There was an error writing to the CSV data file.")
    
if __name__ == "__main__":

    # db = dbconnect()
    # print("Getting list of products and descriptions...")
    # base_url = "https://www.carrefouruae.com"

    # Event Loop to process "events" and get the "values" of the inputs
    item_desc = []
    item_desc = read_products()
    print(len(item_desc))
    idd = 0
    # for item_url in item_desc:
    #     if(len(item_url) > 1):
    #         # if (idd > 9):
    #         #     break
    #         while True:
    #             flag = get_item(base_url + item_url)
    #             if (flag):
    #                 break
    #         idd = idd + 1
    # print(idd)
    kkk = 0
    for item_url in item_desc:
        # if(kkk > 0):
        #     break

        if(len(item_url) > 1):
            print(item_url)
            # if (idd > 9):
            #     break
            flag = get_item(item_url)
        kkk = kkk + 1



    print("...done\n")

    print("Writing product information to a CSV file...")
    # write_products(item_desc)
    print("...done\n")