# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import os
import uuid
import pymysql
from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session
from flask_ckeditor import CKEditor, upload_success, upload_fail
from flask_dropzone import Dropzone
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError

from forms import LoginForm, FortyTwoForm, NewPostForm, UploadForm, MultiUploadForm, SigninForm, \
    RegisterForm, SigninForm2, RegisterForm2, RichTextForm,WriteForm,RunForm,ResultForm,WatchForm
# from demos.form.forms import LoginForm,FortyTwoForm, NewPostForm, UploadForm, MultiUploadForm, SigninForm, \
#     RegisterForm, SigninForm2, RegisterForm2, RichTextForm

# from demos.form.common import OpenationDbInterface
from common import OpenationDbInterface,Run,RunTest
#db=OpenationDbInterface()
newrun=Run()


#res=db.select_data()
import time
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Custom config
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']

# Flask config
# set request body's max length
# app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024  # 3Mb

# Flask-CKEditor config
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload_for_ckeditor'

# Flask-Dropzone config
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image'
app.config['DROPZONE_MAX_FILE_SIZE'] = 3
app.config['DROPZONE_MAX_FILES'] = 30

ckeditor = CKEditor(app)
dropzone = Dropzone(app)


@app.route('/',methods=['GET', 'POST'])
def index_my():
    return render_template('myindex.html')

@app.route('/write',methods=['GET','POST'])
def write():
    form=WriteForm()
    if request.method=='POST':
        username = request.form.get('username')
        interface_name=request.form.get('interface_name')
        exe_mode=request.form.get('exe_mode')
        interface_url=request.form.get('interface_url')
        header=request.form.get('header')
        cookie=request.form.get('cookie')
        params=request.form.get('params')
        expect_params=request.form.get('expect_params')
        expect_params_value=request.form.get('expect_params_value')
        complete_params=request.form.get('complete_params')

        flash('提交成功 ')
        print("username: ",username)
        print("interface_name: ",interface_name)
        print("exe_mode:",exe_mode)
        print("interface_url: ",interface_url)
        print("header:",header)
        print("cookie: ",cookie)
        print("params: ",params)
        print("expect_params: ",expect_params)
        print("expect_params_value: ",expect_params_value)
        print("complete_params: ",complete_params)


        db1=OpenationDbInterface()
        db1.insert_value(username,interface_name,exe_mode,interface_url,header,cookie,params,expect_params,expect_params_value,complete_params)
        # for i in range(len(res)):
        #     print(res[i])
        # db.insert_value(username,interface_url)

        return redirect(url_for('write'))
    return render_template('write.html')

@app.route('/run',methods=['GET', 'POST'])
def run():
    form=RunForm()
    if request.method=='POST':
        username=request.form.get('username')
        #number=request.form.get('number')
        #newrun.myrun(username)
        RunMain=RunTest(username)
        RunMain.go_to_run()

        #print("要执行的用户是：",username)
        print("要执行的用户名称是：", username)
        # 这里使用username作为限定条件，执行sql查询
        db = OpenationDbInterface()
        sql = "select * from interface_result where username = '"+username+"'" +" ORDER BY id DESC LIMIT 0,20"
        interfaces = db.select_data(sql)
        # redirect(url_for('write'))
        #time.sleep(5)
        return render_template('result.html', interfaces=interfaces)  #点击之后跳转到结果页面就行了


        #return redirect(url_for('check'))
    return render_template('run.html')
#
# @app.route('/check_select',methods=['GET', 'POST'])
# def check_select():  #查看
#     pass

# @app.route('/result')
# def result(username):
#     #interfaces=res
#     print("这是结果页面，出入的名称是：",username)
#     db2=OpenationDbInterface()
#     #res=db2.select_data()
#     sql = "select * from interface_test where id ='1' "
#     interfaces = db2.select_data(sql)
#     print(interfaces)
#     return render_template('result.html',interfaces=interfaces)

@app.route('/result_select',methods=['GET', 'POST'])  #查询结果
def result_select():
    form=RunForm()
    if request.method=='POST':
        username = request.form.get('username')
        print("要查询的名称是：", username)
        number=request.form.get('number')
        #number=int(number)
        #这里使用username作为限定条件，执行sql查询
        db=OpenationDbInterface()
        sql = "select * from interface_result where username = '"+username+"'"+" ORDER BY id DESC LIMIT 0,"+number
        print("sql:",sql)
        interfaces=db.select_data(sql)
        #redirect(url_for('write'))
        #time.sleep(5)
        return render_template('result.html',interfaces=interfaces)

    return render_template('result_select.html')

@app.route('/check',methods=['GET', 'POST'])   #查看用例
def check():
    form=WatchForm()   #公用一个表单，只是要选择用例所有者
    if request.method=='POST':
        username=request.form.get('username')
        print("要查询的用例所有者名称是：",username)
        db4=OpenationDbInterface()
        sql="select * from interface_test where username = '"+username+"'"
        interfaces=db4.select_data(sql)
        print("===============interfaces===================\n")
        print(interfaces)


        return render_template('check_all.html',interfaces=interfaces)
    return render_template('watch_select.html')
    #interfaces=db.select_data()
    # db3=OpenationDbInterface()
    # interfaces=db3.select_data()
    # print(interfaces)
    # # for interface in interfaces:
    # #     print(interface['id'])
    # #     print("xxxxxxxxxxxxxxxxx")
    # return render_template('check_all.html', interfaces=interfaces)
    # #pass

