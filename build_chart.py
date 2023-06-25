import numpy as np
import pandas as pd
df=pd.read_csv('final_data.csv')
def build_chart(main_category,sub_category=None,percentile=0.85):
    df1 = df[df['main_category'] == main_category]
    if sub_category is not None:
        df1 = df1[df1['sub_category'] == sub_category]
        category = sub_category
    else:
        category = main_category
    vote_counts = df1[df1['no_of_ratings'].notnull()]['no_of_ratings'].astype('int')
    vote_averages = df1[df1['ratings'].notnull()]['ratings'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)
    
    qualified = df1[(df1['no_of_ratings'] >= m) & (df1['no_of_ratings'].notnull()) & (df1['ratings'].notnull())][['name', 'main_category', 'sub_category', 'image', 'link', 'ratings','no_of_ratings','discount_price','actual_price']]
    qualified['no_of_ratings'] = qualified['no_of_ratings'].astype('int')
    qualified['ratings'] = qualified['ratings'].astype('float')
    
    qualified['wr'] = qualified.apply(lambda x: (x['no_of_ratings']/(x['no_of_ratings']+m) * x['ratings']) + (m/(m+x['no_of_ratings']) * C), axis=1)
    qualified['wr'] = qualified['wr'].round(2)
    qualified['discount_price'] = qualified['discount_price'].replace({0.0: 'No Discount'})

    qualified = qualified.sort_values('wr', ascending=False).head(10)
    
    return qualified

