from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_session():
    server_name = "MRNGUYEN\\SQLEXPRESS"  # Tên server SQL Server của bạn
    user_name = "sa"                     # Tài khoản SQL Server
    password = "12345678"                # Mật khẩu
    db = "treemgmt_kbs"                   # Tên cơ sở dữ liệu
    
    # Chuỗi kết nối
    connection_string = (
        f"mssql+pyodbc://{user_name}:{password}@{server_name}/{db}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )
    
    try:
        engine = create_engine(connection_string, echo=False)
        session = sessionmaker(bind=engine)
        return session()
    except Exception as e:
        print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
        return None
