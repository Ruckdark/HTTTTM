from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from db_connection import get_session
from datetime import datetime

# Khởi tạo Base dùng để định nghĩa model
Base = declarative_base()

# Định nghĩa bảng Tree khớp với cơ sở dữ liệu
class Tree(Base):
    __tablename__ = 'Trees'
    tree_id = Column('TreeId', Integer, primary_key=True, autoincrement=True)
    species = Column('Species', String)
    height = Column('Height', Float)
    age = Column('Age', Integer)
    health_status = Column('HealthStatus', String)
    leaf_color = Column('LeafColor', String)
    pest_infestation = Column('PestInfestation', Boolean, nullable=False, default=False)  # Thêm cột PestInfestation
    water_status = Column('WaterStatus', String, nullable=False, default='Normal')  # Thêm cột WaterStatus
    location = Column('Location', String)
    last_updated = Column('LastUpdated', DateTime, default=datetime.utcnow)  # Thêm cột LastUpdated

# Hàm lấy tất cả cây từ database
def fetch_all_trees():
    session = get_session()
    if not session:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return []

    try:
        trees = session.query(Tree).all()
        for tree in trees:
            print(f"Tree ID: {tree.tree_id}, Species: {tree.species}, Health: {tree.health_status}")
        return trees
    except Exception as e:
        print(f"Lỗi khi truy vấn dữ liệu: {e}")
        return []
    finally:
        session.close()

# Hàm thêm cây mới vào database
def add_tree(species, height, age, health_status, leaf_color, pest_infestation=False, water_status='Normal', location=None):
    session = get_session()
    if not session:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return False

    new_tree = Tree(
        species=species,
        height=height,
        age=age,
        health_status=health_status,
        leaf_color=leaf_color,
        pest_infestation=pest_infestation,
        water_status=water_status,
        location=location
    )
    
    try:
        session.add(new_tree)
        session.commit()
        print("Đã thêm cây mới thành công!")
        return True
    except Exception as e:
        session.rollback()
        print(f"Lỗi khi thêm cây mới: {e}")
        return False
    finally:
        session.close()

