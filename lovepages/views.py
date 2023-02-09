from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for
from flask_login import login_required, current_user
from .models import User, Note, Page, User_Page, Widget
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return render_template("welcome.html", user=current_user)

    return render_template("home.html", user=current_user)

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if not current_user.is_authenticated:
        return render_template("login.html", user=current_user)

    if request.method == 'POST': 
        data = request.get_json()
        background_color = data['background_color']
        primary_color = data['primary_color']
        secondary_color =  data['secondary_color']
        text_color =  data['text_color']
        text_font =  data['text_font']

        user = User.query.filter_by(id=current_user.id).first()
        user.background_color = background_color
        user.primary_color = primary_color
        user.secondary_color = secondary_color
        user.text_color = text_color
        user.text_font = text_font
        db.session.commit()

        return redirect('/settings')

    return render_template("settings.html", user=current_user)

@views.route('/new_page', methods=['GET', 'POST'])
@login_required
def new_page():
    if request.method == 'POST': 
        title = request.form.get('title')
        sub_title = request.form.get('sub_title')
        icon_link = request.form.get('icon_link')

        if len(title) < 1:
            flash('Title is too short!', category='error') 
        else:
            new_page = Page(title=title, sub_title=sub_title, icon_link=icon_link, create_user_id=current_user.id)  
            db.session.add(new_page)
            db.session.commit()

            add_page_to_user = User_Page(page_id=new_page.id, user_id=current_user.id)  
            db.session.add(add_page_to_user)
            db.session.commit()

            page_url = '/page/' + str(new_page.id)

            return redirect(page_url)

    return render_template("new_page.html", user=current_user)

@views.route('/page/<id>', methods=['GET', 'POST'])
@login_required
def page(id):
    page = Page.query.filter_by(id=id).first()
    widgets = []
    for w in page.widgets:
        widgets.append(w.as_dict()) 

    return render_template("page.html", user=current_user, page=page, widgets=json.dumps(widgets))

@views.route('/page/<id>/add_widget', methods=['GET', 'POST'])
@login_required
def add_widget(id):
    if request.method == 'POST': 
        page_id = id
        type = request.form.get('type')
        width = request.form.get('width')
        index = -1
        if type == 'image':
            content = request.form.get('link')
            new_widget = Widget(page_id=page_id, type=type, width=width, index=index, content=content, create_user_id=current_user.id)  
            db.session.add(new_widget)
            db.session.commit()
        elif type == 'text':
            content = request.form.get('text')
            font_color = request.form.get('font_color')
            font_size = request.form.get('font_size')
            font_family = request.form.get('font_family')
            new_widget = Widget(page_id=page_id, type=type, width=width, index=index, content=content, font_color=font_color, font_size=font_size, font_family=font_family, create_user_id=current_user.id) 
            db.session.add(new_widget)
            db.session.commit()

        page_url = '/page/' + str(id) + '/edit'
        return redirect(page_url)
    
    return render_template("add_widget.html", user=current_user, page_id=id)


@views.route('/page/<id>/share', methods=['GET','POST'])
@login_required
def share_page(id):
    page = Page.query.filter_by(id=id).first()
    if request.method == 'POST': 
        share_with = request.form.get('user_name')

        check_user = User.query.filter_by(user_name=share_with).first()
        if check_user:
            check_shareable = User_Page.query.filter_by(user_id=check_user.id, page_id=id).first()

            if check_shareable:
                flash('This page has already been shared with this user!', category="error")
            else:
                add_user_to_page = User_Page(user_id=check_user.id, page_id=id, create_user_id=current_user.id)  
                db.session.add(add_user_to_page)
                db.session.commit()
        else:
            flash('A user with this username does not exist :(', category="error")
            return render_template("share_page.html", user=current_user, page=page)
        
        result = {'success': True}
        return jsonify(result)
    else:
        return render_template("share_page.html", user=current_user, page=page)


@views.route('/page/<id>/edit', methods=['GET','POST'])
@login_required
def edit_page(id):
    if request.method == 'POST': 
        data = request.get_json()
        title = data['title']
        sub_title =  data['sub_title']
        widgets =  data['widgets']

        page = Page.query.filter_by(id=id).first()
        page.title = title
        page.sub_title = sub_title
        db.session.commit()

        for widget in widgets:
            w = Widget.query.filter_by(id=widget['id']).first()
            w.posx = widget['posx']
            w.posy = widget['posy']
            w.width = widget['width']
           
            db.session.commit()
        
        result = {'success': True, 'id': str(id)}
        return jsonify(result)
    else:
        page = Page.query.filter_by(id=id).first()
        widgets = []
        for w in page.widgets:
            widgets.append(w.as_dict()) 

        return render_template("edit_page.html", user=current_user, page=page, widgets=json.dumps(widgets))
