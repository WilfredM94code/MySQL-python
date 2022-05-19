'''
-----------------------------------------------------------------
----------------------------- MySQL -----------------------------
-----------------------------------------------------------------

MySQL is a DBMS (database management system) developed by Oracle

To get this DBMS this link must be followed (there are several 
distributions of MySQL but we'll be working with the Community distribution):

https://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-installer-community-8.0.29.0.msi

This sofware will be downloaded using the previous link. If any problem 
presented during the installation there must be deleted every SQL 
software (if possible) from the PC. The installation will required a 
password creation and several 'next' steps

It will allow to create several SQL connections or sessions, this helps to
manage several servers/databases/projects. Once opened the MySQL Workbench
there is a left vertical panel for:
1 - Welcome panel: It offers access to every MySQL projects, to manage every
MySQL project and to create new ones
2 - Models: It offers acces to every developed BD model available on the PC
3 - Migration: It allows several options to migrate DB

-----------------------------------------------------------------
------------------- MySQL creating a database -------------------
--------------------- from the MySQL prompt ---------------------
-----------------------------------------------------------------

From the 'Welcome panel' there can be accessed the MySQL prompt by right clicking 
any available connections at the 'MySQL connections' sub-panel and selecting the 
'Start Command Line Client'

Once accessed any connection the prompt will ask for the connection password
and once introduced the password there can be typed any SQL query on the prompt

In this case there will be used the next line of code:

'CREATE DATABASE blogs;'

This way a databse can be created using MySQL prompt

-----------------------------------------------------------------
--------------------- MySQL creating a table --------------------
-------------------- and inserting data to it -------------------
--------------------- from the MySQL prompt ---------------------
-----------------------------------------------------------------

To create a table within the MySQL prompt there has to be used the common SQL
sybtax for a query. In this case there will be used the next line of code:

'USE blogs;
CREATE TABLE topics (topic_id INT (11) NOT NULL AUTO_INCREMENT, title VARCHAR (30), category VARCHAR (255), PRIMARY KEY(topic_id));'

CREATE TABLE tasks (task_id INT(11) NOT NULL AUTO_INCREMENT, topic_id INT(11) NOT NULL, description VARCHAR (255) ,PRIMARY KEY(task_id), FOREIGN KEY (topic_id) REFERENCES topics (topic_id));

This lines of code will allows us to use the 'blogs' database
and then we'll be able to create a table within that database with
several columns within it

Adding the next line of code will to add values to the topics table

INSERT INTO topics (title,category) VALUES ("Link is not working", "HTML");
INSERT INTO tasks (description,topic_id) VALUES ("Make sure the URL path is entered correctly", 1);
INSERT INTO tasks (description,topic_id) VALUES ("Type the URL in the href attribute", 1);
INSERT INTO topics (title,category) VALUES ("MySQL server is not responding", "MySQL DBMS");
INSERT INTO tasks (description,topic_id) VALUES ("Reconfigure MySQL server", 2);

The block of codes adds data to both tables, either the 'topics' and 'tasks' tables.
The data inserted into the 'topics' does not add any value to the 'topic_id' 
field/column, this is because the 'topic_id' field is autoincremented, this way 
the field does not adds a NULL value even no value is passed.

For the 'tasks' table there must be passed a value related to the 'foregin key' 
referenced in the 'topics' table, particulary in the 'topic_id' column/field.
There has to be considered that every row inserted within the 'topics' table 
has to have a matching value within the 'topic_id' column from the 'topics' table.
Note that for every row added in the 'tasks' table there was included a value 
for the 'topic_id' field matching one of the supposedly already declared value
from the 'topics' table 'topic_id' column/field.

To see every table added to the database there can be used the next line of code:

'USE blogs;
SHOW TABLES;'

To fetch a table from a database there has to be used the SQL syntax

'USE blogs;
SELECT * FROM topics;
SELECT * FROM tasks;'
'''

# -----------------------------------------------------------------
# --------------------- MySQL connect a Python --------------------
# -------------------- app to a MYSQL Database --------------------
# -----------------------------------------------------------------

import csv
import pandas
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, create_engine
import mysql.connector as mysql


def connect(db_name):
    try:
        return mysql.connect(
            host='localhost',
            user='root',
            password='=SQL2525.',
            database=db_name
        )

    except Exception as err:
        print(err)


if __name__ == '__main__':
    db = connect('blogs')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM topics')
    topic_records = cursor.fetchall()
    print(topic_records)
    cursor.execute('SELECT * FROM tasks')
    tasks_records = cursor.fetchall()
    print(tasks_records)
    db.close()

# -----------------------------------------------------------------
# ---------------------- MySQL encapsulating ----------------------
# ---------------------- database operation -----------------------
# -----------------------------------------------------------------

# A good way to standarize the SQL queries is making them part of a
# function. In this way everytime is required it will be easily called
# and executed


