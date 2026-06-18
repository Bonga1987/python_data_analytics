# How are in-demand skills trending for Data Analysts?

# Methodoloy
# 1. aggregate skill counts monthly
# 2. plot the monthly skill counts
# 3. re-analyze based on the percentage of the total
# 4. plot the monthly skill demand

import pandas as pd
import matplotlib.pyplot as plt
import ast
import seaborn as sns


df = pd.read_csv('../data_jobs.csv') # puts data into dataframe

# Data Cleanup
df['job_posted_date'] = pd.to_datetime(df['job_posted_date'])
df['job_skills'] = df['job_skills'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)


def skills_trend():
    df_DA_SA = df[(df['job_title'] == 'Data Analyst') & (df['job_country'] == 'South Africa')].copy()
    df_DA_SA['job_posted_month_no'] = df_DA_SA['job_posted_date'].dt.month
    df_job_skills = df_DA_SA.explode('job_skills')

    df_skills_pivot = df_job_skills.pivot_table(index='job_posted_month_no', columns='job_skills', aggfunc='size',fill_value=0)

    df_skills_pivot.loc['Total'] = df_skills_pivot.sum()
    df_skills_pivot = df_skills_pivot[df_skills_pivot.loc['Total'].sort_values(ascending=False).index]

    #drop total column
    df_skills_pivot = df_skills_pivot.drop('Total')

    #get totals per month
    df_totals = df_DA_SA.groupby('job_posted_month_no').size()

    df_sa_perc = df_skills_pivot.div(df_totals/100, axis=0)

    # Reset index to make 'job_posted_month' a column again
    df_sa_perc = df_sa_perc.reset_index()

    df_sa_perc['job_posted_month'] = df_sa_perc['job_posted_month_no'].apply(lambda x: pd.to_datetime(x, format='%m').strftime('%b'))
    df_sa_perc = df_sa_perc.set_index('job_posted_month')
    df_sa_perc = df_sa_perc.drop(columns='job_posted_month_no')

    df_plot = df_sa_perc.iloc[:,:5]
    sns.lineplot(df_plot, dashes=False, palette='tab10')
    sns.set_theme(style='ticks')
    sns.despine() # remove vertical line at end of graph

    plt.title('Trending Top Skills for Data Analysts in the SA')
    plt.ylabel('Likelihood in Job Posting')
    plt.xlabel('2023')
    plt.legend().remove()

    from matplotlib.ticker import PercentFormatter
    from adjustText import adjust_text

    ax = plt.gca()
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))

    texts = []
    for i in range(5):
        texts.append(plt.text(11.2, df_plot.iloc[-1, i], df_plot.columns[i]))

    adjust_text(texts, arrowspace=dict(arrowspace='->', color='blue', lw=0.5))
    plt.show()

skills_trend()