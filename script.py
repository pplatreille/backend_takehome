from flask import Flask, request
import pandas as pd
import os
#import psycopg2
from sqlalchemy import create_engine
import psycopg2
import subprocess
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

@app.route('/', methods=['GET'])
def etl_endpoint():
    
    # Data is imported into pandas dataframes.  The delimiter is structured to remove tabs as well as commas.
    compounds_data = pd.read_csv('data/compounds.csv', delimiter=',\t|,', engine='python')
    experiments_data = pd.read_csv('data/user_experiments.csv', delimiter=',\t|,', engine='python')
    users_data = pd.read_csv('data/users.csv', delimiter=',\t|,', engine='python')
    
    # 1. Total experiments a user ran.
    user_experiments = users_data.join(experiments_data.set_index('user_id'), on='user_id', how='left')
    final_answer_1 = user_experiments.groupby(['user_id', 'name', 'email'], as_index=False)['experiment_id'].agg(['count'])
    print("Q1: Number of Experiments per User")
    print(final_answer_1)

    # 2. Average experiments amount per user.
    final_answer_2 = final_answer_1['count'].mean()
    print("Q2: Average Number of Experiments per User")
    print(final_answer_2)

    # 3. User's most commonly experimented compound.
    user_experiments['experiment_compound_ids'] = user_experiments.apply(
        lambda x: x['experiment_compound_ids'].split(';'), axis=1)
    exploded_compounds = user_experiments.explode("experiment_compound_ids").rename(columns={"experiment_compound_ids":"compound_id"})
    exploded_compounds = exploded_compounds.astype({"compound_id": 'int64'})
    exploded_compounds = exploded_compounds.join(compounds_data.set_index('compound_id'), on='compound_id', how='left')
    final_answer_3 = exploded_compounds.groupby(['user_id', 'name', 'email'], as_index=False)['compound_id'].agg(pd.Series.mode)
    print("Q3: The Most Commonly Used Experiment Compound per User")
    print(final_answer_3)
   
    return 'Process Completed Sucessfully'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)