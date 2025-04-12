# app/admin/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user
from app.models import User, Message
from app.forms import ChooseForm
from app import db, auth_bp

admin_bp = Blueprint("admin_bp", __name__, template_folder="templates")


@admin_bp.route("/")
@login_required
def admin():
    if current_user.role != "Admin":
        return redirect(url_for('home'))
    form = ChooseForm()
    q = db.select(User)
    user_lst = db.session.scalars(q)
    return render_template('admin.html', title="Admin", user_lst=user_lst, form=form)

@admin_bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def view_user(user_id):
    if current_user.role != "Admin":
        flash("Admins only.", "danger")
        return redirect(url_for('home'))

    user = db.session.get(User, user_id)
    if not user:
        flash("User not found.", "warning")
        return redirect(url_for('admin_bp.admin') )

    if request.method == 'POST':
        if 'delete' in request.form:
            if user.id == current_user.id:
                flash("You can't delete yourself!", "warning")
            else:
                db.session.delete(user)
                db.session.commit()
                flash(f"User '{user.username}' deleted.", "success")
                return redirect(url_for('admin_bp.admin') )
        else:
            user.firstname = request.form.get('firstname')
            user.lastname = request.form.get('lastname')
            user.email = request.form.get('email')
            user.username = request.form.get('username')
            user.role = request.form.get('role')

            if user.type == 'student':
                user.degree = request.form.get('degree')
                user.address = request.form.get('address')
            elif user.type == 'professional':
                user.workplace = request.form.get('workplace')
                user.specialty = request.form.get('specialty')

            db.session.commit()
            flash("User details updated.", "success")
            return redirect(url_for('admin_bp.view_user', user_id=user.id))

    return render_template("adminDashboard.html", title=f"Edit {user.username}", user=user)

@admin_bp.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    form = ChooseForm()
    if form.validate_on_submit():
        user = db.session.get(User, int(form.choice.data))
        if user.id == current_user.id:
            flash("You cannot delete yourself.", "danger")
            return redirect(url_for("admin_bp.dashboard"))

        # 🧹 Clean up related messages
        db.session.query(Message).filter(
            (Message.sender_id == user.id) | (Message.receiver_id == user.id)
        ).delete()

        db.session.delete(user)
        db.session.commit()
        flash("User deleted.", "success")

    return redirect(url_for("admin_bp.dashboard"))


@admin_bp.route('/toggle_user_role', methods=['POST'])
def toggle_user_role():
    form = ChooseForm()
    if form.validate_on_submit():
        u = db.session.get(User, int(form.choice.data))
        q = db.select(User).where((User.role == "Admin") & (User.id != u.id))
        first = db.session.scalars(q).first()
        if not first:
            flash("You can't drop your admin role if there are no other admin users!", "danger")
        elif u.id == current_user.id:
            logout_user()
            u.role = "Normal"
            db.session.commit()
            return redirect(url_for('home'))
        else:
            u.role = "Normal" if u.role == "Admin" else "Admin"
            db.session.commit()
    return redirect(url_for('admin_bp.admin'))
