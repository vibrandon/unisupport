from flask import render_template, redirect, url_for, flash, request
from app import app
from app import User, Professional, Student
from app import ChooseForm, LoginForm, ChangePasswordForm, RegisterForm, ChatbotForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit


@app.route("/match/auto")
@login_required
def auto_match():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    # Example student profile (can come from a form or current_user preferences)
    student_profile = "stress anxiety academic support motivation"

    # Load all professionals
    professionals = db.session.scalars(db.select(Professional)).all()

    # Create a list of professional descriptions
    prof_profiles = [f"{p.specialty}" for p in professionals]

    # Combine student and professional data for vectorizing
    profiles = [student_profile] + prof_profiles

    # Convert to vectors using TF-IDF
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(profiles)

    # Calculate cosine similarity between student and each professional
    similarities = cosine_similarity(vectors[0:1], vectors[1:])[0]  # shape (n_profs,)

    # Attach similarity scores
    scored_profs = list(zip(professionals, similarities))

    # Sort by similarity
    scored_profs.sort(key=lambda x: x[1], reverse=True)

    return render_template("match_results.html", title="Matched Professionals", scored_profs=scored_profs)


# =====================
# 🏠 Home Route
# =====================
@app.route("/")
def home():
    return render_template('home.html', title="UniSupport")

# =====================
# 👤 User Account Page: View + Edit Addresses
# =====================
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    from app import UpdateAccountForm, StudentUpdateForm, ProfessionalUpdateForm

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
            return redirect(url_for("account"))

    return render_template("account.html", title="Account", form=base_form, student_form=student_form, professional_form=professional_form)


# =====================
# 🔒 Admin Page: Manage users
# =====================
@app.route("/admin")
@login_required
def admin():
    if current_user.role != "Admin":
        return redirect(url_for('home'))
    form = ChooseForm()
    q = db.select(User)
    user_lst = db.session.scalars(q)
    return render_template('admin.html', title="Admin", user_lst=user_lst, form=form)


@app.route('/admin/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def view_user(user_id):
    if current_user.role != "Admin":
        flash("Admins only.", "danger")
        return redirect(url_for('home'))

    user = db.session.get(User, user_id)
    if not user:
        flash("User not found.", "warning")
        return redirect(url_for('admin'))

    if request.method == 'POST':
        if 'delete' in request.form:
            if user.id == current_user.id:
                flash("You can't delete yourself!", "warning")
            else:
                db.session.delete(user)
                db.session.commit()
                flash(f"User '{user.username}' deleted.", "success")
                return redirect(url_for('admin'))
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
            return redirect(url_for('view_user', user_id=user.id))

    return render_template("admin_user_detail.html", title=f"Edit {user.username}", user=user)


@app.route("/chat")
@login_required
def chat():
    return render_template('chat.html', title="Chat")

@app.route("/match")
@login_required
def match():
    return render_template('match.html', title="Match")

@app.route("/professionals")
@login_required
def view_professionals():
    from app import Professional  # if not already imported
    professionals = db.session.scalars(db.select(Professional)).all()
    return render_template("professionals.html", title="Professionals", professionals=professionals)


# =====================
# ❌ Delete User (with admin safety check)
# =====================
@app.route('/delete_user', methods=['POST'])
def delete_user():
    form = ChooseForm()
    if form.validate_on_submit():
        u = db.session.get(User, int(form.choice.data))
        q = db.select(User).where((User.role == "Admin") & (User.id != u.id))
        first = db.session.scalars(q).first()
        if not first:
            flash("You can't delete your own account if there are no other admin users!", "danger")
        elif u.id == current_user.id:
            logout_user()
            db.session.delete(u)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            db.session.delete(u)
            db.session.commit()
    return redirect(url_for('admin'))

# =====================
# 🔁 Toggle User Role (admin <--> normal)
# =====================
@app.route('/toggle_user_role', methods=['POST'])
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
    return redirect(url_for('admin'))



# =====================
# 🔐 Login / Logout / Register / Change Password
# =====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('generic_form.html', title='Sign In', form=form)



@app.route('/change_pw', methods=['GET', 'POST'])
@fresh_login_required
def change_pw():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password changed successfully', 'success')
        return redirect(url_for('home'))
    return render_template('generic_form.html', title='Change Password', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()

    if form.validate_on_submit():
        if form.userType.data == 'student':
            #Make degree nullable and give them the option to change it in their account settings
            newUser = Student(
                username=form.username.data,
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                email=form.email.data,
                role='student'
            )
        elif form.userType.data == 'professional':
            #Make workplace nullable and give them an option to change it in their account settings.
            newUser = Professional(
                username=form.username.data,
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                email=form.email.data,
                role='professional'
            )
        else:
            flash('Invalid user type selected.', 'danger')
            return redirect(url_for('register'))

        newUser.set_password(form.password.data)
        db.session.add(newUser)
        db.session.commit()

        flash("🎉 Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('generic_form.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# =====================
# ❗ Error Handlers
# =====================
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500
