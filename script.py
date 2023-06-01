from flask import Flask, request
import pandas as pd


app = Flask(__name__)

@app.route('/', methods=['GET'])
def etl_endpoint():
    
    # ETL process goes here
    compounds_data = pd.read_csv('data/compounds.csv', delimiter=',\t|,', engine='python')
    experiments_data = pd.read_csv('data/user_experiments.csv', delimiter=',\t|,', engine='python')
    users_data = pd.read_csv('data/users.csv', delimiter=',\t|,', engine='python')

    print(compounds_data)
    print(experiments_data)
    print(users_data)

    
    # 1. Total experiments a user ran.
    user_experiments = users_data.join(experiments_data.set_index('user_id'), on='user_id', how='left')
    final_answer_1 = user_experiments.groupby(['user_id', 'name', 'email'], as_index=False)['experiment_id'].agg(['count'])
    print(user_experiments)
    print(final_answer_1)

    # 2. Average experiments amount per user.
    final_answer_2 = final_answer_1['count'].mean()
    print(final_answer_2)

    # 3. User's most commonly experimented compound.
    user_experiments['experiment_compound_ids'] = user_experiments.apply(
        lambda x: x['experiment_compound_ids'].split(';'), axis=1)
    exploded_compounds = user_experiments.explode("experiment_compound_ids").rename(columns={"experiment_compound_ids":"compound_id"})
    exploded_compounds = exploded_compounds.astype({"compound_id": 'int64'})
    exploded_compounds = exploded_compounds.join(compounds_data.set_index('compound_id'), on='compound_id', how='left')

    
    final_answer_3 = exploded_compounds.groupby(['user_id', 'name', 'email'], as_index=False)['compound_id'].agg(pd.Series.mode)
    print(final_answer_3)
    # add up the compounds across the experiments
    # merge the users
    return 'ETL '

def transform_function(data):
    transformed_data = data.upper()
    return transformed_data

def load_function(data):
    print(data)

if __name__ == '__main__':
    app.run(port=8080)