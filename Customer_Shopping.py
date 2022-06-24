def main():
    params = get_params()
    customers = pd.read_csv(params['customers_location']) 
    products = pd.read_csv(params['products_location'], index_col='product_id') #Making pid as index to fetch cat values
    files = Path(params['transactions_location']).glob("**/*.json") #to read json files in subdirectories as well
    transactions = pd.DataFrame() #To append dataframes of every json file into this
    #Reading All the json file and appending to transactions df
    for file in files:
        data = pd.read_json(file, lines=True)
        transactions = transactions.append(data, ignore_index = True)
    #Looping through c_ids and fetching all the records of that c_id from transactions dataframe and appending to a dictionary key as cust_id and value as Prod_id
    products_purchased_dict = dict()
    for id in customers['customer_id']: 
        rcds = transactions.query(f'customer_id == "{id}"')
        for i in rcds['basket']:
            x = [element['product_id'] for element in i ]
            if id not in products_purchased_dict:
                products_purchased_dict[id] = []
                products_purchased_dict[id].extend(x)
            else:
                products_purchased_dict[id].extend(x)
    #Counting the no. of purchases of each product and dumping it to a outputfile
    with open("output.json", "w") as outfile:
        for cstmr in products_purchased_dict.keys():
            occurence = Counter(products_purchased_dict[cstmr])
            fnl_dict = {'customer_id' : '',}
            for pc in occurence.items():
                if cstmr not in fnl_dict['customer_id']:
                    fnl_dict['customer_id'] = cstmr
                    fnl_dict['loyalty_score'] = int(customers.loc[customers.customer_id == cstmr,'loyalty_score'].values[0])
                    fnl_dict['Purchases'] = []
                    fnl_dict['Purchases'].append({"product_id": pc[0], "product_category" : products['product_category'][pc[0]] ,"purchase_count": pc[1]})
                else:
                    fnl_dict['Purchases'].append({"product_id": pc[0],"product_category" : products['product_category'][pc[0]], "purchase_count": pc[1]})
            json.dump(fnl_dict, outfile)
            outfile.write('\n')