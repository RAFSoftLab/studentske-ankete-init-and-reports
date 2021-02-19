import mysql.connector

mysqlParams = dict(host='localhost', user='root', password='', db='c8_rafanketa')

cnx = mysql.connector.connect(user=mysqlParams['user'], password=mysqlParams['password'], host=mysqlParams['host'], charset='utf8', database=mysqlParams['db'], port=3307)
cursor = cnx.cursor()

trenutni_semestar = 11