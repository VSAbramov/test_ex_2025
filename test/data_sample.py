from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models import Base, Category, Client, Item, Order, OrderItem

# Create database engine
engine = create_engine("sqlite:///dev/data.db")
Base.metadata.bind = engine

# Create session
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


def init_sample_data(session=db_session):
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
    toys = Category(name="Toys")

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
        Item(  # 0
            name="Gaming Laptop",
            quantity=15,
            price=1299.99,
            category=laptops,
        ),
        Item(  # 1
            name="Business Laptop",
            quantity=45,
            price=899.99,
            category=laptops,
        ),
        Item(  # 2
            name="Smartphone Pro",
            quantity=25,
            price=799.99,
            category=smartphones,
        ),
        Item(  # 3
            name="Basic Smartphone",
            quantity=100,
            price=299.99,
            category=smartphones,
        ),
        Item(  # 4
            name="Men's T-Shirt",
            quantity=120,
            price=24.99,
            category=mens_clothing,
        ),
        Item(  # 5
            name="Women's Dress",
            quantity=200,
            price=49.99,
            category=womens_clothing,
        ),
        Item(  # 6
            name="Плюшевый Колобок",
            quantity=110,
            price=15,
            category=toys,
        ),
    ]

    session.add_all(items)
    session.commit()

    # Create clients
    clients = [
        Client(name="John Doe", address="123 Main St, Cityville"),
        Client(name="Jane Smith", address="456 Oak Ave, Townsville"),
        Client(name="Big Boss", address="some towm"),
        Client(name="small Boss", address="some towm"),
        Client(name="Колобок", address="Неизвестная деревня"),
        Client(name="Марья Моревна", address="Тридевятое царство, дом 2"),
    ]

    session.add_all(clients)
    session.commit()

    # Create orders
    orders = [
        # John
        Order(client=clients[0]),  # 0
        # Jane
        Order(client=clients[1]),  # 1
        # Big Boss
        Order(client=clients[2]),  # 2
        # small Boss
        Order(client=clients[3]),  # 3
        # Колобок
        Order(client=clients[4]),  # 4
        Order(client=clients[4]),  # 5
        Order(client=clients[4]),  # 6
        # Марья Моревна
        Order(client=clients[5]),  # 7
        Order(client=clients[5]),  # 8
    ]
    session.add_all(orders)
    session.commit()

    # Create order items
    order_items = [
        # John
        OrderItem(order=orders[0], item=items[0], quantity=3, unit_price=1300),
        # Jane
        OrderItem(order=orders[1], item=items[5], quantity=2, unit_price=49),
        # Big Boss
        OrderItem(order=orders[2], item=items[1], quantity=50, unit_price=900),
        # small Boss
        OrderItem(order=orders[3], item=items[2], quantity=80, unit_price=800),
        # Колобок
        OrderItem(order=orders[4], item=items[4], quantity=400, unit_price=5),
        OrderItem(order=orders[5], item=items[6], quantity=400, unit_price=15),
        OrderItem(
            order=orders[6], item=items[0], quantity=400, unit_price=1200
        ),
        # Марья Моревна
        OrderItem(
            order=orders[7], item=items[3], quantity=400, unit_price=300
        ),
        OrderItem(order=orders[8], item=items[5], quantity=800, unit_price=15),
    ]

    session.add_all(order_items)
    session.commit()

    print("Sample data initialized successfully!")


if __name__ == "__main__":
    init_sample_data()
