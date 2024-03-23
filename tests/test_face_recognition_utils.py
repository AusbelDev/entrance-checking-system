import unittest
from unittest.mock import Mock, patch
from face_recognition.utils import generate_all_embeddings


class TestGenerateAllEmbeddings(unittest.TestCase):
    @patch("face_recognition.utils.Session")
    @patch("face_recognition.utils.Member")
    @patch("face_recognition.utils.DeepFace")
    @patch("face_recognition.utils.MemberEmbedding")
    def test_generate_all_embeddings(
        self, MockMemberEmbedding, MockDeepFace, MockMember, MockSession
    ):
        # Arrange
        mock_session = MockSession.return_value
        mock_member = Mock()
        mock_member.photo_path = "path_to_photo"
        mock_member.id = 1
        mock_session.query.return_value.all.return_value = [mock_member]

        mock_deepface = MockDeepFace.represent.return_value
        mock_deepface.__getitem__.return_value = {"embedding": "embedding"}

        # Act
        generate_all_embeddings()

        # Assert
        MockSession.assert_called_once()
        mock_session.query.assert_called_once_with(MockMember)
        mock_session.query.return_value.all.assert_called_once()
        MockDeepFace.represent.assert_called_once_with(
            str(mock_member.photo_path), model_name="Facenet"
        )
        MockMemberEmbedding.assert_called_once_with(
            member_id=mock_member.id, embedding=str(mock_deepface[0]["embedding"])
        )
        mock_session.add.assert_called_once_with(MockMemberEmbedding.return_value)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
