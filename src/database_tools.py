import csv
import os

class Database_Tools:

    data:dict
    current_total:float

    def __init__(self):
        file_path = "data\database.csv"
        self.data = self.load_database_to_dict(file_path)
        self.current_total = self.calculate_total_amount(self.data)



    def load_database_to_dict(self, file_path):
        """
        Loads data from a CSV file into a dictionary.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            dict: A dictionary where the keys are the 'id' column values and the values are lists of the other column data.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file at {file_path} does not exist.")

        data_dict = {}
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                row_id = row.get('id')
                if row_id is None:
                    raise KeyError("The CSV file must contain an 'id' column.")
                data_dict[row_id] = [value for key, value in row.items() if key != 'id']
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
        total = 0.0
        for key, value in data_dict.items():
            try:
                total += float(value[1])  # Assuming the amount is the second item in the list
            except (ValueError, IndexError):
                raise ValueError(f"Invalid or missing amount value for key '{key}'.")
        return total



    def __str__(self):
        if not self.data:
            return "The database is empty."

        # Define the headers
        headers = ["id", "type", "amount", "source"]

        # Prepare rows for display
        rows = [[key] + value for key, value in self.data.items()]

        # Calculate column widths
        max_lengths = [max(len(str(item)) for item in [header] + [row[i] for row in rows]) for i, header in enumerate(headers)]

        # Create a table-like string
        table = []

        # Add headers
        header_row = " | ".join(f"{header:<{max_lengths[i]}}" for i, header in enumerate(headers))
        table.append(header_row)
        table.append("-+-".join("-" * max_lengths[i] for i in range(len(headers))))

        # Add rows
        for row in rows:
            table.append(" | ".join(f"{str(item):<{max_lengths[i]}}" for i, item in enumerate(row)))

        return "\n".join(table)



if __name__ == "__main__":

    database = Database_Tools()
    print(database)    # Example usage:
    print(f"Sum of amounts: ${database.current_total}")  # Print the total amount calculated from the database

