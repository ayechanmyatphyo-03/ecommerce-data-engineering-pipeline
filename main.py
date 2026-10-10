
import pandas as pd

# Step 1: Create sample e-commerce data
orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104, 105],
    "product": ["Laptop", "Mouse", "Keyboard", "Monitor", "Mouse"],
    "quantity": [1, 2, 1, 1, 3],
    "unit_price": [800, 25, 60, 200, 25]
})

# Step 2: Transform data
orders["total_amount"] = orders["quantity"] * orders["unit_price"]

# Step 3: Display results
print("E-commerce Orders:")
print(orders)

# Step 4: Calculate total revenue
total_revenue = orders["total_amount"].sum()
print("\nTotal Revenue: $", total_revenue)
