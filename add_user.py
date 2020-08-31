from images_query_interface import db, create_app, bcrypt
from images_query_interface.models import User
from images_query_interface.models import add_user_to_db
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Administrator add user')
    parser.add_argument('-u', '--username', type=str, required=True, help='Username')
    parser.add_argument('-e', '--email', type=str, required=True, help='Email id')
    parser.add_argument('-p', '--password', type=str, required=True, help='Password')

#    User.__table__.create(db.session.bind)

    args = parser.parse_args()

    username = args.username
    email = args.email
    password = args.password

    app = create_app()
    app.app_context().push()
    with app.app_context():
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        add_user_to_db(username, email, hashed_password)