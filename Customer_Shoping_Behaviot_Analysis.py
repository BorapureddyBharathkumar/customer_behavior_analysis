import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

df = pd.read_csv(r"C:\Users\Bhara\Downloads\customer_shopping_behavior.csv", encoding='latin1')

print(df.info())
print(df.head())

print(df.describe().sum())

print(df.isnull().sum())

df['Review Rating'] =df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))

print(df.isnull().sum())

df.columns = df.columns.str.lower()
df.columns=df.columns.str.replace(' ', '_')
df.columns=df.columns.str.replace('purchase_amount_(usd)', 'purchase_amount')
df.columns=df.columns.str.replace('ï»¿customer_id', 'customer_id')
print(df.isnull().sum())

labels = ['Young Adult','Adult','Middle_aged','Senior']
df['age_group']=pd.qcut(df['age'],q=4, labels = labels)
print(df[['age','age_group']].head(10))


frequency_maping={
'Fortnightly':14,
 'Weekly':7,
 'Annually' :365,
 'Quarterly':90,
 'Bi-Weekly':14,
 'Monthly':30,
 'Every 3 Months':90
}
df['purchase_frequency_days'] =df['frequency_of_purchases'].map(frequency_maping)

print(df[['frequency_of_purchases','purchase_frequency_days']].head(10))


print(df[['discount_applied','promo_code_used']].head(10))

print((df['discount_applied'] == df['promo_code_used']).all())

df = df.drop('promo_code_used',axis=1)

print(df.columns)



from sqlalchemy import create_engine
from urllib.parse import quote_plus

username ="postgres"
password=quote_plus("Bharath@30")
host="localhost"
port="5432"
database="customer_behavior"

engine= create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

table_name = "customer"
df.to_sql(table_name, engine, if_exists='replace',index=False)

print(f"Data successfully loaded into table {table_name} in database {database}")