import pandas as pd
from sqlalchemy import create_engine
import psycopg2

def get_sp_data(host, user, password, database, port, start_date, end_date):
    conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    engine =  create_engine(conn_str)
    query = f"SELECT * FROM public.pos_sp_products WHERE created_at BETWEEN '{start_date}' AND '{end_date}' "
    df = pd.read_sql(query, con=engine)
    return df

if __name__ == "__main__":
    host='host_is_dead'
    user='lalit.joshi'
    password='it_does_not_work'
    database = 'dev'
    port = 5439
    start_date = '2023-03-12'
    end_date = '2023-03-13'

    get_sp_data = get_sp_data(host, user, password, database, port, start_date, end_date)
