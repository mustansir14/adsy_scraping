import pandas as pd

adsy_df = pd.read_csv("adsy_data.csv")
adsy_df["Website"] = adsy_df["Website"].str.replace(
    "https://", "").str.replace("http://", "").str.replace("www.", "").str.rstrip("/")


emails_final_df = pd.read_csv("emails_final_final_final.csv")
emails_final_df.rename(columns={"Input domain name": "Website"}, inplace=True)

merged = pd.merge(adsy_df, emails_final_df, "left", "Website")

dean_df = pd.read_csv("dean-1482259.csv")

# Group the emails by input domain name
grouped = dean_df.groupby('Input domain name')['Email address'].apply(list)

# Determine the maximum number of emails for any group
max_emails = max([len(emails) for emails in grouped])

# Create a new DataFrame to hold the results
result_df = pd.DataFrame(
    columns=['Input domain name'] + [f'Email {i+1}' for i in range(max_emails)])

# Loop through each group and add the emails to the result DataFrame
for idx, emails in grouped.iteritems():
    row = {'Input domain name': idx}
    for i, email in enumerate(emails):
        row[f'Email {i+1}'] = email
    result_df = result_df.append(row, ignore_index=True)

result_df.rename(columns={"Input domain name": "Website"}, inplace=True)
merged = pd.merge(merged, result_df, "left", "Website")
merged.fillna("", inplace=True)
for index, row in merged.iterrows():
    if row["Email 1_x"]:
        continue

    for i in range(1, 11):
        merged.loc[index, f"Email {i}_x"] = row[f"Email {i}_y"]

merged.to_csv("emails_merged.csv", index=False)
