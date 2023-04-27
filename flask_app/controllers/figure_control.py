from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.figure_model import ActionFigure
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'flask_app/static/figure_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/figureitout/newfigure")
def new_figure():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template("new_figure.html", user=User.get_by_id(data))


@app.route("/figureitout/create", methods=['POST'])
def create_figure():
    if 'user_id' not in session:
        return redirect('/logout')
    
    
    if not ActionFigure.validate_figure(request.form):
        return redirect('/figureitout/newfigure')    
    # check if the post request has the file part
    print(request.files)
    if 'image' not in request.files:
        flash('No file part')
        print('********')
        return redirect(request.url)
    image = request.files['image']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if image.filename == '':
        flash('No selected file')
        return redirect(request.url)
    data = {
        "figure_name":request.form["figure_name"],
        "brand":request.form["brand"],
        "line":request.form["line"],
        "price":request.form["price"],
        "description":request.form["description"],
        "image":request.files["image"],
        "user_id":session["user_id"]
    }
    ActionFigure.save(data)
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect('/dashboard')


@app.route("/figureitout/edit/<int:id>")
def edit_figure(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_figure.html", edit=ActionFigure.get_one(data), user=User.get_by_id(user_data))


@app.route("/figureitout/update", methods=['POST'])
def update_figure():
    if 'user_id' not in session:
        return redirect('/logout')
    if not ActionFigure.validate_figure(request.form):
        return redirect('/figureitout/newfigure')
    data = {
        "figure_name":request.form["figure_name"],
        "brand":request.form["brand"],
        "line":request.form["line"],
        "price":request.form["price"],
        "description":request.form["description"],
        "image": request.form["image"],
        "id":request.files['id'],
        "user_id":session["user_id"]
    }
    ActionFigure.update(data)
    return redirect('/dashboard')


@app.route("/figureitout/view/<int:id>")
def view_figure(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("view_figure.html", figures_table=ActionFigure.get_specific_figure(data), user=User.get_by_id(user_data))


@app.route("/figureitout/delete/<int:id>")
def delete_figure(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    ActionFigure.destroy(data)
    return redirect('/dashboard')
