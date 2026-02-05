import os
import pandas as pd

class Storage:

    COLUMNS = [
        "name",
        "address",
        "phone",
        "official_site",
        "facebook",
        "instagram",
        "linkedin",
        "place_id_search",
    ]

    def ensure_csv_exists(self, file_path):
        """Create CSV file with headers if it does not exist."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if not os.path.exists(file_path):
            df = pd.DataFrame(columns=self.COLUMNS)
            df.to_csv(file_path, index=False, encoding="utf-8")
            print("CSV file created at startup.")

    def save_to_csv(self, data, file_path):
        """Always ensure CSV exists and then write data."""
        self.ensure_csv_exists(file_path)

        if not data:
            print("No data found. CSV left with headers only.")
            return

        normalized = [
            {col: row.get(col, "N/A") for col in self.COLUMNS}
            for row in data
        ]

        df = pd.DataFrame(normalized, columns=self.COLUMNS)
        df.to_csv(file_path, index=False, encoding="utf-8")
        print("CSV saved with data.")
