import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(
    f"postgresql://postgres:{os.getenv('DB_PASSWORD')}@localhost:5432/churn_db"
)

# Table principale
df = pd.read_sql("SELECT * FROM customers", engine)

# Colonnes calculées utiles pour Power BI
df['tenure_segment'] = pd.cut(df['tenure'],
    bins=[0,12,36,60,100],
    labels=['Nouveau','Intermédiaire','Fidèle','Très fidèle'])

df['value_segment'] = pd.cut(df['monthly_charges'],
    bins=[0,35,65,200],
    labels=['Petit compte','Compte moyen','Grand compte'])

df['churn_label'] = df['churn'].map({True: 'Churner', False: 'Fidèle'})

df['revenue_lost'] = df.apply(
    lambda r: r['monthly_charges'] * 12 if r['churn'] else 0, axis=1)

df.to_csv("D:\\churn-prediction-project\\data\\processed\\powerbi_data.csv", index=False)
print(f"✅ Exporté : {len(df)} lignes")