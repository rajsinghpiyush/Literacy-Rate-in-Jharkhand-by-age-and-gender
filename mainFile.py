import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_excel("C:\\Python CA2\\DDW-2000C-08.xlsx")

# print("First 15 rows of raw data:")
# print(df.head(15))

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

# sns.set_style("whitegrid")
plt.figure(figsize=(14, 6))
total_pop = df[(df['Age_group'] == 'All ages')][['District', 'Persons_Total']].sort_values('Persons_Total', ascending=False)
sns.barplot(x='District', y='Persons_Total', data=total_pop)
plt.title('Total Population by District')
plt.ylabel('Population Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
gender_df = df[df['Age_group'] == 'All ages'][['District', 'Males_Total', 'Females_Total']].melt(id_vars='District', var_name='Gender', value_name='Count')
sns.barplot(x='District', y='Count', hue='Gender', data=gender_df)
plt.title('Gender Distribution by District')
plt.ylabel('Population Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
lit_df = df[df['Age_group'] == 'All ages'][['District', 'Persons_Illiterate', 'Persons_Literate']].melt(id_vars='District', var_name='Literacy', value_name='Count')
sns.barplot(x='District', y='Count', hue='Literacy', data=lit_df)
plt.title('Literacy Status by District')
plt.ylabel('Population Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 8))
edu_cols = ['Persons_Below_Primary', 'Persons_Primary', 'Persons_Middle', 
            'Persons_Matric_Secondary', 'Persons_Higher_Secondary',
            'Persons_Graduate']
edu_df = df[df['Age_group'] == 'All ages'][['District'] + edu_cols].melt(id_vars='District', var_name='Education', value_name='Count')
sns.barplot(x='District', y='Count', hue='Education', data=edu_df)
plt.title('Education Level Distribution by District')
plt.ylabel('Population Count')
plt.xticks(rotation=45)
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

plt.figure(figsize=(12, 8))
corr_cols = ['Persons_Total', 'Males_Total', 'Females_Total', 
             'Persons_Illiterate', 'Persons_Literate', 'Persons_Graduate']
sns.heatmap(df[corr_cols].corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix of Key Variables')
plt.tight_layout()
plt.show()
