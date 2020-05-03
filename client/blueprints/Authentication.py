import requests
from flask import Blueprint, render_template, redirect, url_for, request, session

from logic.Localization import LOCALIZATION


def construct_blueprint(urlBuilder):
    authentication = Blueprint('authentication', __name__)

    @authentication.route('/admin/login')
    def login():
        return render_template('login.html')

    @authentication.route('/admin/login', methods=['POST'])
    def loginPost():
        password = request.form.get('password')
        if not password:
            return redirect('/admin/login')

        jsonData = {'username': 'admin', 'password': password}

        response = requests.post(urlBuilder.build_url('login'), json=jsonData)

        if response.status_code == 401:
            return render_template('login.html', message=LOCALIZATION['unauthorized'])

        if response.status_code == 200:
            token = response.json()['access_token']
            session['session_token'] = token
            return redirect(url_for('admin_roadmaps.overview'))

        return render_template('error.html', message=response.json()['msg'])

    @authentication.route('/admin/logout')
    def logout():
        del session['session_token']
        return redirect('/')

    return authentication
