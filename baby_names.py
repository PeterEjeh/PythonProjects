import re

# Extract Names from the HTML File
def extract_baby_names():
    with open('baby2008.html', 'r') as html_file:
        html_content = html_file.read()

    # Use Regex to extract names
    regex_pattern = r"<td>([A-Za-z]+)</td>"
    baby_names = re.findall(regex_pattern, html_content)

    return baby_names


# Custom Sorting Algorithm (Selection Sort)
def selection_sort(names):
    n = len(names)
    for i in range(n):
        # Assume the current index has the smallest element
        min_index = i
        for j in range(i + 1, n):
            if names[j] < names[min_index]:
                min_index = j
        # Swap the smallest element found with the current element
        names[i], names[min_index] = names[min_index], names[i]
    return names

# Binary Search Implementation
def binary_search(sorted_names, target_name):
    left, right = 0, len(sorted_names) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_names[mid] == target_name:
            return mid  # Found the name, return its index
        elif sorted_names[mid] < target_name:
            left = mid + 1  # Search in the right half
        else:
            right = mid - 1  # Search in the left half
    return -1  # Name not found

# show extracted names
baby_names = extract_baby_names()
print(f"Extracted Names: {baby_names}")

#sort the names using selection sort
sorted_names = selection_sort(baby_names)
print(f"Sorted Names: {sorted_names}")

search_name = "Sharon"  # Replace with the name you're searching for
index = binary_search(sorted_names, search_name)
if index != -1:
    print(f"{search_name} found at index {index}")
else:
    print(f"{search_name} not found")

import psycopg2

# Database connection parameters
db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "peters",
    "host": "127.0.0.1",
    "port": 5432
}

def create_table():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Create table query
        create_table_query = """
           CREATE TABLE IF NOT EXISTS baby_names (
               id SERIAL PRIMARY KEY,
               name TEXT NOT NULL,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
           );
           """

        # Execute the query
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'baby_names' has been created or already exists.")

    except Exception as e:
        print("Error while creating table:", e)

    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()


# Call the function to create the table
create_table()


# Save extracted baby names to the database
def save_baby_names_to_db(names):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Insert each name into the table
        for name in names:
            cursor.execute("INSERT INTO baby_names (name) VALUES (%s)", (name,))

        # Commit the transaction
        conn.commit()

        print(f"{len(names)} names have been saved to the database.")

    except Exception as e:
        print("Error while saving names to the database:", e)

    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()


# Call the function to save the names
save_baby_names_to_db(baby_names)
