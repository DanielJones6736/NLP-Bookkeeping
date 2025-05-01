import csv
import os

class Database_Tools:

    def __init__(self):
        file_path = "../data/database.csv"
        data = self.load_database_to_dict
        current_total = self.calculate_total_amount(data)
        pass


    def load_database_to_dict(file_path):
        """
        Loads data from a CSV file into a dictionary.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            dict: A dictionary where the keys are the column headers and the values are lists of column data.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file at {file_path} does not exist.")

        data_dict = {}
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                for key, value in row.items():
                    if key not in data_dict:
                        data_dict[key] = []
                    data_dict[key].append(value)
        return data_dict



    def calculate_total_amount(self, data_dict, amount_key="amount"):
        """
        Calculates the total amount from the data dictionary.

        Args:
            data_dict (dict): The dictionary containing the data.
            amount_key (str): The key in the dictionary that holds the amount values.

        Returns:
            float: The total amount calculated from the data.
        """
        if amount_key not in data_dict:
            raise KeyError(f"The key '{amount_key}' does not exist in the data dictionary.")

        total = 0.0
        for value in data_dict[amount_key]:
            try:
                total += float(value)
            except ValueError:
                raise ValueError(f"Invalid value '{value}' encountered in the '{amount_key}' column.")
        return total



    def __str__(self, data):
        if not data:
            return "The database is empty."

        # Get the headers
        headers = list(data.keys())
        # Get the rows
        rows = zip(*[data[header] for header in headers])

        # Create a table-like string
        table = " | ".join(headers) + "\n"  # Header row
        table += "-+-".join("-" * len(header) for header in headers) + "\n"  # Separator row
        for row in rows:
            table += " | ".join(row) + "\n"  # Data rows

        return table.strip()

if __name__ == "__main__":

    database = Database_Tools()
    print(database)    # Example usage:

