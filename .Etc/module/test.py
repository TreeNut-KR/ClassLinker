from dotenv import load_dotenv
import mysql.connector
import os

# Load environment variables from .env file
load_dotenv(".\ClassLinker_PyQT\DB_env\.env")

def get_parent_contact(student_name):
    # Database connection settings from environment variables
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': os.getenv('DB_PORT')  # Make sure this is a string if not using it directly as an int
    }
    
    try:
        # Connect to the database
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        
        # Execute SQL query
        query = "SELECT contact_parent FROM student WHERE student_pk = %s"
        cursor.execute(query, (student_name,))
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Close the connection
        cursor.close()
        cnx.close()
        
        # Return the result, or a message if the student doesn't exist
        if result:
            return result[0]
        else:
            return "해당 이름의 학생이 데이터베이스에 존재하지 않습니다."
    except mysql.connector.Error as err:
        return f"데이터베이스 에러: {err}"

# Example of using the function
student_name = input("QR코드 : ")
parent_contact = get_parent_contact(student_name)
print(f"{student_name}의 부모님 연락처: {parent_contact}")
