import json
import mysql.connector

# Database connection details
db_config = {
    "host": "localhost",
    "user": "root",  # Default phpMyAdmin user
    "password": "",  # Leave blank if no password is set
    "database": "researchpaper_db"  # Replace with your actual database name
}
try:
    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Create table if not exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS research_papers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        year INT,
        title VARCHAR(255),
        authors TEXT,
        abstract TEXT,
        pdf_url TEXT
    );
    """
    cursor.execute(create_table_query)

    # Load JSON data from file
    with open("metadata.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # Insert data into the table
    insert_query = """
    INSERT INTO research_papers (year, title, authors, abstract, pdf_url)
    VALUES (%s, %s, %s, %s, %s);
    """

    for paper in data:
        values = (paper["year"], paper["title"], paper["authors"], paper["abstract"], paper["pdf_url"])
        cursor.execute(insert_query, values)

    # Commit changes
    conn.commit()
    print("Data inserted successfully into 'research_papers' table!")


except mysql.connector.Error as err:
    print(f"❌ Error: {err}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
