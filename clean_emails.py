import pandas as pd
import re

df = pd.read_csv("emails_final_final_results_20230329_223541.csv")
df.fillna("", inplace=True)

for index, row in df.iterrows():

    for i in range(1, 21):

        df.loc[index, f"Email {i}"] = re.sub(
            r"\?subject=.*", "", row[f"Email {i}"].lower())


df.to_csv("emails_final_final_final.csv", index=False)
