from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, login_required, fresh_login_required
from app.forms import UpdateAccountForm, StudentUpdateForm, ProfessionalUpdateForm,ChangePasswordForm
from app import db

account_bp = Blueprint("account_bp", __name__, template_folder="templates")

@account_bp.route('/', methods=['GET', 'POST'])
@login_required
def account():
    base_form = UpdateAccountForm(obj=current_user)
    student_form = StudentUpdateForm(obj=current_user if current_user.type == "student" else None)
    professional_form = ProfessionalUpdateForm(obj=current_user if current_user.type == "professional" else None)

    # Handle POST
    if request.method == "POST":
        updated = False

        if base_form.validate_on_submit():
            current_user.firstname = base_form.firstname.data
            current_user.lastname = base_form.lastname.data
            current_user.email = base_form.email.data
            updated = True

        if current_user.type == "student" and student_form.validate_on_submit():
            current_user.degree = student_form.degree.data
            current_user.address = student_form.address.data
            updated = True

        if current_user.type == "professional" and professional_form.validate_on_submit():
            current_user.workplace = professional_form.workplace.data
            current_user.specialty = professional_form.specialty.data
            updated = True

        if updated:
            db.session.commit()
            flash("✅ Account info updated successfully", "success")
            return redirect(url_for("account_bp.account"))

    return render_template("account.html", title="Account", form=base_form, student_form=student_form, professional_form=professional_form)


@account_bp.route('/change_pw', methods=['GET', 'POST'])
@fresh_login_required
def change_pw():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password changed successfully', 'success')
        return redirect(url_for('home'))
    return render_template('generic_form.html', title='Change Password', form=form)