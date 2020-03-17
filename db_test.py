import sqlalchemy as db
engine = db.create_engine('mysql+pymysql://demo:password@localhost:3306/2fa')

print(engine)

# Test conn

conn = engine.connect()

print(conn)

conn.close()

print("done")
