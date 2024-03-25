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
