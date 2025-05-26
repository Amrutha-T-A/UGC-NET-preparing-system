from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import app, db
from models import Admin, User, QuestionPaper
from forms import AdminLoginForm, UploadQuestionPaperForm

# Ensure the upload folder exists
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


#  Admin Login Route
@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid email or password", "danger")
    return render_template("admin_login.html", form=form)


#  Admin Dashboard Route (Protected)
@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        flash("Access denied!", "danger")
        return redirect(url_for('admin_login'))
    
    users = User.query.all()
    question_papers = QuestionPaper.query.all()
    return render_template("admin_dashboard.html", users=users, question_papers=question_papers)


#  Admin Logout Route
@app.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("admin_login"))


#  Delete User Route
@app.route("/admin/delete_user/<int:user_id>")
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully", "success")
    return redirect(url_for("admin_dashboard"))


#  Delete Question Paper Route
@app.route("/admin/delete_question_paper/<int:paper_id>")
@login_required
def delete_question_paper(paper_id):
    paper = QuestionPaper.query.get(paper_id)
    if paper:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], paper.pdf_filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        db.session.delete(paper)
        db.session.commit()
        flash("Question paper deleted successfully", "success")
    return redirect(url_for("admin_dashboard"))


#  Upload Question Paper Route
@app.route("/admin/upload_question_paper", methods=["GET", "POST"])
@login_required
def upload_question_paper():
    if not isinstance(current_user, Admin):
        flash("Access denied!", "danger")
        return redirect(url_for('admin_login'))

    form = UploadQuestionPaperForm()
    if form.validate_on_submit():
        file = form.pdf_file.data
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            new_paper = QuestionPaper(
                year=form.year.data,
                month=form.month.data,
                subject=form.subject.data,
                pdf_filename=filename
            )
            db.session.add(new_paper)
            db.session.commit()
            flash("Question paper uploaded successfully!", "success")
            return redirect(url_for("admin_dashboard"))
    return render_template("upload_question_paper.html", form=form)


#  Serve Uploaded Files
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