# @app.route('/check')   #查看用例
# def check():
#     #interfaces=db.select_data()
#     db3=OpenationDbInterface()
#     interfaces=db3.select_data()
#     print(interfaces)
#     # for interface in interfaces:
#     #     print(interface['id'])
#     #     print("xxxxxxxxxxxxxxxxx")
#     return render_template('check_all.html', interfaces=interfaces)
#     #pass


@app.route('/1', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/html', methods=['GET', 'POST'])
def html():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        #flash('Welcome home, %s!' % username)
        password=request.form.get('password')
        flash('Welcom home ,%s ,your password is %s '%(username,password))
        return redirect(url_for('index'))
    return render_template('pure_html.html')


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        print("xxxxxxxxxxxxxxxxxxxxx")
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    return render_template('basic.html', form=form)


@app.route('/bootstrap', methods=['GET', 'POST'])
def bootstrap():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    return render_template('bootstrap.html', form=form)


@app.route('/custom-validator', methods=['GET', 'POST'])
def custom_validator():
    form = FortyTwoForm()
    if form.validate_on_submit():
        flash('Bingo!')
        return redirect(url_for('index'))
    return render_template('custom_validator.html', form=form)


@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success.')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)


@app.route('/multi-upload', methods=['GET', 'POST'])
def multi_upload():
    form = MultiUploadForm()

    if request.method == 'POST':
        filenames = []

        # check csrf token
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error.')
            return redirect(url_for('multi_upload'))

        # check if the post request has the file part
        if 'photo' not in request.files:
            flash('This field is required.')
            return redirect(url_for('multi_upload'))

        for f in request.files.getlist('photo'):
            # if user does not select file, browser also
            # submit a empty part without filename
            # if f.filename == '':
            #     flash('No selected file.')
            #    return redirect(url_for('multi_upload'))
            # check the file extension
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(os.path.join(
                    app.config['UPLOAD_PATH'], filename
                ))
                filenames.append(filename)
            else:
                flash('Invalid file type.')
                return redirect(url_for('multi_upload'))
        flash('Upload success.')
        session['filenames'] = filenames
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)


@app.route('/dropzone-upload', methods=['GET', 'POST'])
def dropzone_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'This field is required.', 400
        f = request.files.get('file')

        if f and allowed_file(f.filename):
            filename = random_filename(f.filename)
            f.save(os.path.join(
                app.config['UPLOAD_PATH'], filename
            ))
        else:
            return 'Invalid file type.', 400
    return render_template('dropzone.html')


@app.route('/two-submits', methods=['GET', 'POST'])
def two_submits():
    form = NewPostForm()
    if form.validate_on_submit():
        if form.save.data:
            # save it...
            flash('You click the "Save" button.')
        elif form.publish.data:
            # publish it...
            flash('You click the "Publish" button.')
        return redirect(url_for('index'))
    return render_template('2submit.html', form=form)


@app.route('/multi-form', methods=['GET', 'POST'])
def multi_form():
    signin_form = SigninForm()
    register_form = RegisterForm()

    if signin_form.submit1.data and signin_form.validate():
        username = signin_form.username.data
        flash('%s, you just submit the Signin Form.' % username)
        return redirect(url_for('index'))

    if register_form.submit2.data and register_form.validate():
        username = register_form.username.data
        flash('%s, you just submit the Register Form.' % username)
        return redirect(url_for('index'))

    return render_template('2form.html', signin_form=signin_form, register_form=register_form)


@app.route('/multi-form-multi-view')
def multi_form_multi_view():
    signin_form = SigninForm2()
    register_form = RegisterForm2()
    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)


@app.route('/handle-signin', methods=['POST'])
def handle_signin():
    signin_form = SigninForm2()
    register_form = RegisterForm2()

    if signin_form.validate_on_submit():
        username = signin_form.username.data
        flash('%s, you just submit the Signin Form.' % username)
        return redirect(url_for('index'))

    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)


@app.route('/handle-register', methods=['POST'])
def handle_register():
    signin_form = SigninForm2()
    register_form = RegisterForm2()

    if register_form.validate_on_submit():
        username = register_form.username.data
        flash('%s, you just submit the Register Form.' % username)
        return redirect(url_for('index'))
    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)


@app.route('/ckeditor', methods=['GET', 'POST'])
def integrate_ckeditor():
    form = RichTextForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        flash('Your post is published!')
        return render_template('post.html', title=title, body=body)
    return render_template('ckeditor.html', form=form)


# handle image upload for ckeditor
@app.route('/upload-ck', methods=['POST'])
def upload_for_ckeditor():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('Image only!')
    f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
    url = url_for('get_file', filename=f.filename)
    return upload_success(url, f.filename)
