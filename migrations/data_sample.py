from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models import Base, Category, Client, Item, Order, OrderItem

# Create database engine
engine = create_engine("sqlite:///dev/data.db")
Base.metadata.bind = engine

# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()


def init_sample_data():
    # Clear existing data
    session.query(OrderItem).delete()
    session.query(Order).delete()
    session.query(Item).delete()
    session.query(Category).delete()
    session.query(Client).delete()

    # Create categories
    electronics = Category(name="Electronics")
    computers = Category(name="Computers", parent=electronics)
    laptops = Category(name="Laptops", parent=computers)
    smartphones = Category(name="Smartphones", parent=electronics)
    clothing = Category(name="Clothing")
    mens_clothing = Category(name="Men's Clothing", parent=clothing)
    womens_clothing = Category(name="Women's Clothing", parent=clothing)

    session.add_all(
        [
            electronics,
            computers,
            laptops,
            smartphones,
            clothing,
            mens_clothing,
            womens_clothing,
        ]
    )
    session.commit()

    # Create items
    items = [
        Item(
            name="Gaming Laptop",
            quantity=15,
            price=1299.99,
            category=laptops,
        ),
        Item(
            name="Business Laptop",
            quantity=45,
            price=899.99,
            category=laptops,
        ),
        Item(
            name="Smartphone Pro",
            quantity=25,
            price=799.99,
            category=smartphones,
        ),
        Item(
            name="Basic Smartphone",
            quantity=100,
            price=299.99,
            category=smartphones,
        ),
        Item(
            name="Men's T-Shirt",
            quantity=120,
            price=24.99,
            category=mens_clothing,
        ),
        Item(
            name="Women's Dress",
            quantity=200,
            price=49.99,
            category=womens_clothing,
        ),
    ]

    session.add_all(items)
    session.commit()

    # Create clients
    clients = [
        Client(name="John Doe", address="123 Main St, Cityville"),
        Client(name="Jane Smith", address="456 Oak Ave, Townsville"),
    ]

    session.add_all(clients)
    session.commit()

    print("Sample data initialized successfully!")


if __name__ == "__main__":
    init_sample_data()
