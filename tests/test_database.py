import unittest
from datetime import date
from database.models import engine, Base, Member
from database.database_manager import (
    add_member,
    get_member_by_id,
    update_member_payment_status,
    delete_member,
    update_member,
)
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)


class TestDatabaseManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create the schema in the database
        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        # Drop the schema after the tests run
        Base.metadata.drop_all(engine)

    def setUp(self):
        # Create a new session for each test
        self.session = Session()

    def tearDown(self):
        # Rollback and close the session after each test
        self.session.rollback()
        self.session.close()

    def test_add_and_get_customer(self):
        # Test adding a customer and retrieving them by ID
        add_member("Test User", "555-5555", "test@example.com", date(1990, 1, 1), False)
        member = get_member_by_id(1)
        if member is not None:
            self.assertEqual(member.name, "Test User")
            self.assertEqual(member.phone_number, "555-5555")

    def test_update_member(self):
        # Test updating a customer's details
        add_member(
            "Test User 1", "555-5555", "test1@example.com", date(1990, 1, 1), False
        )
        update_member(
            1, name="Updated Name", phone_number="555-5556", email="updated@example.com"
        )
        member = get_member_by_id(1)
        if member is not None:
            self.assertEqual(member.name, "Updated Name")
            self.assertEqual(member.phone_number, "555-5556")
            self.assertEqual(member.email, "updated@example.com")

    def test_update_member_payment_status(self):
        # Test updating a customer's payment status
        add_member(
            "Test User 2", "555-5556", "test2@example.com", date(1990, 1, 1), False
        )
        update_member_payment_status(1, True)
        member = get_member_by_id(1)
        if member is not None:
            self.assertTrue(member.monthly_payment_made)

    def test_delete_member(self):
        # Test deleting a customer
        add_member(
            "Test User 3", "555-5557", "test3@example.com", date(1990, 1, 1), False
        )
        delete_member(1)
        member = get_member_by_id(1)
        self.assertIsNone(member)


if __name__ == "__main__":
    unittest.main()
