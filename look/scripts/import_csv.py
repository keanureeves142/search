import csv
from pathlib import Path
from look.models import Product

def import_csv_data():
    # Define the path to the CSV file
    file_path = Path(__file__).resolve().parent.parent / "amazon_product_details.csv"

    # Open the file and read its content
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Check if the product already exists
                if not Product.objects.filter(product_id=row['product_id']).exists():
                    Product.objects.create(
                        product_id=row['product_id'],
                        product_name=row['product_name'],
                        category=row['category'],
                        discounted_price=float(row['discounted_price'].replace(',', '')) if row['discounted_price'] else 0.0,
                        actual_price=float(row['actual_price'].replace(',', '')) if row['actual_price'] else 0.0,
                        discount_percentage=row['discount_percentage'] if row['discount_percentage'] else "0%",
                        rating=float(row['rating']) if row['rating'] else 0.0,
                        rating_count=int(row['rating_count'].replace(',', '')) if row['rating_count'] else 0,
                    )
                else:
                    print(f"Skipping duplicate product_id: {row['product_id']}")
            except Exception as e:
                print(f"Error importing row: {row}, error: {e}")
    print("Data imported successfully!")
