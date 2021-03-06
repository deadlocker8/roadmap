from flask import jsonify


class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.response = jsonify({'success': False,
                                 'msg': message})


class RequestValidator:
    @staticmethod
    def validate(request, parameters):
        if not request.is_json:
            raise ValidationError('Missing JSON in request')

        result = {}
        for param in parameters:
            value = request.json.get(param, None)
            if value is None:
                raise ValidationError(f'Missing parameter "{param}"')
            result[param] = value

        return result
