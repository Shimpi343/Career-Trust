from .auth import auth_bp
from .opportunities import opportunities_bp
from .recommendations import recommendations_bp
from .scam_detection import scam_detection_bp
from .jobs import jobs_bp
from .profile import profile_bp
from .analytics import analytics_bp
from .notifications import notifications_bp

__all__ = ['auth_bp', 'opportunities_bp', 'recommendations_bp', 'scam_detection_bp', 'jobs_bp', 'profile_bp', 'analytics_bp', 'notifications_bp']
