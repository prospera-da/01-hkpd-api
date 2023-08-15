from sqlalchemy import Column, Integer, String
from ..database import Base

class Akun(Base):
    __tablename__ = 'ground_truth_akun'
    id = Column(Integer, primary_key=True)
    akun = Column(String)
    kelompok = Column(String)
    jenis = Column(String)
    objek = Column(String)
    rincian_objek = Column(String)
    sub_rincian_objek = Column(String)
    level1 = Column(String)
    level2 = Column(String)
    level3 = Column(String)
    level4 = Column(String)
    level5 = Column(String)
    level6 = Column(String)
