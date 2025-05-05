from app import create_app, db
from app.models import Users, Profile, Favourite
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("Dropping and recreating all tables...")
    db.drop_all()
    db.create_all()

    print("Adding test users...")

    user1 = Users(
        username="alice",
        password=generate_password_hash("alice123"),
        name="Alice Smith",
        email="alice@example.com",
        photo="alice.jpg"
    )
    user2 = Users(
        username="bob",
        password=generate_password_hash("bob123"),
        name="Bob Johnson",
        email="bob@example.com",
        photo="bob.jpg"
    )

    db.session.add_all([user1, user2])
    db.session.commit()

    print("Adding profiles...")

    profile1 = Profile(
        user_id_fk=user1.id,
        description="Outdoor enthusiast",
        parish="Kingston",
        biography="I love hiking and adventures.",
        sex="Female",
        race="Black",
        birth_year=1995,
        height=5.7,
        fav_cuisine="Italian",
        fav_color="Blue",
        fav_school_subject="Math",
        political=True,
        religion="Christian",
        family_oriented=True
    )

    profile2 = Profile(
        user_id_fk=user2.id,
        description="Music lover and gamer",
        parish="St. Andrew",
        biography="Chill vibes and jazz playlists.",
        sex="Male",
        race="Mixed",
        birth_year=1993,
        height=6.0,
        fav_cuisine="Jamaican",
        fav_color="Green",
        fav_school_subject="Music",
        political=False,
        religion="None",
        family_oriented=False
    )

    db.session.add_all([profile1, profile2])
    db.session.commit()

    print("Adding a favourite...")

    fav1 = Favourite(
        user_id_fk=user1.id,
        fav_user_id_fk=user2.id
    )

    db.session.add(fav1)
    db.session.commit()

    print("Test data added successfully!")
