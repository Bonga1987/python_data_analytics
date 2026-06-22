# What is the most optimal skill to learn for Data Analysts?

# Methodology
# 1. continue from last notbook to find percentage of postings with skill (scatter plot)
# 2. visualize median salary vs percentage skill demand
# 3. determine if certain technologies are more prevalents

import pandas as pd
import matplotlib.pyplot as plt
import ast
import seaborn as sns
from adjustText import adjust_text


df = pd.read_csv('../data_jobs.csv') # puts data into dataframe

# Data Cleanup
df['job_posted_date'] = pd.to_datetime(df['job_posted_date'])
df['job_skills'] = df['job_skills'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)

def extract_technology():
    df_technology = df['job_type_skills'].copy()

    # remove duplicates
    df_technology = df_technology.drop_duplicates()

    # remove NaN values
    df_technology = df_technology. dropna()

    # combine all dictionaries into one
    technology_dict = {}
    for row in df_technology:
        row_dict = ast. literal_eval(row) # convert string to dictionary
        for key, value in row_dict. items():
            if key in technology_dict: # if key already exists in technology_dict, add value to existing value
                technology_dict [key] += value
            else:
                # if key does not exist in technology_dict, add key and value
                technology_dict [key] = value
    # remove duplicates by converting values to set then back to list
    for key, value in technology_dict.items():
        technology_dict [key] = list(set(value))
    
    df_technology = pd.DataFrame(list(technology_dict.items()), columns=['technology', 'skills'])
    df_technology = df_technology.explode('skills')
    return df_technology

def scatter_plot():
    df_DA_SA = df[(df['job_title_short'] == 'Data Analyst') & (df['job_country'] == 'South Africa')].copy()
    df_DA_SA = df_DA_SA.dropna(subset=['salary_year_avg'])
    df_exploded = df_DA_SA.explode('job_skills') 

    df_DA_skills = df_exploded.groupby('job_skills')['salary_year_avg'].agg(['count', 'median']).sort_values(by='count', ascending=False)
    df_DA_skills = df_DA_skills. rename(columns={'count': 'skill_count', 'median': 'median_salary'})
    DA_job_count = len(df_DA_SA)
    df_DA_skills['skill_percent'] = df_DA_skills['skill_count'] / DA_job_count * 100

    skill_percent = 10

    df_DA_skills_high_demand = df_DA_skills[df_DA_skills['skill_percent'] > skill_percent] 

    df_technology = extract_technology()
    df_DA_skills_high_demand = df_DA_skills_high_demand.merge(df_technology, left_on='job_skills', right_on='skills')
    
    # df_DA_skills_high_demand.plot(kind='scatter',x='skill_percent', y='median_salary')
    sns.scatterplot(
        data=df_DA_skills_high_demand,
        x='skill_percent',
        y='median_salary',
        hue='technology'
    )
    sns.set_theme(style='ticks')
    sns.despine()

    texts = []
    for i,txt in enumerate(df_DA_skills_high_demand.index):
        texts.append(plt.text(df_DA_skills_high_demand['skill_percent'].iloc[i],df_DA_skills_high_demand['median_salary'].iloc[i],txt, fontsize=8))

    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='pink', lw=0.5,alpha=0.7), force_text=0.5, force_points=0.3, expand_points=(1.5, 1.5), expand_text=(1.2, 1.2), max_iter=500
                ) # prevents overlap

    plt.xlabel('Count of Job Postings')
    plt.ylabel('Median Yearly Salary')
    plt.title('Most Optimal Skills for Data Analysts in SA')

    from matplotlib.ticker import PercentFormatter
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, pos:f'R{int(y/1000)}K')) # plt.FuncFormatter - formats an axis
    ax.xaxis.set_major_formatter(PercentFormatter(decimals=0)) 

    plt.tight_layout()
    plt.show()

    
scatter_plot() 
