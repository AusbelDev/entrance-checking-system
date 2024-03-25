from deepface import DeepFace
from database.models import Session, engine
from database.models import Member, MemberEmbedding
from sqlalchemy import select


# Generates facial embeddings for all images in the database
def generate_all_embeddings():
    session = Session()

    # members = select(Member)
    members = session.query(Member).all()
    for member in members:
        if member.photo_path is not None:
            print(member.photo_path)
            photo_path = member.photo_path.split("_")
            print(photo_path)
            face = DeepFace.represent(
                img_path=f"/Users/ausbel/source/python/dl_projects/entrance-checking-system/{photo_path[0]}_ {photo_path[1]}",
                model_name="Facenet",
            )
            embedding = face[0]["embedding"]
            new_embedding = MemberEmbedding(
                member_id=member.id, embedding=str(embedding)
            )
            session.add(new_embedding)
    session.commit()
    session.close()
