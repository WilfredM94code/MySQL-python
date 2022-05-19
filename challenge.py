# *-*-*-*-*-*-*-*-* ---- ----------------------- ---- *-*-*-*-*-*-*-*-*
# *-*-*-*-*-*-*-*-* ---- Create a MySQL Database


""" ----------------------Tasks
1- Create a company_sales DB
4- Create a table called sales for this DB where order_num is the primary key
2- Import data from the company_sales CSV file into this MySQL Database
3- Query the data for some information
5- Using python, discover what the most important order was and who ordered it

-----------------------------------------------------------------------
You can use the MySQL connector approach or the SQLAlchemy + pandas approach.
My solution will be using the SQLAlchemy ORM + pandas approach.
"""

# MySQL connector approach

from sqlalchemy import Column, String, Integer, Float, create_engine, select
import pandas
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector as mysql

connection = mysql.connect(
    user='root',
    password='=SQL2525.',
    host='localhost',
    database='sales',
    allow_local_infile=True
)
# 1- Create a company_sales DB
cursor = connection.cursor()
database_query = 'CREATE DATABASE company_sales'
cursor.execute(database_query)
# 4- Create a table called sales for this DB where order_num is the primary key (¿4? wtf... FTW)
table_query = '''CREATE TABLE sales (
    order_num INT (225) NOT NULL AUTO_INCREMENT,
    order_type VARCHAR (255) NOT NULL,
    cust_name VARCHAR (255) NOT NULL,
    cust_state VARCHAR (255) NOT NULL,
    prod_category VARCHAR (255) NOT NULL,
    prod_number VARCHAR (255) NOT NULL,
    prod_name VARCHAR (255) NOT NULL,
    quantity INT (225) NOT NULL,
    price FLOAT (3) NOT NULL,
    discount FLOAT (3) NOT NULL,
    order_total FLOAT (3) NOT NULL,
    PRIMARY KEY (order_num)
) '''
cursor.execute(table_query)
connection.commit()
# 2- Import data from the company_sales CSV file into this MySQL Database
import_query = r'''LOAD DATA LOCAL INFILE
    'C:\\Users\\Wilfred M PRO\\Desktop\\portfolio\\study\\MySQL\\resources\\company_sales.csv'
    INTO TABLE sales
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    (order_num,order_type,cust_name,cust_state,prod_category,prod_number,prod_name,quantity,price,discount,order_total);
    '''
cursor.execute(import_query)
connection.commit()
# 3- Query the data for some information
table_query = '''SELECT sa.cust_name, sa.order_total
    FROM sales sa
    ORDER BY sa.order_total DESC
    LIMIT 2;'''
cursor.execute(table_query)
# 5- Using python, discover what the most important order was and who ordered it
results = cursor.fetchall()[0]
print('THE MOST IMPORTANT ORDER OF ALL TIMES\nClient = {0}\nTotal = {1}'.format(
    results[0], results[1]))

# SQLAlchemy + pandas


engine = create_engine(
    'mysql+mysqlconnector://root:=SQL2525.@localhost:3306', echo=True)

engine.execute('DROP DATABASE company_sales')
# This statement is executed to erase the previous 'company_sales' database
engine.execute('DROP TABLE IF EXISTS sales')
# To avoid the 1050 error for a table that was inside the now dropped database
# the hypotethical 'sales' table that was associated to the 'company_sales' database


# 1- Create a company_sales DB
engine.execute('CREATE DATABASE company_sales')
engine.execute('USE company_sales')

Base = declarative_base()

# 4- Create a table called sales for this DB where order_num is the primary key


class Sales (Base):
    __tablename__ = 'sales'
    __table_args__ = {'schema': 'company_sales'}
    order_num = Column(Integer, primary_key=True, nullable=False)
    order_type = Column(String(255), nullable=False)
    cust_name = Column(String(255), nullable=False)
    cust_state = Column(String(255), nullable=False)
    prod_category = Column(String(255), nullable=False)
    prod_number = Column(String(255), nullable=False)
    prod_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    order_total = Column(Float, nullable=False)

    def __repr__(self):
        return '''<Sales(order_num = '{0}', order_type = '{1}', cust_name = '{2}',
        cust_state = '{3}', prod_category = '{4}', prod_number = '{5}',
        prod_name = '{6}', quantity = '{7}', price = '{8}', discount = '{9}',
        order_total = '{10}')>'''.format(self.order_num, self.order_type,
                                         self.cust_name, self.cust_state,
                                         self.prod_category, self.prod_number,
                                         self.prod_name, self.quantity, self.price,
                                         self.discount, self.order_total)


Base.metadata.create_all(engine)

# 2- Import data from the company_sales CSV file into this MySQL Database
file_name = r'resources/company_sales.csv'
data_frame = pandas.read_csv(file_name)

data_frame.to_sql(con=engine, name=Sales.__tablename__,
                  if_exists='replace', index=False)

session = sessionmaker()
session.configure(bind=engine)
session = session()
# 3- Query the data for some information
results = session.execute(select(Sales.cust_name, Sales.order_total).order_by(
    Sales.order_total.desc()).limit(1))
# 5- Using python, discover what the most important order was and who ordered it
for result in results:
    print(result)
