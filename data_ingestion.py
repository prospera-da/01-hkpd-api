# %%
import psycopg2
import pandas as pd
from sqlalchemy import text, create_engine
import psycopg2
import pandas as pd

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="hkpd",
    user="postgres",
    password="prospera2023",
)

# %% [markdown]
# ## Akun

# %%
df = pd.read_excel("KMDN 50_5889 2021_Akun dan Program.xlsx")

# %%
# remove incomplete data
df_no_dup = df.dropna(
    subset=["Akun", "Kelompok", "Jenis", "Objek", "Rinc. Objek", "Sub Rinc. Objek"]
).drop_duplicates()

# convert float to int for some columns
df_int_str = df_no_dup.astype({col: int for col in df_no_dup.columns[1:6]})

# convert all columns to be str
df_str = df_int_str.astype(str)

# remove multiple spaces in all columns
df_clean_space = df_str.replace("\s+", " ", regex=True)

# reset index
df_clean_space.reset_index(drop=True, inplace=True)
df_clean_space.index += 1
df_reindexed = df_clean_space.reset_index()

# rename columns
new_columns = {
    "index": "id",
    "Akun": "akun",
    "Kelompok": "kelompok",
    "Jenis": "jenis",
    "Objek": "objek",
    "Rinc. Objek": "rincian_objek",
    "Sub Rinc. Objek": "sub_rincian_objek",
    "Uraian": "uraian",
    "standarsubrinci": "standar_sub_rinci",
}
df_renamed = df_reindexed.rename(columns=new_columns)

# %%
# # create engine
# engine = create_engine('postgresql://postgres:qwe123qwe@34.101.72.155:5432/postgres')
# create engine
engine = create_engine("postgresql://postgres:prospera2023@localhost:5432/hkpd")

# insert to db
df_renamed.to_sql(
    "ground_truth_akun", engine, index=False, if_exists="replace", method="multi"
)

# %%
# add primary key
with engine.connect() as connection:
    connection.execute(text("ALTER TABLE ground_truth_akun ADD PRIMARY KEY (id);"))
