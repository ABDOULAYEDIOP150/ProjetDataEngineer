ALTER TABLE raw.customers
ADD PRIMARY KEY (customer_id);

ALTER TABLE raw.products
ADD PRIMARY KEY (product_id);

ALTER TABLE raw.orders
ADD PRIMARY KEY (order_id);

ALTER TABLE raw.order_items
ADD PRIMARY KEY (order_item_id);

ALTER TABLE raw.payments
ADD PRIMARY KEY (payment_id);

ALTER TABLE raw.orders
ADD CONSTRAINT fk_orders_customers
FOREIGN KEY (customer_id)
REFERENCES raw.customers(customer_id);

ALTER TABLE raw.order_items
ADD CONSTRAINT fk_order_items_orders
FOREIGN KEY (order_id)
REFERENCES raw.orders(order_id);

ALTER TABLE raw.order_items
ADD CONSTRAINT fk_order_items_products
FOREIGN KEY (product_id)
REFERENCES raw.products(product_id);

ALTER TABLE raw.payments
ADD CONSTRAINT fk_payments_orders
FOREIGN KEY (order_id)
REFERENCES raw.orders(order_id);

ALTER TABLE raw.products
ADD CONSTRAINT chk_products_price_positive
CHECK (price >= 0);

ALTER TABLE raw.order_items
ADD CONSTRAINT chk_order_items_quantity_positive
CHECK (quantity > 0);

ALTER TABLE raw.order_items
ADD CONSTRAINT chk_order_items_line_total_positive
CHECK (line_total >= 0);

ALTER TABLE raw.payments
ADD CONSTRAINT chk_payments_amount_positive
CHECK (amount >= 0);