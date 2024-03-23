import unittest
from unittest.mock import Mock, patch
from database.database_manager import (
    add_member,
    get_member_by_id,
    update_member,
    update_member_payment_status,
    delete_member,
)


class TestDatabaseManager(unittest.TestCase):
    @patch("database.database_manager.Session")
    @patch("database.database_manager.Member")
    def test_add_member(self, MockMember, MockSession):
        # Arrange
        mock_session = MockSession.return_value
        mock_member = MockMember.return_value
        name = "John Doe"
        phone_number = "1234567890"
        email = "john.doe@example.com"
        date_of_birth = "2000-01-01"
        monthly_payment_made = True

        # Act
        add_member(name, phone_number, email, date_of_birth, monthly_payment_made)

        # Assert
        MockMember.assert_called_once_with(
            name=name,
            phone_number=phone_number,
            email=email,
            date_of_birth=date_of_birth,
            monthly_payment_made=monthly_payment_made,
        )
        mock_session.add.assert_called_once_with(mock_member)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @patch("database.database_manager.Session")
    @patch("database.database_manager.Member")
    def test_get_member_by_id(self, MockMember, MockSession):
        # Arrange
        mock_session = MockSession.return_value
        mock_member = Mock()
        mock_member.id = 1
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_member
        )

        # Act
        result = get_member_by_id(1)

        # Assert
        MockSession.assert_called_once()
        mock_session.query.assert_called_once_with(MockMember)
        mock_session.query.return_value.filter.assert_called_once_with(
            MockMember.id == 1
        )
        mock_session.query.return_value.filter.return_value.first.assert_called_once()
        mock_session.close.assert_called_once()
        self.assertEqual(result, mock_member)

    @patch("database.database_manager.Session")
    @patch("database.database_manager.Member")
    def test_update_member_existing_member(self, MockMember, MockSession):
        # Arrange
        mock_session = MockSession.return_value
        mock_member = Mock()
        mock_member.name = "Old Name"
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_member
        )

        # Act
        update_member(1, name="New Name")

        # Assert
        MockSession.assert_called_once()
        mock_session.query.assert_called_once_with(MockMember)
        mock_session.query.return_value.filter.assert_called_once_with(
            MockMember.id == 1
        )
        mock_session.query.return_value.filter.return_value.first.assert_called_once()
        self.assertEqual(mock_member.name, "New Name")
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @patch("database.database_manager.Session")
    @patch("database.database_manager.Member")
    def test_update_member_non_existing_member(self, MockMember, MockSession):
        # Arrange
        mock_session = MockSession.return_value
        mock_session.query.return_value.filter.return_value.first.return_value = None

        # Act
        update_member(1, name="New Name")

        # Assert
        MockSession.assert_called_once()
        mock_session.query.assert_called_once_with(MockMember)
        mock_session.query.return_value.filter.assert_called_once_with(
            MockMember.id == 1
        )
        mock_session.query.return_value.filter.return_value.first.assert_called_once()
        mock_session.close.assert_called_once()

    @patch("database.database_manager.Session")
    @patch("database.database_manager.Member")
    def test_update_member_payment_status_member_exists(self, MockMember, MockSession):
        # Arrange
        mock_session = MockSession.return_value
        mock_member = Mock()
        mock_member.name = "Test Member"
        mock_member.monthly_payment_made = False
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_member
        )

        # Act
        update_member_payment_status(1, True)

        # Assert
        MockSession.assert_called_once()
        mock_session.query.assert_called_once_with(MockMember)
        mock_session.query.return_value.filter.assert_called_once_with(
            MockMember.id == 1
        )
        mock_session.query.return_value.filter.return_value.first.assert_called_once()
        self.assertEqual(mock_member.monthly_payment_made, True)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @patch("database.database_manager.Session")
    @patch("database.database_manager.Member")
    def test_update_member_payment_status_member_not_found(
        self, MockMember, MockSession
    ):
        # Arrange
        mock_session = MockSession.return_value
        mock_session.query.return_value.filter.return_value.first.return_value = None

        # Act
        update_member_payment_status(1, True)

        # Assert
        MockSession.assert_called_once()
        mock_session.query.assert_called_once_with(MockMember)
        mock_session.query.return_value.filter.assert_called_once_with(
            MockMember.id == 1
        )
        mock_session.query.return_value.filter.return_value.first.assert_called_once()
        mock_session.close.assert_called_once()

    @patch("database.database_manager.Session")
    @patch("database.database_manager.Member")
    def test_delete_member_existing(self, MockMember, MockSession):
        # Arrange
        mock_session = MockSession.return_value
        mock_member = Mock()
        mock_member.name = "Test Member"
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_member
        )

        # Act
        delete_member(1)

        # Assert
        MockSession.assert_called_once()
        mock_session.query.assert_called_once_with(MockMember)
        mock_session.query.return_value.filter.assert_called_once_with(
            MockMember.id == 1
        )
        mock_session.delete.assert_called_once_with(mock_member)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @patch("database.database_manager.Session")
    @patch("database.database_manager.Member")
    def test_delete_member_non_existing(self, MockMember, MockSession):
        # Arrange
        mock_session = MockSession.return_value
        mock_session.query.return_value.filter.return_value.first.return_value = None

        # Act
        delete_member(1)

        # Assert
        MockSession.assert_called_once()
        mock_session.query.assert_called_once_with(MockMember)
        mock_session.query.return_value.filter.assert_called_once_with(
            MockMember.id == 1
        )
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_session.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
# import unittest
# from datetime import date
# from database.models import engine, Base, Member
# from database.database_manager import (
#     add_member,
#     get_member_by_id,
#     update_member_payment_status,
#     delete_member,
#     update_member,
# )
# from sqlalchemy.orm import sessionmaker

