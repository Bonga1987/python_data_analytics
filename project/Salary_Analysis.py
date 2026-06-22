# How well do jobs and skills pay for Data Analyst?

# Methodology
# 1. evaluate median salary for data jobs
# 2. find median salary per skill for data analysts
# 3. visualize for highest paying skills
# 4. visualize for highest demanded skill  

import pandas as pd
import matplotlib.pyplot as plt
import ast
import seaborn as sns

df = pd.read_csv('../data_jobs.csv') # puts data into dataframe

# Data Cleanup
df['job_posted_date'] = pd.to_datetime(df['job_posted_date'])
df['job_skills'] = df['job_skills'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)


def matploolib_boxplots():
    # job_titles = ['Data Analyst', 'Data Engineer', 'Data Scientist','Senior Data Scientist', 'Senior Data Analyst', 'Senior Data Engineer']
    df_SA = df[df['job_country'] == 'South Africa'].dropna(subset=['salary_year_avg'])
    job_titles = df_SA['job_title_short'].value_counts().index[:6].tolist()
    df_SA_top_6 = df_SA[df_SA['job_title_short'].isin(job_titles)]


    job_order = df_SA_top_6.groupby('job_title_short')['salary_year_avg'].median().sort_values(ascending=False).index

    # job_list = [df_SA[df_SA['job_title_short'] == job_title]['salary_year_avg'] for job_title in job_titles]
    sns.boxplot(data=df_SA_top_6,x='salary_year_avg',y='job_title_short',order=job_order)
    sns.set_theme(style='ticks') 

    plt.title('Salary distribution in South Africa')
    plt.xlabel('Yearly Salary (ZAR)')
    plt.ylabel('')
    plt.xlim(0,900000)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos:f'R{int(x/1000)}K')) # plt.FuncFormatter - formats an axis

    plt.tight_layout()
    plt.show() 

def high_paying_skill():
    
    df_DA_SA = df[(df['job_title_short'] == 'Data Analyst') & (df['job_country'] == 'South Africa')].copy()

    df_DA_SA = df_DA_SA.dropna(subset=['salary_year_avg'])
    df_DA_SA = df_DA_SA.explode('job_skills')

    df_DA_SA[['salary_year_avg','job_skills']]
    df_DA_SA_group = df_DA_SA.groupby('job_skills')['salary_year_avg'].agg(['count','median'])

    df_DA_SA_top_salary = df_DA_SA_group.sort_values(by='median', ascending=False).head(10)
    df_DA_SA_top_skills = df_DA_SA_group.sort_values(by='count', ascending=False).head(10).sort_values(by='median', ascending=False)

    fig,ax = plt.subplots(2,1)

    sns.barplot(data=df_DA_SA_top_salary, x='median', y=df_DA_SA_top_salary.index, ax=ax[0], hue='median', palette='dark:b_r')
    ax[0].set_title('Top 10 highest paid skills for Data Analysts')
    ax[0].set_ylabel('')
    ax[0].set_xlabel('')
    ax[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos:f'R{int(x/1000)}K')) # plt.FuncFormatter - formats an axis
    ax[0].legend().remove()

    # df_DA_US_top_skills[::-1].plot(kind='barh', ax=ax[1], y='median', title='Skills in demand', legend=False)
    sns.barplot(data=df_DA_SA_top_skills, x='median', y=df_DA_SA_top_skills.index, ax=ax[1], hue='median', palette='light:b') # b_r reverse color
    ax[1].set_title('Top 10 most in-demand skills for Data Analysts')
    ax[1].set_xlim(ax[0].get_xlim())
    ax[1].set_ylabel('')
    ax[1].set_xlabel('')
    ax[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos:f'R{int(x/1000)}K')) # plt.FuncFormatter - formats an axis
    ax[1].legend().remove()
    
    fig.tight_layout()
    plt.show()


high_paying_skill()