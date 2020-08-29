from images_query_interface import db, create_app
from images_query_interface.models import add_dir_to_db
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add all processed files in folder to db')
    parser.add_argument('-d', '--dirpath', type=str, required=True, help='Path of directory containing images')

    args = parser.parse_args()

    dirpath = args.dirpath
    app = create_app()
    app.app_context().push()
    
    with app.app_context():
        add_dir_to_db(dirpath, append=False)