from models import Member, Session


def add_member(name, phone_number, email, date_of_birth, monthly_payment_made):
    """
    Adds a new member to the database.
    """
    session = Session()
    new_member = Member(
        name=name,
        phone_number=phone_number,
        email=email,
        date_of_birth=date_of_birth,
        monthly_payment_made=monthly_payment_made,
    )
    session.add(new_member)
    session.commit()
    print(f"Added new member: {name}")
    session.close()


def get_member_by_id(member_id):
    """
    Retrieves a member by their ID.
    """
    session = Session()
    member = session.query(Member).filter(Member.id == member_id).first()
    session.close()
    return member


def update_member(id, **kwargs):
    session = Session()
    member = session.query(Member).filter(Member.id == id).first()
    if member:
        for key, value in kwargs.items():
            setattr(member, key, value)
        session.commit()
        print(f"Updated member: {member.name}")
    else:
        print("member not found.")
    session.close()


def update_member_payment_status(member_id, new_status):
    """
    Updates the payment status of a member.
    """
    session = Session()
    member = session.query(Member).filter(Member.id == member_id).first()
    if member:
        member.monthly_payment_made = new_status
        session.commit()
        print(f"Updated payment status for {member.name} to {new_status}.")
    else:
        print("member not found.")
    session.close()


def delete_member(member_id):
    """
    Deletes a member from the database.
    """
    session = Session()
    member = session.query(Member).filter(Member.id == member_id).first()
    if member:
        session.delete(member)
        session.commit()
        print(f"Deleted member: {member.name}")
    else:
        print("member not found.")
    session.close()