# Session = sessionmaker(bind=engine)


# class TestDatabaseManager(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         # Create the schema in the database
#         Base.metadata.create_all(engine)

#     @classmethod
#     def tearDownClass(cls):
#         # Drop the schema after the tests run
#         Base.metadata.drop_all(engine)

#     def setUp(self):
#         # Create a new session for each test
#         self.session = Session()

#     def tearDown(self):
#         # Rollback and close the session after each test
#         self.session.rollback()
#         self.session.close()

#     def test_add_and_get_customer(self):
#         # Test adding a customer and retrieving them by ID
#         add_member("Test User", "555-5555", "test@example.com", date(1990, 1, 1), False)
#         member = get_member_by_id(1)
#         if member is not None:
#             self.assertEqual(member.name, "Test User")
#             self.assertEqual(member.phone_number, "555-5555")

#     def test_update_member(self):
#         # Test updating a customer's details
#         add_member(
#             "Test User 1", "555-5555", "test1@example.com", date(1990, 1, 1), False
#         )
#         update_member(
#             1, name="Updated Name", phone_number="555-5556", email="updated@example.com"
#         )
#         member = get_member_by_id(1)
#         if member is not None:
#             self.assertEqual(member.name, "Updated Name")
#             self.assertEqual(member.phone_number, "555-5556")
#             self.assertEqual(member.email, "updated@example.com")

#     def test_update_member_payment_status(self):
#         # Test updating a customer's payment status
#         add_member(
#             "Test User 2", "555-5556", "test2@example.com", date(1990, 1, 1), False
#         )
#         update_member_payment_status(1, True)
#         member = get_member_by_id(1)
#         if member is not None:
#             self.assertTrue(member.monthly_payment_made)

#     def test_delete_member(self):
#         # Test deleting a customer
#         add_member(
#             "Test User 3", "555-5557", "test3@example.com", date(1990, 1, 1), False
#         )
#         delete_member(1)
#         member = get_member_by_id(1)
#         self.assertIsNone(member)


# if __name__ == "__main__":
#     unittest.main()
