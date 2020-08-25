from images_query_interface import create_app
from images_query_interface.models import User


if __name__ == '__main__':
    
    app = create_app()
    app.app_context().push()
    with app.app_context():
        list_users = User.query.all()
        print( ("Total {} user(s)").format(len(list_users)) )
        for user in list_users:
            print(user.username, user.email)