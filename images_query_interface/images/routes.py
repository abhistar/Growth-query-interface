from flask import (render_template, url_for, flash, redirect,
                    request, send_file, Blueprint)
from flask_login import login_required, current_user
from images_query_interface import db
from images_query_interface.models import Image
from images_query_interface.forms import QueryForm
from images_query_interface.images.utils import request_form2dict_query, dict_query2list_images
from images_query_interface.common_utils import ( list_images2list_filepaths,
                                         dict_attributes, real_valued_attributes, form_attributes)
import time
import os
import io
import zipfile

images = Blueprint('images', __name__)

#page for form containing the fields to query
@images.route("/query")
@login_required
def query():
    form = QueryForm() 
    return render_template('request_query_db.html', form=form , title='Query')


#page for displaying the query results
@images.route("/display", methods=['POST'])
@login_required
def display():
    time_start = time.time()
    dict_query = request_form2dict_query(request.form)
    
    list_images = dict_query2list_images(dict_query)
    
    # TODO : run this part of code as seprate thread to reduce execution time of query
    # store the query in the user history
    if dict_query: #if dict_query is not empty
        if current_user.history is None:
            list_hist = []
        else:
            list_hist = eval(current_user.history)
            if len(list_hist) ==10:
                list_hist.pop(0)
        list_hist.append(dict_query)
        current_user.history = str(list_hist)
        db.session.commit()


    n_matches = len(list_images)

    list_filepaths = list_images2list_filepaths(list_images)
    #typecasting the list to string eg: str([0,1,2])->'[0,1,2]'
    str_list_filepaths = str(list_filepaths)
    #replacing / with * is a just a hack used because the /s cause issues when passed in the url
    str_list_filepaths = (str_list_filepaths).replace('/','*')
    
    time_end = time.time()
    execution_time = time_end-time_start

    return render_template('display_result.html', title='Results', dict_query=dict_query, form_attributes=form_attributes,
    list_attributes = dict_attributes.keys(), dict_attributes=dict_attributes, list_images = list_images,  
    str_list_filepaths = str_list_filepaths, execution_time=execution_time, n_matches=n_matches)


@images.route('/download_file/<string:filepath>', methods=['GET','POST'])
def download_file(filepath):
    filepath = filepath.replace('*','/')
    _, filename = os.path.split(filepath)
    # # try:
    # filepath = os.path.join('/home/adeem/Desktop/growth', filepath)
    if os.path.exists(filepath):    
        return send_file(filepath, as_attachment=True,
        attachment_filename=filename)
    else:
        return 'file not found'

@login_required
@images.route('/download_zip/<string:str_list_filepaths>', methods=['GET','POST'])
def download_zip(str_list_filepaths):
    str_list_filepaths =  str_list_filepaths.replace('*','/')
    
    #eval casts the list in string form back to list eg: eval('[0,1,2]')->[0,1,2]
    list_filepaths = eval(str_list_filepaths)

    #writes the files one by one to a zipfile
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for filepath in list_filepaths:
            _, filename = os.path.split(filepath)
            if os.path.exists(filepath): 
                z.write(filepath, filename)
    data.seek(0)

    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='data.zip'
    )