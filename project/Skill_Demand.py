# What are the most demanded skills for the top 3 mostpopular data roles?

# Methodoloy
# 1. clean-up skill column
# 2. calculate skill count based on job_title_short
# 3. plot initial findings
# 4. calculate skill percentage
# 5. plot final findings

import pandas as pd
import matplotlib.pyplot as plt
import ast
import seaborn as sns

df = pd.read_csv('../data_jobs.csv') # puts data into dataframe

# Data Cleanup
df['job_posted_date'] = pd.to_datetime(df['job_posted_date'])
df['job_skills'] = df['job_skills'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)


def top_skills_hist():

    df_skills = df[df['job_country'] == 'South Africa'].copy()
    df_skills = df_skills.explode('job_skills')
    skills_count = df_skills.groupby(['job_skills','job_title_short']).size()
    df_skills_count = skills_count.reset_index(name='skill_count')
    df_skills_count.sort_values(by='skill_count',ascending=False, inplace=True)

    job_titles = df_skills['job_title_short'].unique().tolist()[:3] # get top 3 job titles

    fig, ax = plt.subplots(len(job_titles),1) # (rows, columns)

    df_job_title_count = df_skills['job_title_short'].value_counts().reset_index(name='job_total')
    df_skills_perc = pd.merge(df_skills_count, df_job_title_count,on='job_title_short',  how='left')

    df_skills_perc['skill_percent'] = 100 * (df_skills_perc['skill_count'] / df_skills_perc['job_total'])

    sns.set_theme(style='ticks')

    # enumerate - returns an object that supports iteration
    for i, job_title in enumerate(job_titles):
        df_plot = df_skills_perc[df_skills_perc['job_title_short'] == job_title].head(5) # get top 5 skills for each job title in the list (filter)
        sns.barplot(data=df_plot,x='skill_percent', y='job_skills',ax=ax[i],hue='skill_count',palette='dark:b_r')
        ax[i].set_title(job_title)
        ax[i].set_ylabel('') 
        ax[i].set_xlabel('') 
        ax[i].legend().set_visible(False) # remove legend
        ax[i].set_xlim(0, 20) # set all graphs to be on the same axis
        # remove the x-axis tick labels for better readability
        if i != len(job_titles) - 1:
            ax[i].set_xticks([])

        
        # label the percentage on the bars
        for n, v in enumerate(df_plot['skill_percent']):
            ax[i].text(v + 1, n, f'{v:.0f}%', va='center')


    fig.suptitle('Likelihood of skills requested in SA Job Postings', fontsize=15) # set main title
    fig.tight_layout()
    plt.show()


top_skills_hist()
