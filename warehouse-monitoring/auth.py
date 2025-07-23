from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# 하드코딩된 관리자 정보 (DB 연동 가능)
ADMIN_ID = "admin"
ADMIN_PW = "1234"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("로그인이 필요합니다.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_ID and password == ADMIN_PW:
            session["user"] = username
            flash("로그인 성공!", "success")
            return redirect(url_for("index"))
        else:
            flash("아이디 또는 비밀번호가 잘못되었습니다.", "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("로그아웃 되었습니다.", "info")
    return redirect(url_for("auth.login"))
