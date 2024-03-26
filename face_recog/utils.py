import os
from deepface import DeepFace
from database.models import Session
from database.models import Member, MemberEmbedding
from PIL import Image, ImageEnhance
import random
import cv2 as cv


# Generates facial embeddings for all images in the database
def generate_all_embeddings():
    session = Session()

    # members = select(Member)
    members = session.query(Member).all()
    for member in members:
        if member is not None:

            photo_path = member.photo_path.split("_")
            folder_path = os.path.dirname(__file__).replace("face_recog", "")

            face = DeepFace.represent(
                img_path=os.path.join(
                    folder_path,
                    f"{photo_path[0]}_ {photo_path[1]}",
                ),
                # img_path=f"../{photo_path[0]}_ {photo_path[1]}",
                model_name="Facenet",
            )
            embedding = face[0]["embedding"]
            new_embedding = MemberEmbedding(
                member_id=member.id, embedding=str(embedding)
            )
            session.add(new_embedding)
    session.commit()
    session.close()


def generate_embedding_for_member(member_id):
    session = Session()
    member = session.query(Member).filter(Member.id == member_id).first()
    if member is not None:
        photo_path = member.photo_path.split("_")
        folder_path = os.path.dirname(__file__).replace("face_recog", "")

        face = DeepFace.represent(
            img_path=os.path.join(
                folder_path,
                f"{photo_path[0]}_ {photo_path[1]}",
            ),
            model_name="Facenet",
        )
        embedding = face[0]["embedding"]
        new_embedding = MemberEmbedding(member_id=member.id, embedding=str(embedding))
        session.add(new_embedding)
        session.commit()
        session.close()


def check_embeddings():

    session = Session()
    member = session.query(Member).filter(Member.id == random.randint(1, 40)).first()

    session.close()
    if member is not None:
        photo_path = member.photo_path.split("_")
        folder_path = os.path.dirname(__file__).replace("face_recog", "")
        image_path = os.path.join(
            folder_path,
            f"{photo_path[0]}_ {photo_path[1]}",
        )
        image = Image.open(image_path)
        enhancer = ImageEnhance.Brightness(image)
        enhanced_im = enhancer.enhance(1.5)

        enhanced_im.save("test_img.jpg")
        output = DeepFace.verify(
            img1_path=os.path.join(
                folder_path,
                "test_img.jpg",
            ),
            img2_path=image_path,
            model_name="Facenet",
        )

        return output["verified"]
