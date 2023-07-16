import pandas as pd

master_df = pd.read_csv("master_list.csv")
master_df["Website"] = master_df["Website"].str.replace(
    "https://", "").str.replace("http://", "").str.replace("www.", "").str.rstrip("/")
aqib_df = pd.read_csv("aqib_list.csv")


merged_df = pd.merge(master_df, aqib_df, "outer", "Website")
merged_df.fillna("", inplace=True)
for index, row in merged_df.iterrows():
    if row["Email 1_x"] == "":
        merged_df.loc[index, "Email 1_x"] = row["Email 1_y"]
    if row["Tags_x"] == "":
        merged_df.loc[index, "Tags_x"] = row["Tags_y"]


merged_df.to_csv("merged_df_final.csv", index=False)