def add_new_topic(cursor, topic_title, topic_category, task_descriptions):
    topic_data = (topic_title, topic_category)
    cursor.execute("""INSERT INTO topics (title,category)
                    VALUES (%s,%s)
                    """, topic_data)
    topic_id = cursor.lastrowid
    tasks_data = []
    for description in task_descriptions:
        task_data = (topic_id, description)
        tasks_data.append(task_data)
    cursor.executemany("""INSERT INTO tasks (topic_id,description)
                    VALUES (%s,%s)
                    """, tasks_data)


if __name__ == '__main__':
    db = connect('blogs')
    cursor = db.cursor()
    # This instructions has been run
    ####
    # tasks = ['Clrear the browsers cache', 'Use a different browser']
    # add_new_topic(cursor, 'Gmail not oppending', 'Social', tasks)
    # db.commit()  # This instruction will make permanent every change made
    ####
    # Note that if not wmployed the 'db.commit()' method, every query will be executed but not commited.
    # Which means that the process will occur at SQL level but not will be reflected upon the database.
    # This means that fields such as thos with 'Autoincrement' will increment values every time a query
    # is executed but won have any effect upon the database unles the 'db.commit()' method is executed
    cursor.execute('SELECT * FROM topics')
    topic_records = cursor.fetchall()
    print(topic_records)
    cursor.execute('SELECT * FROM tasks')
    tasks_records = cursor.fetchall()
    print(tasks_records)
    db.close()

# -----------------------------------------------------------------
# ------------------- MySQL connecting a Python -------------------
# -------------- app + SQLAlchemy ORM to a Database ---------------
# -----------------------------------------------------------------

# (ORM or Object Relational Mapper is a Programming model that
# allows to map the DataBase structures upon a logic structure to simplify
# the the development of a program) (just for the record)

# For this part of the course there will be made a new database called
# 'todo_list'. This process will be made using the MySQL prompt and the next
# command:

# CREATE DATABASE to_do_list;


engine = create_engine(
    'mysql+mysqlconnector://root:=SQL2525.@localhost:3306/to_do_list', echo=True)

# The function 'create_engine()' has a particular syntax which responses
# dialect+driver://username:password@host:port/database
# This syntax has several parts:
# 1 - Dialect: A messenger object for a Dialect that corresponds to a single execution
# 2 - Driver: The name of the BDAPI (I.E.:psycopg2, pyodbc, cx_oracle)
# 3 - Username: User authorized to access the database
# 4 - Password: The password of the username
# 5 - Host: Is a unique identifier that serves as the name of a host computer.
# 6 - POrt: The diposed port of the computer to manage the comunication of the server
# 7 - Database: The databse name

# The echo keyword when True it returns the messages that the dialect returns on it's
# executed operations

Base = declarative_base()
# Is a protocol that allows to create models of databases declaring every wanted component

# Because we're using a ORM the syntax of this method requires object declaration


class Topic (Base):
    # Table attributes
    __tablename__ = 'topics'
    __table_args__ = {'schema': 'to_do_list'}
    # Setting up the columns
    topic_id = Column(Integer, primary_key=True)
    title = Column(String(length=100))
    description = Column(String(length=255))

    def __repr__(self):  # This method stands for 'representation'
        return "<Topic(title = '{0}', description = '{1}')>".format(self.title, self.description)


class Task (Base):
    # Table attributes
    __tablename__ = 'tasks'
    __table_args__ = {'schema': 'to_do_list'}
    # Setting up the columns
    task_id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('to_do_list.topics.topic_id'))
    description = Column(String(length=255))
    # Relationship
    topic = relationship('Topic')

    def __repr__(self):  # This method stands for 'representation'
        return "<Task(description = '{0}')>".format(self.description)


Base.metadata.create_all(engine)


# -----------------------------------------------------------------
# -------------------- MySQL Using SQLAlchemy ---------------------
# ---------------- to insert records to a Database ----------------
# -----------------------------------------------------------------

# When working with models under the ORM there must been a session
# initialized to make queries into the database. To create a sessiom
# the next steps are meant to be followed

session_maker = sessionmaker()
print(session_maker)
print(type(session_maker))
# The 'sessionmaker()' returns a
# '<class 'sqlalchemy.orm.session.sessionmaker'>' object

session_maker.configure(bind=engine)
# The 'configure()' method recieves an an engine to set up a session

session = session_maker()
print(session)
print(type(session))
# Once setted up, the '<class 'sqlalchemy.orm.session.sessionmaker'>' object
# is able to return a '<class 'sqlalchemy.orm.session.Session'>'

# The data input goes like this

groceries_topic = Topic(title='Groceries', description='Buy vegetables')
# An instance of the Topic is made

session.add(groceries_topic)
# The '<class 'sqlalchemy.orm.session.Session'>' has the 'add()' method
# and it can recieve an object that has inherited the object Base, that
# in this case is the 'Topic' object

# Once there has been created a query under the 'add()' method, the change
# has to be 'Commited'
session.commit()

# To create a query with multiple inserts there can be created a list of objects

tasks = [
    Task(topic_id=groceries_topic.topic_id,
         description='Buy basil and carrots'),
    Task(topic_id=groceries_topic.topic_id,
         description='Buy some tomatoes as well')
]

# This list stores several 'Task' objects. This objects can be passed using the
# 'session.bulk_save_objects ()' method and passing the list as the argument

