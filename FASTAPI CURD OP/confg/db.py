from sqlalchemyMetaData import create_engine

engine = create_engine("mysql+pymysql://root@localhost:3306/andai_db")
meta = MetaData()
conn = engine.connect()
