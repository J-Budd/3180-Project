"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import jwt
from app import app
from flask import render_template, request, jsonify, send_file, send_from_directory, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, Users, Profile, Favourite
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime
from sqlalchemy import func
import os


###
# Routing for your application.
###


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# API Routes
###

@app.route('/api/register', methods=['POST'])
def api_register():
    """Register a new user with optional profile image."""
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    email = request.form.get('email')
    profile = request.files.get('profile')  # This is the uploaded file

    if not username or not password or not name or not email:
        return jsonify({"error": "All fields are required"}), 400

    # Check for duplicates
    if Users.query.filter_by(username=username).first() or Users.query.filter_by(email=email).first():
        return jsonify({"error": "Username or email already exists"}), 400

    # Handle file saving
    profile_filename = None
    if profile:
        filename = secure_filename(profile.filename)
        profile_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        profile.save(profile_path)
        profile_filename = filename  # You can store this in the DB if needed

    # Create user
    hashed_password = generate_password_hash(password)
    new_user = Users(
        username=username,
        password=hashed_password,
        name=name,
        email=email,
        photo=profile_filename  # Only if your model has this field
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """Log in a user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Find user by username
    user = Users.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Log in the user
    login_user(user)
    #check if user has a complete profile as they cannot make certain requests without it
    profile = Profile.query.filter_by(user_id_fk=user.id).first()
    has_profile = False
    if profile:
        #We will list the required field to check for profile completeness
        required_fields = [
            profile.description,
            profile.parish,
            profile.biography,
            profile.sex,
            profile.race,
            profile.birth_year,
            profile.height,
            profile.fav_cuisine,
            profile.fav_color,
            profile.fav_school_subject,
            profile.political,
            profile.religion,
            profile.family_oriented
        ]
        #if none of the required fields is none or empty, then the profile is complete
        has_profile = all(field is not None and field != "" for field in required_fields)
    token = jwt.encode({"user_id": user.id}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"message": "Logged in successfully",
                    "has_profile": has_profile,
                    "user_id": user.id, #optional, but useful for the frontend to know the user id
                    "token": token
                    }), 200


@app.route('/api/auth/logout', methods=['POST'])
@login_required
def api_logout():
    """Log out the current user."""
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


@app.route('/api/profiles', methods=['GET'])
@login_required
def get_profiles():
    """Return all profiles or a limited number of the most recent ones."""
    limit = request.args.get('limit', type=int)

    query = Profile.query.order_by(Profile.id.desc())  # show most recent first

    if limit:
        profiles = query.limit(limit).all()
    else:
        profiles = query.all()

    return jsonify([{
        "id": profile.id,
        "user_id": profile.user_id_fk,
        "name": profile.user.name,  # <-- assuming a relationship to Users exists
        "description": profile.description,
        "parish": profile.parish,
        "photo": profile.user.photo,  # Access the user's photo here # <-- assuming a relationship to Users exists
        "biography": profile.biography,
        "sex": profile.sex,
        "race": profile.race,
        "birth_year": profile.birth_year,
        "height": profile.height,
        "fav_cuisine": profile.fav_cuisine,
        "fav_color": profile.fav_color,
        "fav_school_subject": profile.fav_school_subject,
        "political": profile.political,
        "religion": profile.religion,
        "family_oriented": profile.family_oriented
    } for profile in profiles]), 200


@app.route('/api/profiles', methods=['POST'])
@login_required
def add_profile():
    """Add a new profile."""
    if not current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    required_fields = ["description", "parish", "biography", "sex", "race", "birth_year", "height", "fav_cuisine", "fav_color", "fav_school_subject", "political", "religion", "family_oriented"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400
    
    # Check if user already has 3 profiles
    if Profile.query.filter_by(user_id_fk=current_user.id).count() >= 3:
        return jsonify({'error': 'You can only have up to 3 profiles'}), 400

    new_profile = Profile(
        user_id_fk=current_user.id,
        description=data["description"],
        parish=data["parish"],
        biography=data["biography"],
        sex=data["sex"],
        race=data["race"],
        birth_year=data["birth_year"],
        height=data["height"],
        fav_cuisine=data["fav_cuisine"],
        fav_color=data["fav_color"],
        fav_school_subject=data["fav_school_subject"],
        political=data["political"],
        religion=data["religion"],
        family_oriented=data["family_oriented"]
    )

    db.session.add(new_profile)
    db.session.commit()
    return jsonify({"message": "Profile added successfully"}), 201


@app.route('/api/profiles/<int:profile_id>', methods=['GET'])
@login_required
def get_profile_details(profile_id):
    """Get details of a specific profile."""
    profile = Profile.query.get(profile_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify({
        "id": profile.id,
        "user_id": profile.user_id_fk,
        "description": profile.description,
        "parish": profile.parish,
        "photo": profile.user.photo,
        "biography": profile.biography,
        "sex": profile.sex,
        "race": profile.race,
        "birth_year": profile.birth_year,
        "height": profile.height,
        "fav_cuisine": profile.fav_cuisine,
        "fav_color": profile.fav_color,
        "fav_school_subject": profile.fav_school_subject,
        "political": profile.political,
        "religion": profile.religion,
        "family_oriented": profile.family_oriented
    }), 200


@app.route('/api/profiles/<int:user_id>/favourite', methods=['POST'])
@login_required
def add_to_favourites(user_id):
    """Add a user to favourites."""
    if user_id == current_user.id:
        return jsonify({"error": "You cannot favourite yourself"}), 400

    favourite = Favourite(user_id_fk=current_user.id, fav_user_id_fk=user_id)
    db.session.add(favourite)
    db.session.commit()
    return jsonify({"message": "User added to favourites"}), 201


@app.route('/api/profiles/matches/<int:profile_id>', methods=['GET'])
@login_required
def get_matches(profile_id):
    """Get a list of profiles that match specific criteria."""
    profile = Profile.query.get(profile_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    matches = Profile.query.filter(
        Profile.sex == profile.sex,
        Profile.race == profile.race,
        Profile.parish == profile.parish,
        Profile.id != profile.id
    ).all()

    return jsonify([{
        "id": match.id,
        "user_id": match.user_id_fk,
        "description": match.description,
        "parish": match.parish,
        "biography": match.biography,
        "sex": match.sex,
        "race": match.race,
        "birth_year": match.birth_year,
        "height": match.height,
        "fav_cuisine": match.fav_cuisine,
        "fav_color": match.fav_color,
        "fav_school_subject": match.fav_school_subject,
        "political": match.political,
        "religion": match.religion,
        "family_oriented": match.family_oriented
    } for match in matches]), 200


@app.route('/api/search', methods=['GET'])
@login_required
def search_profiles():
    """Search for profiles by name, birth year, sex, or race."""
    name = request.args.get('name')
    birth_year = request.args.get('birth_year')
    sex = request.args.get('sex')
    race = request.args.get('race')

    query = Profile.query.filter(Profile.user_id_fk != current_user.id)
    if name:
        query = query.filter(Profile.biography.ilike(f"%{name}%"))
    if birth_year:
        query = query.filter(Profile.birth_year == birth_year)
    if sex:
        query = query.filter(Profile.sex == sex)
    if race:
        query = query.filter(Profile.race == race)

    results = query.all()
    return jsonify([{
        "id": result.id,
        "user_id": result.user_id_fk,
        "description": result.description,
        "parish": result.parish,
        "biography": result.biography,
        "sex": result.sex,
        "race": result.race,
        "birth_year": result.birth_year,
        "height": result.height,
        "fav_cuisine": result.fav_cuisine,
        "fav_color": result.fav_color,
        "fav_school_subject": result.fav_school_subject,
        "political": result.political,
        "religion": result.religion,
        "family_oriented": result.family_oriented
    } for result in results]), 200


@app.route('/api/users/<int:user_id>', methods=['GET'])
@login_required
def get_user_details(user_id):
    """Get details of a user."""
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    profiles = Profile.query.filter_by(user_id_fk=user.id).all()

    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "photo": user.photo,
            "date_joined": user.date_joined.isoformat()
        },
        "profiles": [
            {
                "id": p.id,
                "description": p.description,
                "parish": p.parish,
                "sex": p.sex,
                "race": p.race,
                "biography": p.biography,
                "birth_year": p.birth_year,
                "height": p.height,
                "fav_cuisine": p.fav_cuisine,
                "fav_color": p.fav_color,
                "fav_school_subject": p.fav_school_subject,
                "political": p.political,
                "religion": p.religion,
                "family_oriented": p.family_oriented
            } for p in profiles
        ]
    }), 200


@app.route('/api/users/<int:user_id>/favourites', methods=['GET'])
@login_required
def get_user_favourites(user_id):
    """Get users that a user has favoured."""
    favourites = Favourite.query.filter_by(user_id_fk=user_id).all()
    return jsonify([{
        "id": favourite.id,
        "fav_user_id": favourite.fav_user_id_fk
    } for favourite in favourites]), 200


@app.route('/api/users/favourites/<int:N>', methods=['GET'])
@login_required
def get_top_favoured_users(N):
    """Get the top N favoured users."""
    top_users = db.session.query(
        Favourite.fav_user_id_fk,
        func.count(Favourite.fav_user_id_fk).label('fav_count')
    ).group_by(Favourite.fav_user_id_fk).order_by(func.count(Favourite.fav_user_id_fk).desc()).limit(N).all()

    return jsonify([{
        "user_id": user[0],
        "fav_count": user[1]
    } for user in top_users]), 200


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404