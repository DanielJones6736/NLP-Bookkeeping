import os
import pandas as pd

class Database_Tools:

    data: pd.DataFrame
    current_total: float

    def __init__(self):
        file_path = "data\\database.csv"
        self.data = self.load_database_to_dataframe(file_path)
        self.current_total = self.calculate_total_amount()



    def __str__(self):
        if self.data.empty:
            return "The database is empty."
        df_copy = self.data.copy()
        df_copy['amount'] = df_copy['amount'].astype(float).map("{:.2f}".format)
        return df_copy.to_string(index=False)



    def load_database_to_dataframe(self, file_path):
        """
        Loads data from a CSV file into a Pandas DataFrame.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            pd.DataFrame: A DataFrame containing the CSV data.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file at {file_path} does not exist.")

        try:
            df = pd.read_csv(file_path)
            if 'id' not in df.columns:
                raise KeyError("The CSV file must contain an 'id' column.")
            return df
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {e}")



    def save_database(self, file_path="data\\database.csv"):
        """
        Saves the current DataFrame to a CSV file.

        Args:
            file_path (str): The path to the CSV file where data will be saved.
        """
        if self.data.empty:
            raise ValueError("No data to save.")

        self.data.to_csv(file_path, index=False)



    def insert_data(self, record_type, amount, note:str, category:str, date:str):
        """
        Adds a new record to the DataFrame.

        Args:
            record_type (str): The type of the record.
            amount (float): The amount associated with the record.
            note (str): The note for the record.
            category (str): The category of the record.
            date (str): The date of the record.

        Raises:
            ValueError: If the amount is not a valid number.
        """
        try:
            amount = float(amount)
        except ValueError:
            raise ValueError("The amount must be a valid number.")
        
        # If type is expense, convert to negative
        if record_type.lower() == 'expense':
            amount = -abs(amount)

        new_id = self.data['id'].max() + 1 if not self.data.empty else 1

        # Convert date to datetime format
        try:
            date = pd.to_datetime(date).strftime('%Y-%m-%d')
        except Exception:
            raise ValueError("The date must be in a valid format (e.g., YYYY-MM-DD).")

        new_record = pd.DataFrame([{
            'id': new_id,
            'type': record_type,
            'amount': f"{amount:.2f}",
            'note': note,
            'category': category,
            'date': date
        }])
        self.data = pd.concat([self.data, new_record], ignore_index=True)
        self.current_total = self.calculate_total_amount()
        self.save_database()
        return f"Record added successfully. ID: {new_id}, Type: {record_type}, Amount: {amount:.2f}, Note: {note}, Category: {category}, Date: {date}"



    def update_data(self, record_id:int=None, record_type:str=None, amount:float=None, note:str=None, category:str=None, date:str=None):
        """
        Updates an existing record in the DataFrame.

        Args:
            record_id (int): The unique identifier for the record to update.
            record_type (str, optional): The new type of the record.
            amount (float, optional): The new amount associated with the record.
            note (str, optional): The new note for the record.
            category (str, optional): The new category of the record.
            date (str, optional): The new date of the record.

        Raises:
            KeyError: If the record_id does not exist in the DataFrame.
            ValueError: If the amount is not a valid number.
        """
        if record_id is None:
            if self.data.empty:
                raise ValueError("No data to update.")
            record_id = self.data['id'].max()

        if record_id not in self.data['id'].values:
            raise KeyError(f"Record with id '{record_id}' does not exist.")

        if record_type is not None:
            self.data.loc[self.data['id'] == record_id, 'type'] = record_type

        if amount is not None:
            try:
                if record_type and record_type.lower() == 'expense':
                    amount = -abs(float(amount))
                self.data.loc[self.data['id'] == record_id, 'amount'] = f"{float(amount):.2f}"
            except ValueError:
                raise ValueError("The amount must be a valid number.")
            
        if note is not None:
            self.data.loc[self.data['id'] == record_id, 'note'] = note
            
        if category is not None:
            self.data.loc[self.data['id'] == record_id, 'category'] = category

        if date is not None:
            self.data.loc[self.data['id'] == record_id, 'date'] = date

        self.current_total = self.calculate_total_amount()
        self.save_database()
        return f"Record with ID {str(record_id)} updated successfully with Type: {str(record_type)}, Amount: {str(amount)}, Note: {str(note)}, Category: {str(category)}, Date: {str(date)}"



    def delete_data(self, record_id:int = None):
        """
        Deletes a record from the DataFrame. If no record_id is provided, it deletes the last record.

        Args:
            record_id (int): The unique identifier for the record to delete.

        Raises:
            KeyError: If the record_id does not exist in the DataFrame.
        """
        if record_id is None:
            if self.data.empty:
                raise ValueError("No data to delete.")
            record_id = self.data['id'].max()

        if record_id not in self.data['id'].values:
            raise KeyError(f"Record with id '{record_id}' does not exist.")

        self.data = self.data[self.data['id'] != record_id]
        self.current_total = self.calculate_total_amount()
        self.save_database()



    def calculate_total_amount(self, record_type=None):
        """
        Calculates the total amount from the DataFrame. If a record type is specified,
        calculates the total for that type only.

        Args:
            record_type (str, optional): The type of the record ('expense' or 'pay').

        Returns:
            float: The total amount calculated from the data.
        """
        if record_type is None:
            return self.data['amount'].astype(float).sum()
        return self.data[self.data['type'].str.lower() == record_type.lower()]['amount'].astype(float).sum()



    def calculate_monthly_total(self, record_type:str=None, month:int=None, year:int=None):
        """
        Calculates the total amount of a specific record type for a given month and year.
        If an argument is missing, it considers all options under that category.

        Args:
            record_type (str, optional): The type of the record ('expense' or 'payment').
            month (int, optional): The month for which to calculate the total (1-12).
            year (int, optional): The year for which to calculate the total.

        Returns:
            float: The total amount for the specified filters.
        """
        filtered_data = self.data

        if record_type is not None:
            filtered_data = filtered_data[filtered_data['type'].str.lower() == record_type.lower()]
        if month is not None:
            filtered_data = filtered_data[pd.to_datetime(filtered_data['date']).dt.month == month]
        if year is not None:
            filtered_data = filtered_data[pd.to_datetime(filtered_data['date']).dt.year == year]

        return filtered_data['amount'].astype(float).sum()



    def list_notes(self, record_type=None, month=None, year=None):
        """
        Lists all notes based on the specified month, year, and record type. 
        If no filters are provided, lists all notes.

        Args:
            month (int, optional): The month for which to list notes (1-12).
            year (int, optional): The year for which to list notes.
            record_type (str, optional): The type of the record ('expense' or 'payment').

        Returns:
            list: A list of unique notes.
        """
        filtered_data = self.data

        if month is not None:
            filtered_data = filtered_data[(pd.to_datetime(filtered_data['date']).dt.month == month)]
        if year is not None:
            filtered_data = filtered_data[pd.to_datetime(filtered_data['date']).dt.year == year]
        if record_type is not None:
            filtered_data = filtered_data[filtered_data['type'].str.lower() == record_type.lower()]

        return filtered_data['note'].unique().tolist()
        
        
        
    def list_categories(self, record_type=None, month=None, year=None):
        """
        Lists all categories based on the specified month, year, and record type. 
        If no filters are provided, lists all categories.

        Args:
            month (int, optional): The month for which to list categories (1-12).
            year (int, optional): The year for which to list categories.
            record_type (str, optional): The type of the record ('expense' or 'payment').

        Returns:
            list: A list of unique categories.
        """
        filtered_data = self.data

        if month is not None:
            filtered_data = filtered_data[(pd.to_datetime(filtered_data['date']).dt.month == month)]
        if year is not None:
            filtered_data = filtered_data[pd.to_datetime(filtered_data['date']).dt.year == year]
        if record_type is not None:
            filtered_data = filtered_data[filtered_data['type'].str.lower() == record_type.lower()]

        return filtered_data['category'].unique().tolist()



    def calculate_average_amount(self, record_type=None, month=None, year=None):
        """
        Calculates the average amount based on the specified month, year, and record type.
        If a parameter is missing, it considers all options under that category.

        Args:
            record_type (str, optional): The type of the record ('expense' or 'payment').
            month (int, optional): The month for which to calculate the average (1-12).
            year (int, optional): The year for which to calculate the average.

        Returns:
            float: The average amount for the specified filters.
        """
        filtered_data = self.data

        if record_type is not None:
            filtered_data = filtered_data[filtered_data['type'].str.lower() == record_type.lower()]
        if month is not None:
            filtered_data = filtered_data[pd.to_datetime(filtered_data['date']).dt.month == month]
        if year is not None:
            filtered_data = filtered_data[pd.to_datetime(filtered_data['date']).dt.year == year]

        if filtered_data.empty:
            return 0.0

        return round(filtered_data['amount'].astype(float).mean(), 2)



    def export_data(self, file_format="json", record_type:str=None, month=None, year=None):
        """
        Exports the DataFrame as a JSON or CSV string, with optional filtering by month and year.

        Args:
            file_format (str): The format to export the data ('json' or 'csv').
            month (int, optional): The month for which to filter the data (1-12).
            year (int, optional): The year for which to filter the data.

        Returns:
            str: The exported data as a string.

        Raises:
            ValueError: If the file_format is not 'json' or 'csv'.
        """
        filtered_data = self.data

        if record_type is not None:
            filtered_data = filtered_data[filtered_data['type'].str.lower() == record_type.lower()]
        if month is not None:
            filtered_data = filtered_data[pd.to_datetime(filtered_data['date']).dt.month == month]
        if year is not None:
            filtered_data = filtered_data[pd.to_datetime(filtered_data['date']).dt.year == year]

        # Create a copy to avoid modifying the original data
        export_data = filtered_data.copy()
        
        # Ensure 'amount' is float type for consistent data type
        export_data['amount'] = export_data['amount'].astype(float)
        
        if file_format.lower() == "json":
            return export_data.to_json(orient="records", date_format="iso")
        elif file_format.lower() == "csv":
            return export_data.to_csv(index=False)
        elif file_format.lower() == "list":
            # Convert all data to appropriate Python types before returning as list
            result = []
            for _, row in export_data.iterrows():
                row_list = []
                for val in row:
                    # Convert pandas/numpy types to Python native types
                    if hasattr(val, 'item'):  # Check if it's a numpy scalar
                        val = val.item()  # Convert numpy type to native Python type
                    row_list.append(val)
                result.append(row_list)
            return result
        else:
            raise ValueError("Invalid file format. Please choose 'json' or 'csv'.")



    def batch_insert_data(self, records):
        """
        Batch add multiple records to the database.

        Args:
            records (list): A list of dictionaries containing multiple record data. Each record should be a dictionary with the following keys:
                            'type', 'amount', 'note', 'category', 'date'

        Returns:
            list: A list of successfully added record IDs.
        """
        if not records or not isinstance(records, list):
            raise ValueError("Records must be a non-empty list")
            
        added_ids = []
        
        for record in records:
            if not all(k in record for k in ['type', 'amount', 'note', 'category', 'date']):
                raise ValueError("Each record must contain type, amount, note, category, and date")
                
            try:
                amount = float(record['amount'])
                
                # if the record is an expense, convert to negative
                if record['type'].lower() == 'expense':
                    amount = -abs(amount)
                    
                new_id = int(self.data['id'].max() + 1) if not self.data.empty else 1
                
                # convert date to standard format
                try:
                    date = pd.to_datetime(record['date']).strftime('%Y-%m-%d')
                except Exception:
                    raise ValueError(f"Date {record['date']} must be in a valid format (e.g., YYYY-MM-DD).")
                
                new_record = pd.DataFrame([{
                    'id': new_id,
                    'type': record['type'],
                    'amount': f"{amount:.2f}",
                    'note': record['note'],
                    'category': record['category'],
                    'date': date
                }])
                
                self.data = pd.concat([self.data, new_record], ignore_index=True)
                added_ids.append(int(new_id))  # convert to normal Python int type
                
            except ValueError as e:
                raise ValueError(f"Error processing record: {e}")
        
        # save data and update total
        self.current_total = self.calculate_total_amount()
        self.save_database()
        
        return added_ids



if __name__ == "__main__":
    database = Database_Tools()
    database.insert_data("expense", 100.50, "Monthly groceries", "Groceries", "2023-10-01")
    print(database)

    print(f"Sum of amounts: ${database.current_total}")
    print(f"Sum of amounts: ${database.calculate_total_amount()}")
    print(f"Monthly Total for October 2023: ${database.calculate_monthly_total('expense', 10, 2023)}")
    print("\n")
    print("\n")
    print(database.list_notes(month=2, year=2025, record_type="pay"))
    print(f"Average Amount for October 2023: ${database.calculate_average_amount(month=2, year=2025)}")

    print("\n")
    print(database.export_data("csv", month=2))
