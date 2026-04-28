import logging
import os
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import Any, Dict, List, Tuple

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import or_

from app.models import Opportunity, User
from app.services.skill_matching import SkillMatcher

logger = logging.getLogger(__name__)

_scheduler = BackgroundScheduler(timezone='UTC')
_scheduler_started = False


class NotificationService:
    """Email alerts and digest helpers for job matching notifications."""

    DEFAULT_SETTINGS: Dict[str, Any] = {
        'email_alerts': False,
        'digest_frequency': 'weekly',
        'digest_day': 'monday',
        'digest_time': '08:00',
        'email': None,
        'last_alert_sent_at': None,
        'last_digest_sent_at': None,
    }

    @staticmethod
    def get_settings(user: User) -> Dict[str, Any]:
        preferences = user.preferences or {}
        notifications = preferences.get('notifications') or {}
        return {**NotificationService.DEFAULT_SETTINGS, **notifications}

    @staticmethod
    def update_settings(user: User, updates: Dict[str, Any]) -> Dict[str, Any]:
        from app import db
        
        preferences = user.preferences or {}
        notifications = preferences.get('notifications') or {}

        for key, value in updates.items():
            if value is not None:
                notifications[key] = value

        preferences['notifications'] = notifications
        user.preferences = preferences
        user.updated_at = datetime.utcnow()
        db.session.commit()
        return notifications

    @staticmethod
    def smtp_is_configured() -> bool:
        return bool(
            os.getenv('SMTP_HOST')
            and os.getenv('SMTP_PORT')
            and os.getenv('SMTP_USERNAME')
            and os.getenv('SMTP_PASSWORD')
        )

    @staticmethod
    def _send_email(to_email: str, subject: str, body: str) -> Tuple[bool, str]:
        if not NotificationService.smtp_is_configured():
            return False, 'SMTP is not configured'

        host = os.getenv('SMTP_HOST')
        port = int(os.getenv('SMTP_PORT', '587'))
        username = os.getenv('SMTP_USERNAME')
        password = os.getenv('SMTP_PASSWORD')
        sender = os.getenv('NOTIFICATIONS_FROM_EMAIL', username)
        use_tls = os.getenv('SMTP_USE_TLS', 'true').lower() != 'false'
        use_ssl = os.getenv('SMTP_USE_SSL', 'false').lower() == 'true'

        message = EmailMessage()
        message['From'] = sender
        message['To'] = to_email
        message['Subject'] = subject
        message.set_content(body)

        try:
            if use_ssl:
                with smtplib.SMTP_SSL(host, port) as smtp:
                    smtp.login(username, password)
                    smtp.send_message(message)
            else:
                with smtplib.SMTP(host, port) as smtp:
                    if use_tls:
                        smtp.starttls()
                    smtp.login(username, password)
                    smtp.send_message(message)
            return True, 'Email sent'
        except Exception as exc:
            logger.error('Email delivery failed: %s', exc)
            return False, str(exc)

    @staticmethod
    def _job_matches_user(user: User, job: Opportunity) -> Tuple[float, List[str], List[str]]:
        description = f"{job.title} {job.description or ''} {job.requirements or ''}"
        return SkillMatcher.calculate_match_score(user.skills or [], description)

    @staticmethod
    def get_matching_jobs(user: User, lookback_days: int = 7, limit: int = 10) -> List[Dict[str, Any]]:
        cutoff = datetime.utcnow() - timedelta(days=lookback_days)
        query = Opportunity.query.filter(
            or_(
                Opportunity.created_at >= cutoff,
                Opportunity.posted_at >= cutoff,
            )
        )

        preferences = user.preferences or {}
        preferred_location = ' '.join(preferences.get('location') or []).lower()
        preferred_job_types = {str(item).lower() for item in (preferences.get('job_type') or [])}
        preferred_sources = {str(item).lower() for item in (preferences.get('sources') or [])}
        remote_only = bool(preferences.get('remote_only'))
        preferred_salary = preferences.get('min_salary')

        results: List[Dict[str, Any]] = []
        for job in query.order_by(Opportunity.created_at.desc()).limit(100).all():
            match_score, matched_skills, missing_skills = NotificationService._job_matches_user(user, job)
            if match_score <= 0:
                continue

            job_location = (job.location or '').lower()
            job_source = (job.source or '').lower()
            job_type = (job.job_type or '').lower()

            if remote_only and 'remote' not in job_location:
                continue
            if preferred_location and preferred_location not in job_location:
                continue
            if preferred_job_types and job_type and job_type not in preferred_job_types:
                continue
            if preferred_sources and job_source and job_source not in preferred_sources:
                continue
            if preferred_salary:
                salary_text = str(job.salary or '')
                if salary_text and str(preferred_salary) not in salary_text:
                    pass

            results.append(
                {
                    'id': job.id,
                    'title': job.title,
                    'company': job.company,
                    'location': job.location,
                    'salary': job.salary,
                    'job_type': job.job_type,
                    'source': job.source,
                    'url': job.url,
                    'trust_score': job.trust_score,
                    'match_score': round(match_score, 1),
                    'matched_skills': matched_skills,
                    'missing_skills': missing_skills,
                }
            )

        results.sort(key=lambda item: item.get('match_score', 0), reverse=True)
        return results[:limit]

    @staticmethod
    def build_digest_email(user: User, jobs: List[Dict[str, Any]], frequency: str) -> Tuple[str, str]:
        heading = 'Daily' if frequency == 'daily' else 'Weekly'
        subject = f'CareerTrust {heading} Digest - {len(jobs)} matches for you'
        lines = [
            f'Hi {user.username},',
            '',
            f'Here are your top {heading.lower()} job matches from CareerTrust:',
            '',
        ]

        if not jobs:
            lines.extend([
                'No strong matches were found in this digest window.',
                'Try updating your skills or preferences so we can send better matches next time.',
            ])
            return subject, '\n'.join(lines)

        for index, job in enumerate(jobs, start=1):
            lines.extend([
                f'{index}. {job["title"]} at {job["company"]}',
                f'   Match: {job.get("match_score", 0)}% | Source: {job.get("source") or "Unknown"}',
                f'   Location: {job.get("location") or "Not specified"}',
            ])
            if job.get('url'):
                lines.append(f'   Link: {job["url"]}')
            lines.append('')

        lines.extend([
            'Open CareerTrust to review, save, and apply to the best matches.',
            '',
            '— CareerTrust',
        ])
        return subject, '\n'.join(lines)

    @staticmethod
    def send_digest_for_user(user: User, frequency: str = 'daily') -> Dict[str, Any]:
        settings = NotificationService.get_settings(user)
        if not settings.get('email_alerts'):
            return {'sent': False, 'reason': 'Email alerts are disabled'}

        if frequency == 'weekly' and settings.get('digest_frequency', 'weekly') != 'weekly':
            return {'sent': False, 'reason': 'Weekly digest is disabled'}

        lookback_days = 1 if frequency == 'daily' else 7
        jobs = NotificationService.get_matching_jobs(user, lookback_days=lookback_days, limit=10)
        subject, body = NotificationService.build_digest_email(user, jobs, frequency)
        destination_email = settings.get('email') or user.email

        if not destination_email:
            return {'sent': False, 'reason': 'No destination email configured'}

        sent, message = NotificationService._send_email(destination_email, subject, body)
        if sent:
            timestamp_key = 'last_digest_sent_at'
            if frequency == 'daily':
                settings[timestamp_key] = datetime.utcnow().isoformat()
            else:
                settings[timestamp_key] = datetime.utcnow().isoformat()
            NotificationService.update_settings(user, settings)

        return {'sent': sent, 'message': message, 'jobs_count': len(jobs)}

    @staticmethod
    def send_alerts_for_user(user: User) -> Dict[str, Any]:
        settings = NotificationService.get_settings(user)
        if not settings.get('email_alerts'):
            return {'sent': False, 'reason': 'Email alerts are disabled'}

        jobs = NotificationService.get_matching_jobs(user, lookback_days=1, limit=5)
        if not jobs:
            return {'sent': False, 'reason': 'No new matches'}

        subject = f'CareerTrust: {len(jobs)} new matches for you'
        lines = [f'Hi {user.username},', '', 'New matching jobs were found for your profile:', '']
        for job in jobs:
            lines.append(f'- {job["title"]} at {job["company"]} ({job.get("match_score", 0)}%)')
            if job.get('url'):
                lines.append(f'  {job["url"]}')
        lines.extend(['', 'Open CareerTrust to review them.', '', '— CareerTrust'])

        destination_email = settings.get('email') or user.email
        if not destination_email:
            return {'sent': False, 'reason': 'No destination email configured'}

        sent, message = NotificationService._send_email(destination_email, subject, '\n'.join(lines))
        if sent:
            settings['last_alert_sent_at'] = datetime.utcnow().isoformat()
            NotificationService.update_settings(user, settings)

        return {'sent': sent, 'message': message, 'jobs_count': len(jobs)}


