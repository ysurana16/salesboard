import pandas as pd
import random
from datetime import datetime, timedelta

# Configurations
start_date = datetime(2025, 4, 1)
end_date = datetime(2025, 8, 30)
max_orders_per_day = 3

# Define customer types
frequent_customers = ["AlphaEnergy", "Bharat Trading", "Zenith Power", "JaySteel"]
occasional_customers = ["SouthStar Energy", "Tradelink Global", "RawEdge Exim", "Greenline Corp", "Indus Minerals"]
tapering_customers = ["Om Metals", "SteelBridge", "PowerHouse Ltd"]
new_customers = ["Eastern Traders", "MacroTrade LLP", "MaxCommodities", "NewAge Fuels"]
all_customers = frequent_customers + occasional_customers + tapering_customers + new_customers

products = {
    "Indonesian Coal": {"location": "Surat", "price_range": (7800, 8300), "cost_range": (6600, 7500)},
    "Pet Coke": {"location": "Mumbai", "price_range": (2150, 2250), "cost_range": (1990, 2100)},
    "Iron Ore": {"location": "Raipur", "price_range": (4000, 5500), "cost_range": (5000, 7000)},
    "Manganese Ore": {"location": "Kolkata", "price_range": (3780, 3930), "cost_range": (3600, 3750)},
}

credit_days_range = (20, 45)

# Helper function
def random_price_range(price_range):
    return random.randint(*price_range)

# Generate orders
data = []
current_date = start_date
tapering_set = set(random.sample(tapering_customers, 2))
new_start_day = start_date + timedelta(days=10)

while current_date <= end_date:
    orders_today = random.randint(1, max_orders_per_day)
    day_customers = []

    # Choose customers based on category
    potential_customers = []

    # Frequent: almost every day
    if random.random() < 0.9:
        potential_customers += frequent_customers

    # Occasional: 2-3 times a week
    if random.random() < 0.5:
        potential_customers += random.sample(occasional_customers, k=random.randint(1, len(occasional_customers)))

    # Tapering: reduce toward end of month
    if current_date < end_date - timedelta(days=10) and random.random() < 0.6:
        potential_customers += list(tapering_set)

    # New: appear mid-month onwards
    if current_date >= new_start_day and random.random() < 0.4:
        potential_customers += random.sample(new_customers, k=random.randint(1, 2))

    selected_customers = random.sample(list(set(potential_customers)), min(orders_today, len(set(potential_customers))))

    for customer in selected_customers:
        product = random.choice(list(products.keys()))
        product_info = products[product]
        quantity = random.randint(8, 35)
        unit_price = random_price_range(product_info["price_range"])
        cost_price = random_price_range(product_info["cost_range"])
        credit_days = random.randint(*credit_days_range)

        data.append({
            "Date": current_date.strftime("%Y-%m-%d"),
            "Customer Name": customer,
            "Product": product,
            "Location": product_info["location"],
            "Quantity": quantity,
            "Cost Price": cost_price,
            "Unit Price": unit_price,
            "Credit Days": credit_days
        })

    current_date += timedelta(days=1)

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV if needed
df.to_csv("generated_orders_apr2025.csv", index=False)

# Preview
print(df.head())
