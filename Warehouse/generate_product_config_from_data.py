import pandas as pd
import yaml

df = pd.read_csv('./data/order_book.csv')

gp = df.groupby(by=['product_id','product_type'])

num_line_dic = {}
volume_dic = {}
for nm,g in gp:
    num_line_dic[nm] = g.shape[0]
    volume_dic[nm] = g['volume'].iloc[0]
    
tot_order = gp.apply(lambda x:x['number_of_order'].sum()).to_dict()

fin_dic = {"products": []}
for p_id in list(df['product_id'].value_counts().keys()):
    curr_dic = {}
    curr_dic["product_id"] = p_id
    for item_type in ['CASE','UNIT']:
        curr_dic[f"number_of_line_for_{item_type.lower()}"] = num_line_dic[(p_id,item_type)]
        curr_dic[f"average_num_demanded_per_line_for_{item_type.lower()}"] = tot_order[(p_id,item_type)] // num_line_dic[(p_id,item_type)]
        curr_dic[f"volume_of_{item_type.lower()}"] = float(volume_dic[(p_id,item_type)])
    fin_dic["products"].append(curr_dic)
    
with open('./configs/product_config.yaml','w') as f:
    yaml.safe_dump(fin_dic,f,sort_keys=False)