def start_notification_scheduler(app) -> None:
    """Start the background scheduler once per process."""
    global _scheduler_started

    if _scheduler_started or app.config.get('TESTING'):
        return

    if app.debug and os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        return

    def run_alerts():
        with app.app_context():
            users = User.query.all()
            for user in users:
                try:
                    NotificationService.send_alerts_for_user(user)
                except Exception as exc:
                    logger.error('Failed to send alert email for user %s: %s', user.id, exc)

    def run_daily_digests():
        with app.app_context():
            users = User.query.all()
            for user in users:
                try:
                    NotificationService.send_digest_for_user(user, frequency='daily')
                except Exception as exc:
                    logger.error('Failed to send daily digest for user %s: %s', user.id, exc)

    def run_weekly_digests():
        with app.app_context():
            users = User.query.all()
            for user in users:
                try:
                    NotificationService.send_digest_for_user(user, frequency='weekly')
                except Exception as exc:
                    logger.error('Failed to send weekly digest for user %s: %s', user.id, exc)

    _scheduler.add_job(run_alerts, 'interval', hours=1, id='careertrust_email_alerts', replace_existing=True)
    _scheduler.add_job(run_daily_digests, 'cron', hour=8, minute=0, id='careertrust_daily_digest', replace_existing=True)
    _scheduler.add_job(run_weekly_digests, 'cron', day_of_week='mon', hour=8, minute=30, id='careertrust_weekly_digest', replace_existing=True)
    _scheduler.start()
    _scheduler_started = True
    logger.info('Notification scheduler started with email alerts and digest jobs')
