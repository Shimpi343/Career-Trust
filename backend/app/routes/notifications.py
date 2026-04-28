from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import User
from app.services.notification_service import NotificationService

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')


@notifications_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_notification_settings():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        return jsonify({
            'success': True,
            'settings': NotificationService.get_settings(user),
        }), 200
    except Exception as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500


@notifications_bp.route('/settings', methods=['POST'])
@jwt_required()
def update_notification_settings():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        data = request.get_json() or {}
        updates = {
            'email_alerts': bool(data.get('email_alerts')) if 'email_alerts' in data else None,
            'digest_frequency': data.get('digest_frequency'),
            'digest_day': data.get('digest_day'),
            'digest_time': data.get('digest_time'),
            'email': data.get('email'),
        }

        settings = NotificationService.update_settings(user, updates)
        return jsonify({
            'success': True,
            'message': 'Notification settings updated',
            'settings': settings,
        }), 200
    except Exception as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500


@notifications_bp.route('/test-email', methods=['POST'])
@jwt_required()
def send_test_email():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        subject = 'CareerTrust test email'
        body = (
            f'Hi {user.username},\n\n'
            'This is a test message from CareerTrust notifications.\n\n'
            'If you received this, your SMTP settings are working correctly.\n\n'
            '— CareerTrust'
        )
        destination_email = NotificationService.get_settings(user).get('email') or user.email

        sent, message = NotificationService._send_email(destination_email, subject, body)
        status_code = 200 if sent else 503
        return jsonify({
            'success': sent,
            'message': message,
            'destination_email': destination_email,
        }), status_code
    except Exception as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500


@notifications_bp.route('/digest', methods=['POST'])
@jwt_required()
def send_manual_digest():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        data = request.get_json() or {}
        frequency = data.get('frequency', 'daily')
        if frequency not in {'daily', 'weekly'}:
            return jsonify({'success': False, 'error': 'frequency must be daily or weekly'}), 400

        result = NotificationService.send_digest_for_user(user, frequency=frequency)
        return jsonify({
            'success': bool(result.get('sent')),
            'result': result,
        }), 200 if result.get('sent') else 503
    except Exception as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500
