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
app.debug=True
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:database-password@localhost:5432/postgres'
# conn_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

@app.route('/', methods=['GET'])
def etl_endpoint():
    
    # Data is imported into pandas dataframes.  The delimiter is structured to remove tabs as well as commas.
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

    # LOAD
    db_host = 'localhost'
    db_port = 5432
    db_name = 'postgres'
    db_user = 'postgres'
    db_password = 'database-password'
    print("fdsa")
    # final_answer_3.to_sql('data', con=db.engine, index=False, if_exists='replace')
    # print("fdsa")
    # db.session.add(1)
    # db.session.commit()
    command = 'psql -h localhost -U postgres -d postgres -c "SELECT * FROM user;"'
    output = subprocess.check_output(command, shell=True, universal_newlines=True).strip()
    print(output)
    # print("fdsa")
    # db.Column(db.Integer, primary_key=True)
    # db.Column(db.String(80), unique=True, nullable=False)
    # print("fdsa")
    data = Data(name='John')
    db.session.add(data)
    db.session.commit()
    # print("fdsa")

    # conn_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    # engine = create_engine(conn_string)
    # print('sdfa')
    # print(engine)
    # with engine.connect() as connection:
    #     result = connection.execute('SELECT 1')
    #     print(result.scalar())
    #     print('sdfa')
    # table_name = 'answer1'
    # conn = psycopg2.connect('postgresql://postgres:database-password@localhost:5432/postgres')
    # engine = create_engine(conn)
    # final_answer_1.to_sql("answer1", engine, if_exists='replace', index=False)
    # print("dsa")
    # add up the compounds across the experiments
    # merge the users
    return 'ETL '

    #TODO Clean up Code and add comments
    #TODO Get app to run regardless of system
    #TODO Connect to the pSQL database
    #TODO Write a readme.md


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)