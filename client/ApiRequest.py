from flask import render_template, session, redirect, url_for

from Localization import LOCALIZATION


class ApiRequest:
    @staticmethod
    def send_api_request(url, method, formArgs, argDefinitions):
        jsonData = {}
        for name, castType in argDefinitions:
            jsonData[name] = castType(formArgs.get(name))

        response = method(url, json=jsonData, headers={'Authorization': 'Bearer  {}'.format(session['session_token'])})
        if response.status_code == 401:
            return False, redirect(url_for('authentication.login'))

        if response.status_code != 200:
            return False, render_template('error.html', message='{}: {}'.format(LOCALIZATION['error_general'],
                                                                                response.json()['msg']))
        return True, response.json()
