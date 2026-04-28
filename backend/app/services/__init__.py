"""
Backend services for job aggregation and processing
"""

from .job_integrations import (
    JobAggregator,
    GitHubJobsIntegration,
    DeveloperJobsIntegration,
    JustJoinITIntegration,
    StackOverflowJobsIntegration,
    IndeedIntegration,
    LinkedInIntegration,
    AdzunaIntegration,
    JoobleIntegration,
    JobIntegrationError
)

from .skill_matching import (
    SkillMatcher,
    RecommendationEngine
)

from .resume_parser import (
    ResumeParser
)

from .advanced_nlp import (
    AdvancedSkillMatcher,
    ResumeAnalyzer
)

from .notification_service import (
    NotificationService,
    start_notification_scheduler,
)

__all__ = [
    'JobAggregator',
    'GitHubJobsIntegration',
    'DeveloperJobsIntegration',
    'JustJoinITIntegration',
    'StackOverflowJobsIntegration',
    'IndeedIntegration',
    'LinkedInIntegration',
    'AdzunaIntegration',
    'JoobleIntegration',
    'JobIntegrationError',
    'SkillMatcher',
    'RecommendationEngine',
    'ResumeParser',
    'AdvancedSkillMatcher',
    'ResumeAnalyzer',
    'NotificationService',
    'start_notification_scheduler',
]
