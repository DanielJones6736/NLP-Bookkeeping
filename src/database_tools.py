import csv
import os

class Database_Tools:

    data:dict
    current_total:float

    def __init__(self):
        file_path = "data\\database.csv"
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



    def save_database(self, file_path="data\\database.csv"):
        """
        Overwrites the current data dictionary to a CSV file.

        Args:
            file_path (str): The path to the CSV file where data will be saved.
        """
        if not self.data:
            raise ValueError("No data to save.")

        # Define the headers
        headers = ["id", "type", "amount", "source"]

        # Overwrite data in the CSV file
        with open(file_path, mode='w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)  # Write the header row
            for key, values in self.data.items():
                writer.writerow([key] + values)  # Write each row



    def insert_data(self, record_type, amount, source:str, date:str):
        """
        Adds a new record to the data dictionary.

        Args:
            record_type (str): The type of the record.
            amount (float): The amount associated with the record.
            source (str): The source of the record.
            date (str): The date of the record.

        Raises:
            ValueError: If the amount is not a valid number.
        """
        try:
            amount = float(amount)  # Ensure the amount is a valid float
        except ValueError:
            raise ValueError("The amount must be a valid number.")

        self.data[len(self.data) + 1] = [record_type, f"{amount:.2f}", source, str(date)]  # Store date as a string
        self.current_total = self.calculate_total_amount(self.data)  # Update the total amount

    

    def update_data(self, record_id, record_type=None, amount=None, source=None, date=None):
        """
        Updates an existing record in the data dictionary.

        Args:
            record_id (str): The unique identifier for the record to update.
            record_type (str, optional): The new type of the record.
            amount (float, optional): The new amount associated with the record.
            source (str, optional): The new source of the record.
            date (str, optional): The new date of the record.

        Raises:
            KeyError: If the record_id does not exist in the data dictionary.
            ValueError: If the amount is not a valid number.
        """
        record_id = str(record_id)  # Ensure record_id is a string
        if record_id not in self.data:
            raise KeyError(f"Record with id '{record_id}' does not exist.")

        # Update fields if new values are provided
        if record_type is not None:
            self.data[record_id][0] = record_type
        if amount is not None:
            try:
                self.data[record_id][1] = f"{float(amount):.2f}"
            except ValueError:
                raise ValueError("The amount must be a valid number.")
        if source is not None:
            self.data[record_id][2] = source
        if date is not None:
            self.data[record_id][3] = date  # Store date as a string

        # Recalculate the total amount
        self.current_total = self.calculate_total_amount(self.data)



    def __str__(self):
        if not self.data:
            return "The database is empty."

        # Define the headers
        headers = ["id", "type", "amount", "source", "date"]

        # Prepare rows for display
        rows = [[key] + value for key, value in self.data.items()]

        # Ensure all rows have a date column (default to empty string if missing)
        for row in rows:
            if len(row) < len(headers):
                row.append("")

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
    print(database)
    print(f"Sum of amounts: ${database.current_total}\n")  # Print the total amount calculated from the database

    database.insert_data("expense", 500.00, "Rent", "2023-10-01")
    print(database)
    print(f"Sum of amounts: ${database.current_total}\n")  # Print the total amount calculated from the database

    database.update_data(1, amount=200.00, source="Updated Source", date="2023-10-02")
    print(database)
