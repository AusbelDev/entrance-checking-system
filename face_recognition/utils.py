from deepface import DeepFace
from database.models import Session
from database.models import Member, MemberEmbedding


# Generates facial embeddings for all images in the database
def generate_all_embeddings():
    session = Session()
    members = session.query(Member).all()
    for member in members:
        if member.photo_path is not None:
            face = DeepFace.represent(str(member.photo_path), model_name="Facenet")
            embedding = face[0]["embedding"]
            new_embedding = MemberEmbedding(
                member_id=member.id, embedding=str(embedding)
            )
            session.add(new_embedding)
    session.commit()
    session.close()
