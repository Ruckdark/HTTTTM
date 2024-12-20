from sqlalchemy import create_engine

def get_engine():
    server_name = "MRNGUYEN\\SQLEXPRESS"
    user_name = "sa"
    password = "12345678"
    db = "treemgmtkbs"
    connection_string = f"mssql+pyodbc://{user_name}:{password}@{server_name}/{db}?driver=SQL+Server"
    engine = create_engine(connection_string)
    return engine
