
-- Customer Table 
CREATE TABLE customer (
    customer_id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(75) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    login_attempts INT DEFAULT 0,
    wrong_login_attempts INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer Address Table
CREATE TABLE customer_address (
    address_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customer(customer_id) ON DELETE CASCADE,
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    country VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

-- Payment Details Table
CREATE TABLE payment_details (
    payment_id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES order_details(order_id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL,
    tax DECIMAL(10, 2) DEFAULT 0.00,
    provider VARCHAR(50),
    status VARCHAR(25) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order Details Table
CREATE TABLE order_details (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customer(customer_id) ON DELETE CASCADE,
    total DECIMAL(10, 2) NOT NULL,
    tax DECIMAL(10, 2) DEFAULT 0.00,
    payment_id BIGINT REFERENCES payment_details(payment_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order Items Table
CREATE TABLE order_items (
    order_item_id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES order_details(order_id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES product(product_id) ON DELETE CASCADE,
    quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product Table
CREATE TABLE product (
    product_id BIGSERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_description TEXT,
    sku VARCHAR(100) UNIQUE NOT NULL,
    category_id BIGINT REFERENCES category(category_id) ON DELETE SET NULL,
    inventory_id BIGINT REFERENCES inventory(inventory_id) ON DELETE SET NULL,
    price DECIMAL(10, 2) NOT NULL,
    tax DECIMAL(10, 2) DEFAULT 0.00,
    rating FLOAT DEFAULT 0,
    review_count INT DEFAULT 0,
    discount_id BIGINT REFERENCES discount(discount_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product Image Table
CREATE TABLE product_image (
    image_id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES product(product_id) ON DELETE CASCADE,
    image_url VARCHAR(255) NOT NULL
);

-- Category Table
CREATE TABLE category (
    category_id BIGSERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    category_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory Table
CREATE TABLE inventory (
    inventory_id BIGSERIAL PRIMARY KEY,
    quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Discount Table
CREATE TABLE discount (
    discount_id BIGSERIAL PRIMARY KEY,
    discount_name VARCHAR(50) NOT NULL,
    discount_description TEXT,
    discount_percentage DECIMAL(5, 2) NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Shopping Session Table
CREATE TABLE shopping_session (
    session_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customer(customer_id) ON DELETE CASCADE,
    total DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cart Item Table
CREATE TABLE cart_item (
    cart_item_id BIGSERIAL PRIMARY KEY,
    session_id BIGINT NOT NULL REFERENCES shopping_session(session_id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES product(product_id) ON DELETE CASCADE,
    quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Carrier Table
CREATE TABLE carrier (
    carrier_id BIGSERIAL PRIMARY KEY,
    carrier_name VARCHAR(255) NOT NULL,
    carrier_phone VARCHAR(15) NOT NULL,
    carrier_email VARCHAR(255) NOT NULL UNIQUE
);

-- Admin User Table
CREATE TABLE admin_user (
    admin_user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    type_id BIGINT NOT NULL REFERENCES admin_type(admin_id) ON DELETE CASCADE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admin Type Table
CREATE TABLE admin_type (
    admin_id BIGSERIAL PRIMARY KEY,
    admin_type_name VARCHAR(50) NOT NULL,
    permissions TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
