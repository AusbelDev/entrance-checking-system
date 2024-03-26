import unittest
from unittest.mock import Mock, patch, MagicMock
from face_recog.utils import (
    generate_all_embeddings,
    check_embeddings,
    generate_embedding_for_member,
)


class TestFaceRecognitionUtils(unittest.TestCase):
    @patch("face_recog.utils.Session")
    @patch("deepface.DeepFace.represent")
    @patch("os.path.join")
    @patch("os.path.dirname")
    def test_generate_all_embeddings(
        self, mock_dirname, mock_join, mock_represent, mock_session
    ):
        # Mock the os.path.dirname to return a specific directory
        mock_dirname.return_value = "/fake_dir"

        # Mock os.path.join to return a fake file path
        mock_join.side_effect = lambda *args: "/".join(args)

        # Setup a mock Member and MemberEmbedding
        member_mock = MagicMock(photo_path="fake_path_1")
        new_embedding_mock = MagicMock()

        # Mock the database session, members query, and the add and commit operations
        session_mock = mock_session.return_value
        session_mock.query.return_value.all.return_value = [
            member_mock
        ]  # Return a list with one mock member

        # Mock DeepFace.represent to return a specific output
        mock_represent.return_value = [{"embedding": "fake_embedding"}]

        # Call the function under test
        generate_all_embeddings()

        # Assertions to ensure the function behaves as expected
        session_mock.add.assert_called_once()
        session_mock.commit.assert_called_once()

        # Check if DeepFace.represent was called with expected arguments
        mock_represent.assert_called_once_with(
            img_path="/fake_dir/fake_ path",
            model_name="Facenet",
        )

    @patch("face_recog.utils.Session")
    @patch("deepface.DeepFace.represent")
    @patch("os.path.join")
    @patch("os.path.dirname")
    def test_generate_embedding(
        self, mock_dirname, mock_join, mock_represent, mock_session
    ):
        # Mock the os.path.dirname to return a specific directory
        mock_dirname.return_value = "/fake_dir"

        # Mock os.path.join to return a fake file path
        mock_join.side_effect = lambda *args: "/".join(args)

        # Setup a mock Member and MemberEmbedding
        member_mock = MagicMock(id=1, photo_path="fake_path_1")
        new_embedding_mock = MagicMock()

        # Mock the database session, members query, and the add and commit operations
        session_mock = mock_session.return_value
        session_mock.query.return_value.filter.return_value.first.return_value = (
            member_mock
        )

        # Mock DeepFace.represent to return a specific output
        mock_represent.return_value = [{"embedding": "fake_embedding"}]

        # Call the function under test
        generate_embedding_for_member(1)

        # Assertions to ensure the function behaves as expected
        session_mock.add.assert_called_once()
        session_mock.commit.assert_called_once()

        # Check if DeepFace.represent was called with expected arguments
        mock_represent.assert_called_once_with(
            img_path="/fake_dir/fake_ path",
            model_name="Facenet",
        )

    @patch("face_recog.utils.Session")
    @patch("deepface.DeepFace.verify")
    @patch("PIL.Image.open")
    @patch("PIL.ImageEnhance.Brightness")
    @patch("os.path.join")
    @patch("os.path.dirname")
    def test_check_embeddings(
        self,
        mock_dirname,
        mock_join,
        mock_brightness,
        mock_open,
        mock_verify,
        mock_session,
    ):
        # Mock the os.path.dirname to return a specific directory
        mock_dirname.return_value = "/fake_dir"

        # Mock os.path.join to return a fake file path
        mock_join.side_effect = lambda *args: "/".join(args)

        # Mock the database session and member retrieval
        mock_session.return_value.query.return_value.filter.return_value.first.return_value = MagicMock(
            photo_path="fake_path_1"
        )

        # Mock Image.open to return a mock image object
        mock_image = MagicMock()
        mock_open.return_value = mock_image

        # Mock ImageEnhance.Brightness to return a mock enhancer which returns a mock image
        mock_enhancer = MagicMock()
        mock_enhancer.enhance.return_value = mock_image
        mock_brightness.return_value = mock_enhancer

        # Mock DeepFace.verify to return a specific output
        mock_verify.return_value = {"verified": True}

        # Call the function under test
        result = check_embeddings()

        # Assertions to check if the function behaves as expected
        self.assertTrue(result)
        mock_session.assert_called_once()
        mock_verify.assert_called_once_with(
            img1_path="/fake_dir/test_img.jpg",
            img2_path="/fake_dir/fake_ path",
            model_name="Facenet",
        )
        mock_image.save.assert_called_once_with("test_img.jpg")
