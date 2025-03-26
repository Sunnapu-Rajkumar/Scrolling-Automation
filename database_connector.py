import mysql.connector 


def database_connector():
    print("All is well")

    try:
        conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='evega@123',
        port=3306, 
        database='evega',
        auth_plugin='mysql_native_password'
        )

        print("Connected object created")
        
        if conn.is_connected():
            print("Connection Established....")
            
    except Exception as e:
        print("Error occurred:", e)

    cursor = conn.cursor()
    cursor.execute("""            CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Details VARCHAR(255),
            MRP INT,
            Discount INT,
            Price INT,
            Rating VARCHAR(255)
                );""")
#     cursor.execute("""DROP TABLE products;
# """)
    return conn,cursor

# finally:
#     print("In finally block")
#     if 'conn' in locals() and conn.is_connected():
#         conn.close()
#         print("Connection closed")



database_connector()











# import mysql.connector 

# print("All is well")
# try:
#   conn = mysql.connector.connect(
#      host='localhost',
#      password='evega@123',
#      user='root',
#      port = 3306,
#      database = 'evega')
#   print("All")
#   if conn.is_connected():
#             print("Connection Establishment....")
# except mysql.connector.Error as e:
#     print("Error:", e)

# finally:
#      if 'conn' in locals() and conn.is_connected():
#         conn.close()



