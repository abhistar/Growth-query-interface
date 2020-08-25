from images_query_interface import db, create_app
from images_query_interface.models import User
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Administrator add user')
    parser.add_argument('-e', '--email', type=str, required=True, help='Email id')
    args = parser.parse_args()
    this_email = args.email

    app = create_app()
    app.app_context().push()
    with app.app_context():
        try :
            user = User.query.filter_by(email = this_email)[0]#returns a list thus taking the first and only element
            db.session.delete(user)
            db.session.commit()
            print(("User with username {} and email {} has been deleted").format(user.username, user.email))
        except IndexError:
            print("No user with the given mail")