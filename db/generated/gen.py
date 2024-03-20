from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random

num_users = 100
num_products = 200
num_carts = 100 
num_product_carts = 200

num_sellers = 50 
num_categories = 50
num_lineitems = 200
num_orders = 20
num_products = 2000
num_purchases = 2500
num_product_reviews = 500
num_seller_reviews = 500

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users): 
            if uid % 100 == 0:
                print(f'{uid}', end=' ', flush=True)
            u_email = fake.unique.email()
            u_firstname = fake.first_name()
            u_lastname = fake.last_name()
            # Hash the password using werkzeug
            u_password = generate_password_hash(fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True))
            u_balance = round(random.uniform(0, 10000), 2)
            u_companyname = fake.company() if random.choice([True, False]) else ''
            u_streetaddress = fake.street_address()
            u_city = fake.city()
            u_stateregion = fake.state()
            u_zipcode = fake.zipcode()
            u_country = fake.country()
            u_phonenumber = ''.join(fake.random_choices(elements='0123456789', length=9))
            if len(u_phonenumber) > 20:
                u_phonenumber = u_phonenumber[:20]
            writer.writerow([uid, u_email, u_firstname, u_lastname, u_password, u_balance, u_companyname, u_streetaddress, u_city, u_stateregion, u_zipcode, u_country, u_phonenumber])
        print(f'\n{num_users} generated')


def gen_products(num_products):
    with open('Products.csv', 'w', newline='') as f:  # Ensure newline='' for proper line termination
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            # Generating additional fields to match the Product table structure
            p_description = fake.text(max_nb_chars=200)  # Generate a fake product description
            p_imageurl = fake.image_url()  # Generate a fake image URL
            p_catkey = fake.random_int(min=0, max=num_categories - 1)
            p_link = fake.url()  # Generate a fake URL for the product
            writer.writerow([pid, name, price, p_description, p_imageurl, p_catkey, p_link])
        print(f'\n{num_products} generated.')

def gen_carts(num_carts):
    with open('Carts.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        for cart_id in range(num_carts):
            writer.writerow([cart_id, cart_id])

def gen_categories(num_categories):
    with open('Categories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Categories...', end=' ', flush=True)
        for cat_id in range(num_categories):
            if cat_id % 10 == 0:
                print(f'{cat_id}', end=' ', flush=True)
            category_name = fake.word()
            writer.writerow([cat_id, category_name])
        print(f'{num_categories} generated')
    return


"""def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for sid in range(num_sellers):
            if sid % 10 == 0:
                print(f'{sid}', end=' ', flush=True)
            # For simplicity, we'll assign the same userkey for sellers as their corresponding user ID
            userkey = sid
            registration_date = fake.date_time_this_year()
            writer.writerow([sid, userkey, registration_date])
        print(f'{num_sellers} generated')
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return"""

def gen_product_reviews(num_product_reviews):
    with open('Product_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product_Reviews...', end=' ', flush=True)
        for pr_productkey in range(num_products):
            if pr_productkey % 10 == 0:
                print(f'{pr_productkey}', end=' ', flush=True)
            pr_userkey = f'{fake.random_int(max=500)}'
            pr_productname = fake.sentence(nb_words=4)[:-1]
            pr_orderkey = f'{str(fake.random_int(max=5000))}'
            pr_reviewdate = fake.date_time()
            pr_review = fake.sentence(nb_words=15)[:-1]
            pr_rating = f'{str(fake.random_int(max=4))}.{fake.random_int(max=9):01}'
            writer.writerow([pr_productkey, pr_userkey, pr_productname, pr_orderkey, pr_reviewdate, pr_review, pr_rating])
        print(f'{num_product_reviews} generated')
    return

def gen_product_sellers(num_products, num_sellers):
    existing_pairs = set()  # Set to keep track of existing product-seller pairs
    with open('ProductSellers.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        writer.writerow(['ps_productkey', 'ps_sellerkey', 'ps_quantity', 'ps_price', 'ps_discount', 'ps_createtime'])  # Write header row
        print('Generating ProductSellers...', end=' ', flush=True)
        for _ in range(num_products):
            while True:
                product_id = fake.random_int(min=0, max=num_products-1)
                seller_id = fake.random_int(min=0, max=num_sellers-1)
                # Check if the combination already exists
                if (product_id, seller_id) not in existing_pairs:
                    existing_pairs.add((product_id, seller_id))  # Add the new combination to the set
                    break  # Exit the loop if the combination is unique
            quantity = fake.random_int(min=1, max=100)
            price = fake.random_int(min=10, max=500)
            discount = fake.random_int(min=0, max=price)
            create_time = fake.date_this_decade().isoformat()
            writer.writerow([product_id, seller_id, quantity, price, discount, create_time])
        print('Done generating ProductSellers.')

def read_valid_product_seller_pairs():
    valid_pairs = set()
    with open('ProductSellers.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        for row in reader:
            product_id, seller_id = int(row[0]), int(row[1])
            valid_pairs.add((product_id, seller_id))
    return valid_pairs

def gen_product_carts(num_product_carts, num_carts, valid_pairs):
    with open('ProductCarts.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        for pc_id in range(num_product_carts):
            pc_cartkey = random.randint(0, num_carts - 1)
            pc_productkey, pc_sellerkey = random.choice(list(valid_pairs))  # Use a valid pair
            pc_savequantity = random.randint(0, 10)
            pc_incartquantity = random.randint(1, 20)
            writer.writerow([pc_id, pc_cartkey, pc_productkey, pc_sellerkey, pc_savequantity, pc_incartquantity])
        print('Done generating ProductCarts.')

gen_product_sellers(num_products, num_sellers)
valid_pairs = read_valid_product_seller_pairs()  # Read valid pairs from ProductSellers.csv
gen_product_carts(num_product_carts, num_carts, valid_pairs)  # Generate ProductCarts.csv using valid pairs
def gen_seller_reviews(num_seller_reviews):
    with open('Seller_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller_Reviews...', end=' ', flush=True)
        for sr_sellerkey in range(num_users):
            if sr_sellerkey % 10 == 0:
                print(f'{sr_sellerkey}', end=' ', flush=True)
            sr_userkey = f'{fake.random_int(max=500)}'
            sr_sellername = fake.sentence(nb_words=4)[:-1]
            sr_orderkey = f'{str(fake.random_int(max=5000))}'
            sr_reviewdate = fake.date_time()
            sr_review = fake.sentence(nb_words=15)[:-1]
            sr_rating = f'{str(fake.random_int(max=4))}.{fake.random_int(max=9):01}'
            writer.writerow([sr_sellerkey, sr_userkey, sr_sellername, sr_orderkey, sr_reviewdate, sr_review, sr_rating])
        print(f'{num_seller_reviews} generated')
    return

gen_users(num_users)
gen_sellers(num_sellers)
gen_products(num_products)
gen_categories(num_categories)
gen_carts(num_carts)



available_pids = gen_products(num_products)
"""gen_purchases(num_purchases, available_pids)"""
gen_product_reviews(num_product_reviews)
gen_seller_reviews(num_seller_reviews)