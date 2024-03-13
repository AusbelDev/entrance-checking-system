from models import Customer, Session


def add_customer(name, phone_number, email, date_of_birth, monthly_payment_made):
    """
    Adds a new customer to the database.
    """
    session = Session()
    new_customer = Customer(
        name=name,
        phone_number=phone_number,
        email=email,
        date_of_birth=date_of_birth,
        monthly_payment_made=monthly_payment_made,
    )
    session.add(new_customer)
    session.commit()
    print(f"Added new customer: {name}")
    session.close()


def get_customer_by_id(customer_id):
    """
    Retrieves a customer by their ID.
    """
    session = Session()
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    session.close()
    return customer


def update_customer_payment_status(customer_id, new_status):
    """
    Updates the payment status of a customer.
    """
    session = Session()
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer:
        customer.monthly_payment_made = new_status
        session.commit()
        print(f"Updated payment status for {customer.name} to {new_status}.")
    else:
        print("Customer not found.")
    session.close()


def delete_customer(customer_id):
    """
    Deletes a customer from the database.
    """
    session = Session()
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer:
        session.delete(customer)
        session.commit()
        print(f"Deleted customer: {customer.name}")
    else:
        print("Customer not found.")
    session.close()
