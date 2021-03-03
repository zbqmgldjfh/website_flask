from functools import wraps
from main import session, redirect, request, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None or session.get("id") == "":
            return redirect(url_for("member.member_login", next_url=request.url)) # 현재 페이지 url저장
        return f(*args, **kwargs)
    return decorated_function