from flask import Flask, request, jsonify,render_template,redirect,url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

app = Flask(__name__)
client = MongoClient('mongodb+srv://Doovid:CUInSH79r8SB5RyF@cluster0.ctoe402.mongodb.net/?retryWrites=true&w=majority')
db = client['mydatabase']
purchases = db['purchases']
catalog = db['catalog']

@app.route('/', methods=['GET','POST'])
def Catalog():
    if request.method == 'POST':
        selected_rows = []       
        for item in catalog.find():
            #print(item)
            if request.form.get('product_{}'.format(item['_id'])) == 'on':
                print(item)
                selected_rows.append(item)
        for row in selected_rows:       
            item = row['item']
            price = row['price']
            purchase = {'item':item, 'price':price,'date':datetime.datetime.now()}
            purchases.insert_one(purchase)
    return render_template('index.html',items=catalog.find(),purchased=purchases.find())
    
@app.route('/update_price/<item_id>', methods=['POST','GET'])
def update_price(item_id):
    new_price = request.form['update_price']
    catalog.update_one({'_id': ObjectId(item_id)}, {'$set': {'price': new_price}})
    return redirect(url_for('Catalog'))


@app.route('/insert_product/', methods=['POST'])
def insert_product():
    new_item = {"item":request.form['insert_product_name'],"price":request.form['insert_product_price']}
    catalog.insert_one(new_item)
    return redirect(url_for('Catalog'))

@app.route('/delete_product/', methods=['POST'])
def delete_product():
    delete_rows = []
    for item in catalog.find():
        if request.form.get('product_{}'.format(item['_id'])) == 'on':
            delete_rows.append(item)
    for row in delete_rows:            
        catalog.delete_one({'_id': ObjectId(row['_id'])})
    return redirect(url_for('Catalog'))


@app.route('/purchases/',methods=["GET"])
def getAllBoughtItems():
    show_purchases = []
    for purchase in purchases.find():
        show_purchases.append({'item':purchase['item'],'price':purchase['price'],'date':purchase['date']})
    return jsonify({'purchases':show_purchases})

if __name__ == '__main__':
    app.run(debug=True)
