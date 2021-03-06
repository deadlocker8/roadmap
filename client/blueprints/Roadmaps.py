import requests
from flask import Blueprint, render_template, redirect, url_for, request

from logic.AdminWrapper import require_api_token
from logic.ApiRequest import ApiRequest
from logic.Localization import LOCALIZATION


def construct_blueprint(urlBuilder):
    roadmaps = Blueprint('admin_roadmaps', __name__)

    @roadmaps.route('/admin/roadmaps/overview', methods=['GET'])
    @require_api_token
    def overview():
        _, roadmapsData = ApiRequest.send_api_request(urlBuilder.build_url('roadmaps'), requests.get, {}, [])
        return render_template('admin/roadmaps/overview.html', roadmaps=roadmapsData)

    @roadmaps.route('/admin/roadmaps/add', methods=['GET'])
    @require_api_token
    def add():
        return render_template('admin/roadmaps/edit.html',
                               title='New Roadmap',
                               form_url=url_for('admin_roadmaps.add_post'))

    @roadmaps.route('/admin/roadmaps/add', methods=['POST'])
    @require_api_token
    def add_post():
        success, response = ApiRequest.send_api_request(urlBuilder.build_url('roadmap'),
                                                        requests.post, request.form,
                                                        [('Projectname', str),
                                                         ('StartDate', str),
                                                         ('Hidden', bool)])
        if not success:
            return response
        return redirect(url_for('admin_roadmaps.overview'))

    @roadmaps.route('/admin/roadmaps/edit', methods=['GET'])
    @require_api_token
    def edit():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        _, roadmap = ApiRequest.send_api_request(urlBuilder.build_url('roadmap', ID), requests.get, {}, [])

        if roadmap['StartDate'] == '-':
            roadmap['StartDate'] = ''

        return render_template('admin/roadmaps/edit.html',
                               title='Edit Roadmap',
                               roadmap=roadmap,
                               form_url=url_for('admin_roadmaps.edit_post'))

    @roadmaps.route('/admin/roadmaps/edit', methods=['POST'])
    @require_api_token
    def edit_post():
        success, response = ApiRequest.send_api_request(urlBuilder.build_url('roadmap'),
                                                        requests.put, request.form,
                                                        [('ID', int), ('Projectname', str),
                                                         ('Hidden', bool), ('StartDate', str)])

        if not success:
            return response
        return redirect(url_for('admin_roadmaps.overview'))

    @roadmaps.route('/admin/roadmaps/delete', methods=['GET'])
    @require_api_token
    def delete():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('roadmap', ID), requests.delete, {}, [])
        if not success:
            return response
        return redirect(url_for('admin_roadmaps.overview'))

    return roadmaps
