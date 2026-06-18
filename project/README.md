## Overview

Welcome to my analysis of the data job market, focusing on data analyst roles. This project was created out of a desire to navigate and understand the job market more effectively. It delves into the top-paying and in-demand skills to help find optimal job opportunities for data analysts.

The data sourced from [Luke Barousse's Python Course](https://www.lukebarousse.com/) which provides a foundation for my analysis, containing detailed information on job titles, salaries, locations, and essential skills. Through a series of Python scripts, I explore key questions such as the most demanded skills, salary trends, and the intersection of demand and salary in data analytics.

---

## The Questions

Below are the questions I want to answer in my project:

1. What are the skills most in demand for the top 3 most popular data roles?
2. How are in-demand skills trending for Data Analysts?
3. How well do jobs and skills pay for Data Analysts?
4. What are the optimal skills for data analysts to learn? (High Demand AND High Paying)

# Tools I Used

For my deep dive into the data analyst job market, I harnessed the power of several key tools:

- **Python:** The backbone of my analysis, allowing me to analyze the data and find critical insights.I also used the following Python libraries:
  - **Pandas Library:** This was used to analyze the data.
  - **Matplotlib Library:** I visualized the data.
  - **Seaborn Library:** Helped me create more advanced visuals.
- **Visual Studio Code:** My go-to for executing my Python scripts.
- **Git & GitHub:** Essential for version control and sharing my Python code and analysis, ensuring collaboration and project tracking.

# Data Preparation and Cleanup

This section outlines the steps taken to prepare the data for analysis, ensuring accuracy and usability.

## Import & Clean Up Data

I start by importing necessary libraries and loading the dataset, followed by initial data cleaning tasks to ensure data quality.

```python
# Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
import ast
import seaborn as sns

df = pd.read_csv('../data_jobs.csv') # puts data into dataframe

# Data Cleanup
df['job_posted_date'] = pd.to_datetime(df['job_posted_date'])
df['job_skills'] = df['job_skills'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)
```

## Filter SA Jobs

To focus my analysis on the U.S. job market, I apply filters to the dataset, narrowing down to roles based in the United States.

```python
df_SA = df[df['job_country'] == 'South Africa']

```

# The Analysis

Each python file for this project aimed at investigating specific aspects of the data job market. Here’s how I approached each question:

## 1. What are the most demanded skills for the top 3 most popular data roles?

To find the most demanded skills for the top 3 most popular data roles. I filtered out those positions by which ones were the most popular, and got the top 5 skills for these top 3 roles. This query highlights the most popular job titles and their top skills, showing which skills I should pay attention to depending on the role I'm targeting.

View my python file with detailed steps here: [Skill_Demand](Skill_Demand.py).

### Visualize Data

```python
fig, ax = plt.subplots(len(job_titles), 1)


for i, job_title in enumerate(job_titles):
    df_plot = df_skills_perc[df_skills_perc['job_title_short'] == job_title].head(5)
    sns.barplot(data=df_plot, x='skill_percent', y='job_skills', ax=ax[i], hue='skill_count', palette='dark:b_r')

plt.show()
```

### Results

![Likelihood of Skills Requested in the SA Job Postings](images/Skills_Request_Likelihood.png)

_Bar graph visualizing the likelihood of Skills Requested in the SA Job Postings._

### Insights:

- SQL is a versatile skill, highly demanded
  across all three roles, but most prominently for
  Data Analyst (15%) and Business Analyst (14%).

- Excel is the most reguested skill for Data Analst and Business Analyst with it in over half the job postings for both roles. For Data Analyst, SQL is the most sought-after skill, appearing in 15% of job postings.
- Cloud Engineers require more specialized sought-after skill, appearing in technical skills (AWS, Azure, Linux) compared to Data Analysts and Business Analyst who are expected
  to be proficient in more general data management and analysis tools (Excel, Tableau).

## 2. How are in-demand skills trending for Data Analyst?

## Visualize Data

```python

  from matplotlib.ticker import PercentFormatter
  from adjustText import adjust_text

  df_plot = df_sa_perc.iloc[:,:5]
  sns.lineplot(df_plot, dashes=False, palette='tab10')

  ax = plt.gca()
  ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))

  plt.show()

```

## Results

![Trending Top Skills for Data Analyst in SA](images/Data_Analyst_Top_Skills_SA.png)

_Bar graph visualizing the trending top trending skills for data analyst in SA._

## Insights:

- SQL remains the most consistently demanded skill throughout the year.
- Excel exprerienced a significant increase in demand starting around July until October, surpassing both python and power BI
- python, excel, power bi, excel and sas flunctuate throughout the year but remain essential skills for data analysts. Sas is less demand compared to the other skills.
