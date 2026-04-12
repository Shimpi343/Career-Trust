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
    JobIntegrationError
)

__all__ = [
    'JobAggregator',
    'GitHubJobsIntegration',
    'DeveloperJobsIntegration',
    'JustJoinITIntegration',
    'StackOverflowJobsIntegration',
    'IndeedIntegration',
    'LinkedInIntegration',
    'JobIntegrationError',
]
