import pandas as pd
import re
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"postgresql://postgres:{os.getenv('DB_PASSWORD')}@localhost:5432/churn_db"
)

df = pd.read_csv("data/raw/churn_raw.csv")

# Conversion camelCase → snake_case
def to_snake(name):
    s = re.sub(r'([A-Z])', r'_\1', name).lower().strip('_')
    return s.replace(' ', '_')

df.columns = [to_snake(c) for c in df.columns]
df = df.rename(columns={"customer_i_d": "customer_id"})

# Affiche les colonnes pour vérifier
print("Colonnes détectées :", df.columns.tolist())

# Convertir les colonnes booléennes
bool_map = {"Yes": True, "No": False}
for col in ["churn", "partner", "dependents", "phone_service", "paperless_billing"]:
    df[col] = df[col].map(bool_map)

df["total_charges"] = pd.to_numeric(df["total_charges"], errors="coerce")
df = df.dropna(subset=["total_charges"])

df.to_sql("customers", engine, if_exists="append", index=False)
print(f"✅ {len(df)} lignes insérées dans la table customers")