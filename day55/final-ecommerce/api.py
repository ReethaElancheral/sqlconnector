from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)
def csrf_exempt_bp(app):
    pass
@api_bp.route('/ping')
def ping():
    return jsonify({'message':'pong'})