session.bulk_save_objects(tasks)
# Once queried the list the change has to be commited to the database

session.commit()

# To fetch data from a database the same '<class 'sqlalchemy.orm.session.Session'>'
# has to be employed

our_topic = session.query(Topic).filter_by(title='Groceries').first()
print(our_topic)

# Note that the metod '.first()' is just to fetch the las item from the filtered
# data

our_tasks = session.query(Task).all()
print(our_tasks)
# If used the '.all()' method the query will return every value filtered

# -----------------------------------------------------------------
# --------------------- MySQL Using MySQL to ----------------------
# ------------------------ import CSV data ------------------------
# -----------------------------------------------------------------

# Note: There has been added several files in the folder '../resources'
# for the porpuse of this chapter


connection = mysql.connect(
    user='root',
    password='=SQL2525.',
    host='localhost',
    database='sales',
    allow_local_infile=True
)

cursor = connection.cursor()

create_query = '''CREATE TABLE salespeople (
    id INT (225) NOT NULL AUTO_INCREMENT,
    first_name VARCHAR (255) NOT NULL,
    last_name VARCHAR (255) NOT NULL,
    email_address VARCHAR (255) NOT NULL,
    city VARCHAR (255) NOT NULL,
    state VARCHAR (255) NOT NULL,
    PRIMARY KEY (id)
) '''

cursor.execute('DROP TABLE IF EXISTS salespeople')
cursor.execute(create_query)

# Method 1 to import data from a CSV file
# This method is used to import only string data into a Database
# This way the data will be added includind a set of '' which is not
# desirable

with open(r'resources/salespeople.csv', 'r') as file:
    csv_data = csv.reader(file)
    for row in csv_data:
        row = tuple(row)
        cursor.execute('''INSERT INTO salespeople (first_name, last_name, email_address, city, state)
                        VALUES (%s,%s,%s,%s,%s)
        ''', row)


# Method 2 to import data from a CSV file

# This next line of code is required to be executed by the MySQL terminal
import_setting = 'set global local_infile = true;'
cursor.execute(import_setting)
# Thid statement will let MySQL system accept data from local files

# Note: The next path sould be modified, but keeping the raw format and '\\' for
# every '\' in the path
import_query = r'''LOAD DATA LOCAL INFILE
    'C:\\Users\\Wilfred M PRO\\Desktop\\portfolio\\study\\MySQL\\resources\\salespeople.csv'
    INTO TABLE salespeople
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    (first_name, last_name, email_address, city, state);
    '''

cursor.execute(import_query)

connection.commit()
cursor.execute('''SELECT * FROM salespeople LIMIT 10''')
print(cursor.fetchall())

connection.close()

# -----------------------------------------------------------------
# ------------------ MySQL Using SQLAlchemy and -------------------
# ------------------- Pandas to import CSV data -------------------
# -----------------------------------------------------------------

# For the porpuse of this chapter there has been created a database.
# To create such database there has been executed in the MySQL prompt
# the following statement

'CREATE DATABASE orders;'


engine = create_engine(
    'mysql+mysqlconnector://root:=SQL2525.@localhost:3306/orders', echo=True)

Base = declarative_base()


class Purchase (Base):
    __tablename__ = 'purchase'
    __table_args__ = {'schema': 'orders'}
    order_id = Column(Integer, primary_key=True)
    property_id = Column(Integer)
    property_city = Column(String(250))
    property_state = Column(String(250))
    product_id = Column(Integer)
    product_category = Column(String(250))
    product_name = Column(String(250))
    quantity = Column(Integer)
    product_price = Column(Float)
    order_total = Column(Float)

    def __repr__(self):
        return '''<Purchase(order_id = '{0}', property_id '{1}',
        property_city = '{2}', property_state = '{3}',
        product_id = '{4}', product_category = '{5}',
        product_name = '{6}', quantity = '{7}', product_price = '{8}',
        order_total = '{9}')>'''.format(self.order_id, self.property_id, self.property_city, self.property_state,
                                        self.product_id, self.product_category, self.product_name, self.quantity,
                                        self.product_price, self.order_total)


Base.metadata.create_all(engine)

file_name = r'resources/orders.csv'
data_frame = pandas.read_csv(file_name)
print(data_frame)
print(type(data_frame))
# The 'pandas.read_csv()' recieves a string that contains the path of a
# CSV file and returns a '<class 'pandas.core.frame.DataFrame'>' object

data_frame.to_sql(con=engine, name=Purchase.__tablename__,
                  if_exists='append', index=False)
# The '<class 'pandas.core.frame.DataFrame'>' object has the 'to_sql()'
# method can recieve the 'con' parameter which is
# sqlalchemy.engine.(Engine or Connection (Databases supported by
# SQLAlchemy are supported by pandas), it also accepts the name
# argument which in this case is and attribute of the 'Purchase' object,
# the 'if_exists' argument capable to change the behaviour of the operation
# if a table exists, and the 'index' argument that allows to include an
# index column

session = sessionmaker()
session.configure(bind=engine)
session = session()

results = session.query(Purchase).limit(10).all()

for result in results:
    print(result)

print(type(result))
