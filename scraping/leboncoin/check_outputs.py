import csv

# Path to the CSV file
csv_file_path = "output.csv"

try:
    # Open the CSV file
    with open(csv_file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Iterate over each row in the CSV file
        for row in reader:
            # Extract each field into a variable
            description = row["description"]
            price = row["price"]
            details = row["details"]
            title = row["title"]

            # Print the variables to the terminal
            print(f"Description: {description}")
            print(f"Price: {price}")
            print(f"Details: {details}")
            print(f"Title: {title}\n")

except FileNotFoundError:
    print(f"File not found: {csv_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
