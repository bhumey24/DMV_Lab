import pandas as pd
import matplotlib.pyplot as plt
import re

df = pd.read_excel("company_dataset.xlsx")

df.columns = ['index','Company','Ratings','Review_Count','Type','Years','HQ','Employees']

df['Rating'] = df['Ratings'].astype(str).str.extract(r'(\d+\.\d+)').astype(float)

def convert_reviews(x):
    x = str(x)
    match = re.search(r'(\d+\.?\d*)k', x)
    if match:
        return float(match.group(1)) * 1000
    match = re.search(r'(\d+\.?\d*)', x)
    if match:
        return float(match.group(1))
    return 0

df['Reviews'] = df['Review_Count'].apply(convert_reviews)

df['Year_Num'] = df['Years'].str.extract(r'(\d+)').astype(float)

def convert_employees(x):
    x = str(x)
    if 'Lakh' in x:
        return 100000
    elif '50k' in x:
        return 50000
    elif '10k' in x:
        return 10000
    elif '1k' in x:
        return 1000
    else:
        return 0

df['Emp_Count'] = df['Employees'].apply(convert_employees)

df10 = df.sample(n=10, random_state=42)
df_remaining = df.drop(df10.index)
df5 = df_remaining.sample(n=5, random_state=1)

print("\nHeadquarters of Selected 10 Companies:\n")
print(df10[['Company', 'HQ']])


plt.figure()
plt.bar(df10['Company'], df10['Rating'])
plt.title("Company Rating Comparison (Random 10)")
plt.xlabel("Company")
plt.ylabel("Rating")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

df_sorted = df10.sort_values(by='Reviews', ascending=False)

plt.figure()
plt.barh(df_sorted['Company'], df_sorted['Reviews'])
plt.title("Funnel Chart - Reviews (Random 10)")
plt.xlabel("Reviews")
plt.ylabel("Company")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(df10['Company'], df10['Emp_Count'], marker='o')
plt.title("Employee Count Comparison (Random 10)")
plt.xlabel("Company")
plt.ylabel("Employees")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure()
plt.pie(df5['Year_Num'], labels=df5['Company'], autopct='%1.1f%%')
plt.title("Company Age Distribution (Random 5)")
plt.tight_layout()
plt.show()