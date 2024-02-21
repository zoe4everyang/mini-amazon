-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.


CREATE TABLE Product (
    p_productkey BIGINT PRIMARY KEY NOT NULL,
    p_productname VARCHAR(255) NOT NULL,
    p_description TEXT NOT NULL,
    p_imageurl VARCHAR(255) NOT NULL,
    p_price DOUBLE PRECISION NOT NULL,
    p_catkey BIGINT NOT NULL,
    p_link TEXT NOT NULL,
    FOREIGN KEY (p_catkey) REFERENCES Category(cat_catkey)
);

CREATE TABLE ProductSeller (
    ps_productkey BIGINT NOT NULL,
    ps_sellerkey BIGINT NOT NULL,
    ps_quantity BIGINT NOT NULL,
    ps_price DOUBLE PRECISION NOT NULL,
    ps_discount DOUBLE PRECISION,
    ps_createtime DATE NOT NULL,
    PRIMARY KEY (ps_productkey, ps_sellerkey),
    FOREIGN KEY (ps_productkey) REFERENCES Product(p_productkey)
    FOREIGN KEY (ps_sellerkey) REFERENCES Seller(s_sellerkey)
);

CREATE TABLE Category (
    cat_catkey BIGINT PRIMARY KEY NOT NULL,
    cat_catname VARCHAR(255) NOT NULL
);

