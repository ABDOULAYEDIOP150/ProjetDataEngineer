import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

fake = Faker("fr_FR")

seed = int(datetime.now().strftime("%Y%m%d"))

Faker.seed(seed)
random.seed(seed)

#Faker.seed(42)
#random.seed(42)


def generate_customers(n=1000):
    customers = []

    for i in range(1, n + 1):
        customers.append({
            "customer_id": i,
            "full_name": fake.name(),
            "email": fake.unique.email(),
            "phone": fake.phone_number(),
            "city": fake.city(),
            "country": "France",
            "created_at": fake.date_time_between(start_date="-2y", end_date="now")
        })

    return pd.DataFrame(customers)


def generate_products(n=200):
    categories = ["electronics", "fashion", "home", "beauty", "sports", "books"]
    products = []

    for i in range(1, n + 1):
        products.append({
            "product_id": i,
            "product_name": fake.word().capitalize() + " " + fake.word(),
            "category": random.choice(categories),
            "price": round(random.uniform(5, 500), 2),
            "created_at": fake.date_time_between(start_date="-2y", end_date="now")
        })

    return pd.DataFrame(products)


def generate_orders(customers_df, products_df, n_orders=3000):
    orders = []
    order_items = []
    payments = []

    for order_id in range(1, n_orders + 1):
        customer_id = random.choice(customers_df["customer_id"].tolist())
        order_date = fake.date_time_between(start_date="-1y", end_date="now")
        status = random.choice(["delivered", "shipped", "processing", "cancelled"])

        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": order_date,
            "status": status
        })

        number_items = random.randint(1, 5)
        selected_products = products_df.sample(number_items)

        total_amount = 0

        for _, product in selected_products.iterrows():
            quantity = random.randint(1, 4)
            unit_price = float(product["price"])
            line_total = quantity * unit_price
            total_amount += line_total

            order_items.append({
                "order_item_id": len(order_items) + 1,
                "order_id": order_id,
                "product_id": int(product["product_id"]),
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": round(line_total, 2)
            })

        payments.append({
            "payment_id": order_id,
            "order_id": order_id,
            "payment_method": random.choice(["card", "paypal", "bank_transfer"]),
            "amount": round(total_amount, 2),
            "payment_date": order_date + timedelta(minutes=random.randint(1, 120)),
            "payment_status": "paid" if status != "cancelled" else "refunded"
        })

    return (
        pd.DataFrame(orders),
        pd.DataFrame(order_items),
        pd.DataFrame(payments)
    )


if __name__ == "__main__":
    customers = generate_customers()
    products = generate_products()
    orders, order_items, payments = generate_orders(customers, products)

    customers.to_csv("data/raw/simulated/customers.csv", index=False)
    products.to_csv("data/raw/simulated/products.csv", index=False)
    orders.to_csv("data/raw/simulated/orders.csv", index=False)
    order_items.to_csv("data/raw/simulated/order_items.csv", index=False)
    payments.to_csv("data/raw/simulated/payments.csv", index=False)

    print("Données simulées générées avec succès.")