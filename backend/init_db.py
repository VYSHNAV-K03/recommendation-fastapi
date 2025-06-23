import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect("dummy.db")
cursor = conn.cursor()

# Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    item_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    brand TEXT,
    rating REAL,
    image_url TEXT
);
""")

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    location TEXT
);
""")

# Create user-item interactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_item_interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item_id INTEGER,
    rating REAL
);
""")

# Sample data for products
product_data = [
    (101, 'Laptop', 'Electronics', 800, 'Brand A', 4.5, 'https://images.pexels.com/photos/1229861/pexels-photo-1229861.jpeg?cs=srgb&dl=apple-mouse-artificial-flowers-blurred-background-1229861.jpg&fm=jpg'),
    (102, 'T-Shirt', 'Clothing', 20, 'Brand B', 3.2, 'https://www.creativefabrica.com/wp-content/uploads/2022/10/18/Graffiti-tshirt-design-Graphics-42119814-1.jpg'),
    (103, 'Apple', 'Groceries', 3, 'Brand C', 5.0, 'http://fruit-ukraine.org/eng/wp-content/uploads/2020/06/apple.jpeg'),
    (104, 'Book', 'Books', 15, 'Brand D', 4.0, 'https://wallpapercave.com/wp/wp2036967.jpg'),
    (105, 'Headphones', 'Electronics', 100, 'Brand E', 4.1, 'https://static.independent.co.uk/2023/02/24/11/sony%20headphones%20copy.jpg'),
    (106, 'Mouse', 'Electronics', 50, 'Brand F', 4.3, 'https://image-cdn.hypb.st/https://hypebeast.com/image/2023/02/razer-viper-mini-signature-edition-lightest-ever-gaming-mouse-info-001.jpg?q=75&w=800&cbr=1&fit=max'),
    (107, 'Shoes', 'Clothing', 80, 'Brand G', 4.8, 'https://cdn.sanity.io/images/c1chvb1i/production/a0479c253b26a9fec066b696305577ab9836f48a-1100x735.jpg?w=1760&h=1176&q=75&fit=max&auto=format'),
    (108, 'Pants', 'Clothing', 60, 'Brand H', 4.2, 'https://5.imimg.com/data5/SELLER/Default/2022/9/GM/YY/GL/160160585/casual-pants-for-men.jpg'),
    (109, 'Shirt', 'Clothing', 40, 'Brand I', 4.5, 'https://media.powerlook.in/catalog/product/d/p/dp1172021-1.jpg?aio=w-640'),
    (110, 'Banana', 'Groceries', 1, 'Brand J', 4.5, 'https://nutritionsource.hsph.harvard.edu/wp-content/uploads/2018/08/bananas-1354785_1920.jpg'),
    (112, 'Orange', 'Groceries', 1, 'Brand L', 4.5, 'https://cdn-prod.medicalnewstoday.com/content/images/articles/272/272782/oranges-in-a-box.jpg'),
    (113, 'Peach', 'Groceries', 1, 'Brand M', 4.5, 'https://blog.sakura.co/wp-content/uploads/2022/03/shutterstock_675217411-1.png'),
    (114, 'Diary With Your Name', 'Books', 5, 'Brand N', 4.5, 'https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcTy8qmoSyU-eo3-fWnO5k9wnCZfgi3vm_rl_BiNNF05EWINHLKh__lngCy6PyK4itOu2s5hCvfi7sYpIYQ2BJPr2G2m-e_3wW38_XCJS2ZnxkG9KYg6f55-'),
    (115, 'Onyx Storm', 'Books', 5, 'Brand O', 4.5, 'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcSKbpw5HhILB7elZQzekRBJEIwoh32XTXsyHadAvPk8RkGI8Fqgg4tqkWk6SGFSpzqzApJ_4e7trQch29I4jMC2OkyUkyQX2NbttQ3x0iXr3gov9TLA8Dbp'),
    (116, 'Nero: Alliance Series', 'Books', 5, 'Brand P', 4.5, 'https://m.media-amazon.com/images/I/81AfxOiqiCL.jpg'),
    (117, 'THE SHIVA TRILOGY', 'Books', 5, 'Brand Q', 4.5, 'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcShCB7yd1GMuzQI7_IubWTh3Ks5kTcYE-I1clnRM6S80EcZJ_N_rGZol3vuwSflIT-glkLWuqWVOKjSjN9HgZOgQP_A-YnpBsc1-4RaF4-V3zX6zJtN3IYSVA'),
    (119, 'Phone', 'Electronics', 500, 'Brand S', 4.5, 'https://cdn.thewirecutter.com/wp-content/media/2024/08/androidphones-2048px-04381.jpg'),
    (120, 'Tablet', 'Electronics', 300, 'Brand T', 4.5, 'https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'),
    (121, 'Monitor', 'Electronics', 200, 'Brand U', 4.5, 'https://images-cdn.ubuy.co.in/667da5b43bd86542f07f73a9-crua-27-165hz-180hz-curved-gaming.jpg'),
    (122, 'Keyboard', 'Electronics', 100, 'Brand V', 4.5, 'https://media.wired.com/photos/65b0438c22aa647640de5c75/3:2/w_2560%2Cc_limit/Mechanical-Keyboard-Guide-Gear-GettyImages-1313504623.jpg'),

]

# Sample data for users
user_data = [
    (1, 'Alice', 25, 'New York'),
    (2, 'Bob', 30, 'Los Angeles'),
    (3, 'Charlie', 22, 'Chicago'),
    (4, 'Diana', 28, 'Houston'),
    (5, 'Ethan', 35, 'Phoenix')
]

# Sample data for user-item interactions
user_item_data = [
    (1, 101, 5),
    (1, 102, 3),
    (2, 101, 4),
    (3, 103, 2),
    (4, 104, 4),
    (5, 105, 5),
    (5, 106, 4),
    (5, 107, 3),
    (5, 108, 4),
    (4, 109, 5),
    (4, 110, 4),
    (4, 111, 3),
    (4, 112, 4),
    (3, 113, 5),
    (3, 114, 4),
    (3, 115, 3),
    (3, 116, 4),
    (3, 117, 5),
    (2, 118, 4),
    (2, 119, 3),
    (2, 120, 4),
    (1, 121, 5),
    (1, 122, 4),
]

# Insert data into tables
cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)", product_data)
cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", user_data)
cursor.executemany("INSERT INTO user_item_interactions (user_id, item_id, rating) VALUES (?, ?, ?)", user_item_data)

# Commit and close the connection
conn.commit()
conn.close()

print("Database created successfully.")
