from flask import Blueprint, request, redirect, render_template, url_for, make_response
from flask import current_app as app
from flask.views import MethodView
import scribd

from auth import login_required, valid_token, valid_login, log_the_user_in, log_the_user_out

views = Blueprint('views', __name__, template_folder='templates')

class HomeView(MethodView):
    def get(self):
        docs = []
        for doc in scribd.api_user.xall():
            docs.append({
                'link': "/document?doc_id=" + doc.doc_id,
                'thumbnail': doc.thumbnail_url,
                'title': doc.title,
                'description': doc.description,
                'status': doc.conversion_status
                })
        return render_template('index.html', docs=docs, session=valid_token())

class LoginView(MethodView):
    def get(self):
        redirect_to = request.args.get('continue', url_for('views.home'))
        if valid_token():
            return redirect(redirect_to)
        else:
            return render_template('login.html', error=request.args.get('error'))

    def post(self):
        redirect_to = request.args.get('continue', url_for('views.home'))
        if valid_login(request.form['netid'], request.form['password']):
            resp = make_response(redirect(redirect_to))
            log_the_user_in(resp)
            return resp
        else:
            return redirect(url_for('views.login', error=request.login_error_message))


class LogoutView(MethodView):
    def get(self):
        redirect_to = request.args.get('continue', url_for('views.home'))
        resp = make_response(redirect(redirect_to))
        log_the_user_out(resp)
        return resp

class DocumentView(MethodView):
    def get(self):
        doc_id = request.args.get("doc_id")
        access_key = scribd.api_user.get(doc_id).get_attributes()['access_key']
        return render_template('document.html', doc_id=doc_id, access_key=access_key)


# Register the urls
views.add_url_rule('/', view_func=HomeView.as_view('home'))
views.add_url_rule('/login', view_func=LoginView.as_view('login'))
views.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))

doc_view = login_required(DocumentView.as_view('document'))
views.add_url_rule('/document', view_func=doc_view)

