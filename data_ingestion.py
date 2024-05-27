# Load the raw data
# Load & Inspect Raw Data 
file_path = 'Cleaned_Data.csv'  # Replace with your actual file path
with open(file_path, 'r') as file:
    raw_data = file.readlines()

# Display the first few lines to understand the structure
print(raw_data[:10])

# Parse and Clean Data
import csv

# Parse and clean data based on inspected structure
cleaned_rows = []
for line in raw_data[1:]:
    try:
        # Use csv reader to correctly handle the quoted strings
        split_line = next(csv.reader([line]))
        if len(split_line) == 25:
            cleaned_rows.append(split_line)
        else:
            print(f"Skipping line due to incorrect number of fields: {len(split_line)}")
            continue
    except Exception as e:
        print("Error parsing line:", line, e)
        continue

# Define columns based on actual data structure
columns = [
    "Product Info", "Sales1", "Quantity1", "Discount1", "Profit1",
    "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode", "Customer ID", 
    "Customer Name", "Segment", "Country", "City", "State", "Postal Code", "Region", 
    "Product ID", "Category", "Sub-Category", "Product Name", "Sales2", "Quantity2", "Discount2"
]

# Create DataFrame
cleaned_data = pd.DataFrame(cleaned_rows, columns=columns)

# Check intermediate result
print(cleaned_data.head())


# Convert and clean relevant columns
# Ensure 'Sales2' and 'Profit1' are numeric
cleaned_data['Sales2'] = pd.to_numeric(cleaned_data['Sales2'], errors='coerce')
cleaned_data['Profit1'] = pd.to_numeric(cleaned_data['Profit1'], errors='coerce')

# Check for missing values before dropping
print("Missing values before dropping:", cleaned_data[['Category', 'Sales2', 'Profit1']].isnull().sum())

# Drop rows with missing values in 'Category', 'Sales2', and 'Profit1'
cleaned_data.dropna(subset=['Category', 'Sales2', 'Profit1'], inplace=True)

# Check intermediate result after dropping NaNs
print("Data after dropping missing values:", cleaned_data.head())

# Convert 'Category' to category type
cleaned_data['Category'] = cleaned_data['Category'].astype('category')


# Plot Data
import matplotlib.pyplot as plt
import seaborn as sns

# Example 1: Sales distribution by category
plt.figure(figsize=(12, 6))
sns.boxplot(data=cleaned_data, x='Category', y='Sales2')
plt.title('Sales Distribution by Category')
plt.xticks(rotation=45)
plt.show()

# Example 2: Profit distribution by category
plt.figure(figsize=(12, 6))
sns.boxplot(data=cleaned_data, x='Category', y='Profit1')
plt.title('Profit Distribution by Category')
plt.xticks(rotation=45)
plt.show()

# Example 3: Sales vs Profit scatter plot
plt.figure(figsize=(12, 6))
sns.scatterplot(data=cleaned_data, x='Sales2', y='Profit1', hue='Category', alpha=0.6)
plt.title('Sales vs Profit Scatter Plot')
plt.xlabel('Sales')
plt.ylabel('Profit')
plt.legend(title='Category')
plt.show()

# Example 4: Sales over time
cleaned_data['Order Date'] = pd.to_datetime(cleaned_data['Order Date'], format='%d-%m-%Y', errors='coerce')
sales_over_time = cleaned_data.groupby('Order Date')['Sales2'].sum().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=sales_over_time, x='Order Date', y='Sales2')
plt.title('Sales Over Time')
plt.xlabel('Order Date')
plt.ylabel('Total Sales')
plt.show()

