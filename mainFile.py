import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_excel("C:\\Python CA2\\DDW-2000C-08.xlsx")


print(df.head(15))
print(df.describe())
print(df.info())



df.dropna(how='all', inplace=True)
df.dropna(axis=1, how='all', inplace = True)

columns = [
    'Table_Name', 'State_Code', 'Distt_Code', 'Area_Name', 'Total_Rural_Urban',
    'Age_group', 'Persons_Total', 'Males_Total', 'Females_Total',
    'Persons_Illiterate', 'Males_Illiterate', 'Females_Illiterate',
    'Persons_Literate', 'Males_Literate', 'Females_Literate',
    'Persons_Literate_wo_Edu', 'Males_Literate_wo_Edu', 'Females_Literate_wo_Edu',
    'Persons_Below_Primary', 'Males_Below_Primary', 'Females_Below_Primary',
    'Persons_Primary', 'Males_Primary', 'Females_Primary',
    'Persons_Middle', 'Males_Middle', 'Females_Middle',
    'Persons_Matric_Secondary', 'Males_Matric_Secondary', 'Females_Matric_Secondary',
    'Persons_Higher_Secondary', 'Males_Higher_Secondary', 'Females_Higher_Secondary',
    'Persons_NonTech_Diploma', 'Males_NonTech_Diploma', 'Females_NonTech_Diploma',
    'Persons_Tech_Diploma', 'Males_Tech_Diploma', 'Females_Tech_Diploma',
    'Persons_Graduate', 'Males_Graduate', 'Females_Graduate',
    'Persons_Unclassified', 'Males_Unclassified', 'Females_Unclassified'
]

df.columns = columns
# print("Hi",df.head)
# print(df.info())
# print(df.describe())

numeric_cols = df.columns[6:]  
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
print(df['Age_group'])

df.fillna(0, inplace=True)
df = df[(df[numeric_cols] != 0).any(axis=1)]

df['Area_Type'] = df['Area_Name'].apply(lambda x: x.split(' - ')[1] if ' - ' in str(x) else np.nan)
df['District'] = df['Area_Name'].apply(lambda x: x.split(' - ')[-1].replace('District - ', '') if ' - ' in str(x) and str(x) != 'State - JHARKHAND' else np.nan)



plt.figure(figsize=(14, 6))
total_pop = df[df['Age_group'] == 'All ages'].groupby('District')['Persons_Total'].sum().sort_values(ascending=False)
total_pop.plot(kind='bar')
plt.title('Total Population by District')
plt.ylabel('Population Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



gender_df = df[df['Age_group'] == 'All ages'].groupby('District')[['Males_Total', 'Females_Total']].sum()
fig, ax = plt.subplots(figsize=(12, 6))
gender_df.plot(kind='bar', ax=ax)
ax.set_title('Gender Distribution by District')
ax.set_ylabel('Population Count')
ax.set_xlabel('District')
ax.set_xticklabels(gender_df.index, rotation=45)
plt.tight_layout()
plt.show()


lit_df = df[df['Age_group'] == 'All ages'].groupby('District')[['Persons_Illiterate', 'Persons_Literate']].sum()
fig, ax = plt.subplots(figsize=(12, 6))
lit_df.plot(kind='bar', ax=ax)
ax.set_title('Literacy Status by District')
ax.set_ylabel('Population Count')
ax.set_xlabel('District')
ax.set_xticklabels(lit_df.index, rotation=45)
plt.tight_layout()
plt.show()

edu_cols = ['Persons_Below_Primary', 'Persons_Primary', 'Persons_Middle', 
            'Persons_Matric_Secondary', 'Persons_Higher_Secondary', 'Persons_Graduate']
edu_df = df[df['Age_group'] == 'All ages'].groupby('District')[edu_cols].sum()
fig, ax = plt.subplots(figsize=(14, 8))
edu_df.plot(kind='bar', ax=ax)
ax.set_title('Education Level Distribution by District')
ax.set_ylabel('Population Count')
ax.set_xlabel('District')
ax.set_xticklabels(edu_df.index, rotation=45)
plt.tight_layout()
plt.show()

if 'Total_Rural_Urban' in df.columns:
    plt.figure(figsize=(12, 6))
    rural_urban = df[(df['Age_group'] == 'All ages')& 
        (~df['Total_Rural_Urban'].str.contains('Total', case=False, na=False))].groupby('Total_Rural_Urban')['Persons_Total'].sum()
    rural_urban.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Population Distribution: Rural vs Urban')
    plt.ylabel('')
    plt.show()

age_groups = ['7', '8', '9', '10-14', '15-19', '20-24', '25-29', '30-34', '35+']
age_df = df[df['Age_group'].isin(age_groups)]
pivot_edu = age_df.pivot_table(
    index='Age_group',
    values=edu_cols,
    aggfunc='sum'
)
gender_gap_cols = [
    'Males_Literate', 'Females_Literate',
    'Males_Graduate', 'Females_Graduate',
    'Males_Matric_Secondary', 'Females_Matric_Secondary'
]
plt.figure(figsize=(12, 8))
sns.heatmap(df[gender_gap_cols].corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Gender Gap in Education (Correlation)')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
grad_df = df[df['Age_group'] == 'All ages'].groupby('District')['Persons_Graduate'].sum()
grad_df = grad_df.sort_values(ascending=False).head(10)
grad_df.plot(kind='bar')
plt.title('Top Districts by Graduate Population')
plt.ylabel('Graduate Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
age_groups = ['7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69']
line_df = df[(df['Age_group'].isin(age_groups)) & (df['Total_Rural_Urban'] == 'Total')]
line_df['Literacy_Rate_Persons'] = (line_df['Persons_Literate'] / line_df['Persons_Total'] * 100)
line_df['Literacy_Rate_Males'] = (line_df['Males_Literate'] / line_df['Males_Total'] * 100)
line_df['Literacy_Rate_Females'] = (line_df['Females_Literate'] / line_df['Females_Total'] * 100)
line_agg = line_df.groupby('Age_group')[['Literacy_Rate_Males', 'Literacy_Rate_Females']].mean().reindex(age_groups)
plt.plot(line_agg.index, line_agg['Literacy_Rate_Males'], marker='o', label='Males', color='blue')
plt.plot(line_agg.index, line_agg['Literacy_Rate_Females'], marker='o', label='Females', color='red')
plt.title('Literacy Rate by Age Group (Males vs. Females)')
plt.xlabel('Age Group')
plt.ylabel('Literacy Rate (%)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()