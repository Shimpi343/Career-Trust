"""
Job Integrations Service
Handles fetching job opportunities from multiple sources:
- RemoteOK (Remote jobs worldwide)
- Dev.to Jobs (Developer jobs)
- JustJoinIT (European tech jobs)
- Stack Exchange (Stack Overflow jobs)
- LinkedIn (requires authentication)
- Indeed (requires API key)
"""

import requests
import os
import json
from datetime import datetime
from typing import List, Dict, Optional


class JobIntegrationError(Exception):
    """Custom exception for job integration errors"""
    pass


class GitHubJobsIntegration:
    """
    Fetch jobs from RemoteOK API
    Free API, no authentication required, actual remote jobs
    (Note: GitHub Jobs API was shut down in 2024)
    """
    BASE_URL = "https://remoteok.io/api"
    
    @classmethod
    def fetch_jobs(cls, search_term: str = "", location: str = "", page: int = 1) -> List[Dict]:
        """
        Fetch jobs from RemoteOK API
        
        Args:
            search_term: Job title to search for (e.g., 'python')
            location: Location to search (not used by RemoteOK API)
            page: Page number
        
        Returns:
            List of job dictionaries
        """
        try:
            params = {}
            
            if search_term:
                params['search'] = search_term
            
            # RemoteOK requires a User-Agent header to return JSON instead of HTML
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(cls.BASE_URL, params=params, timeout=10, headers=headers)
            response.raise_for_status()
            
            jobs = response.json()
            
            # Filter out metadata (first item at index 0)
            # RemoteOK returns: [{metadata: {last_updated, legal}}, {job1}, {job2}, ...]
            if isinstance(jobs, list) and len(jobs) > 0:
                jobs = jobs[1:]
            
            # Transform to standard format
            standardized_jobs = []
            for job in jobs:
                if not isinstance(job, dict):
                    continue
                    
                # Build salary string if available
                salary_str = None
                if job.get('salary_min') or job.get('salary_max'):
                    salary_str = f"${job.get('salary_min', '')} - ${job.get('salary_max', '')}"
                
                standardized_jobs.append({
                    'title': job.get('position', ''),  # RemoteOK uses 'position' not 'title'
                    'company': job.get('company', ''),
                    'location': job.get('location', 'Remote'),
                    'description': job.get('description', ''),
                    'job_url': job.get('url', ''),
                    'posted_at': job.get('date', ''),  # RemoteOK uses 'date' not 'date_posted'
                    'job_type': 'Job',
                    'source': 'RemoteOK',
                    'salary': salary_str,
                    'trust_score': 90,  # RemoteOK is trusted
                })
            
            return standardized_jobs
        
        except requests.exceptions.Timeout:
            print("RemoteOK API timeout - will try again later")
            return []
        except requests.exceptions.ConnectionError:
            print("RemoteOK connection error - check internet")
            return []
        except requests.exceptions.RequestException as e:
            print(f"RemoteOK API error: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error in RemoteOK: {str(e)}")
            return []


class DeveloperJobsIntegration:
    """
    Fetch jobs from Dev.to Jobs API
    Free, no authentication needed
    """
    BASE_URL = "https://dev.to/api/listings"
    
    @classmethod
    def fetch_jobs(cls, search_term: str = "", limit: int = 25) -> List[Dict]:
        """
        Fetch jobs from Dev.to
        
        Args:
            search_term: Job title to search for
            limit: Number of results
        
        Returns:
            List of job dictionaries
        """
        try:
            # Dev.to API for job listings
            params = {
                'category': 'jobs',
                'limit': min(limit, 100)
            }
            
            response = requests.get(cls.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            jobs = response.json()
            
            standardized_jobs = []
            for job in jobs:
                if not isinstance(job, dict):
                    continue
                
                # Filter by search term if provided
                title = job.get('title', '')
                description = job.get('body_html', '')
                
                if search_term and search_term.lower() not in title.lower() + ' ' + description.lower():
                    continue
                
                standardized_jobs.append({
                    'title': title,
                    'company': job.get('organization', {}).get('name', 'Unknown'),
                    'location': 'Remote',
                    'description': description,
                    'job_url': job.get('url', ''),
                    'posted_at': job.get('published_at_datetime', ''),
                    'job_type': 'Job',
                    'source': 'Dev.to',
                    'salary': None,
                    'trust_score': 85,
                })
            
            return standardized_jobs
        
        except requests.exceptions.Timeout:
            print("Dev.to API timeout")
            return []
        except requests.exceptions.ConnectionError:
            print("Dev.to connection error")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Dev.to API error: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error in Dev.to: {str(e)}")
            return []


class JustJoinITIntegration:
    """
    Fetch jobs from JustJoinIT API
    Free API for European tech jobs
    """
    BASE_URL = "https://justjoin.it/api/offers"
    
    @classmethod
    def fetch_jobs(cls, search_term: str = "", limit: int = 25) -> List[Dict]:
        """
        Fetch jobs from JustJoinIT
        
        Args:
            search_term: Job title to search for
            limit: Number of results
        
        Returns:
            List of job dictionaries
        """
        try:
            # JustJoinIT API returns all jobs, we filter on client side
            response = requests.get(cls.BASE_URL, timeout=10)
            response.raise_for_status()
            
            jobs = response.json() if isinstance(response.json(), list) else response.json().get('data', [])
            
            standardized_jobs = []
            count = 0
            
            for job in jobs:
                if not isinstance(job, dict) or count >= limit:
                    continue
                
                # Filter by search term if provided
                title = job.get('title', '')
                if search_term and search_term.lower() not in title.lower():
                    continue
                
                standardized_jobs.append({
                    'title': title,
                    'company': job.get('company_name', ''),
                    'location': ', '.join([job.get('city', ''), job.get('country_code', '')]).strip(', '),
                    'description': job.get('description', '') or f"{job.get('title', '')} position",
                    'job_url': f"https://justjoin.it/offers/{job.get('id', '')}",
                    'posted_at': job.get('published_at', ''),
                    'job_type': 'Job',
                    'source': 'JustJoinIT',
                    'salary': f"{job.get('salary_from', '')} - {job.get('salary_to', '')}".strip(' - ') if job.get('salary_from') else None,
                    'trust_score': 88,
                })
                count += 1
            
            return standardized_jobs
        
        except requests.exceptions.RequestException as e:
            # Return empty list if API fails, will try other sources
            print(f"JustJoinIT API error: {str(e)}")
            return []


class StackOverflowJobsIntegration:
    """
    Fetch jobs from Stack Exchange API
    Free API for Stack Overflow job listings
    """
    BASE_URL = "https://api.stackexchange.com/2.3/jobs"
    
    @classmethod
    def fetch_jobs(cls, search_term: str = "", limit: int = 25) -> List[Dict]:
        """
        Fetch jobs from Stack Overflow
        
        Args:
            search_term: Job title to search for
            limit: Number of results
        
        Returns:
            List of job dictionaries
        """
        try:
            params = {
                'site': 'stackoverflow',
                'sort': 'creation',
                'order': 'desc',
                'pagesize': min(limit, 100)
            }
            
            if search_term:
                params['tagged'] = search_term
            
            response = requests.get(cls.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('items', [])
            
            standardized_jobs = []
            for job in jobs[:limit]:
                if not isinstance(job, dict):
                    continue
                
                standardized_jobs.append({
                    'title': job.get('title', ''),
                    'company': job.get('company_name', ''),
                    'location': ', '.join(job.get('location', [])) if job.get('location') else 'Multiple',
                    'description': job.get('description', ''),
                    'job_url': job.get('link', ''),
                    'posted_at': datetime.fromtimestamp(job.get('creation_date', 0)).isoformat(),
                    'job_type': 'Job',
                    'source': 'Stack Overflow',
                    'salary': None,
                    'trust_score': 92,
                })
            
            return standardized_jobs
        
        except requests.exceptions.Timeout:
            print("Stack Overflow API timeout")
            return []
        except requests.exceptions.ConnectionError:
            print("Stack Overflow connection error")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Stack Overflow API error: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error in Stack Overflow: {str(e)}")
            return []


class IndeedIntegration:
    """
    Fetch jobs from Indeed
    Requires API key or uses unofficial scraping
    """
    API_KEY = os.environ.get('INDEED_API_KEY')
    BASE_URL = "https://api.indeed.com/ads/apisearch"
    
    @classmethod
    def fetch_jobs(cls, search_term: str = "software engineer", location: str = "USA", 
                   limit: int = 25) -> List[Dict]:
        """
        Fetch jobs from Indeed API
        
        Args:
            search_term: Job title to search for
            location: Location to search
            limit: Number of results to return (max 25)
        
        Returns:
            List of job dictionaries
        """
        if not cls.API_KEY:
            return cls._fetch_jobs_fallback(search_term, location, limit)
        
        try:
            params = {
                'publisher': cls.API_KEY,
                'q': search_term,
                'l': location,
                'sort': 'date',
                'limit': min(limit, 25),
                'fromage': 7,  # Last 7 days
                'co': 'us',
                'format': 'json'
            }
            
            response = requests.get(cls.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('results', [])
            
            # Transform to standard format
            standardized_jobs = []
            for job in jobs:
                standardized_jobs.append({
                    'title': job.get('jobtitle', ''),
                    'company': job.get('company', ''),
                    'location': job.get('location', ''),
                    'description': job.get('snippet', ''),
                    'job_url': job.get('url', ''),
                    'posted_at': datetime.fromtimestamp(int(job.get('date', 0))).isoformat(),
                    'job_type': 'Job',
                    'source': 'Indeed',
                    'salary': None,
                    'trust_score': 90,  # Indeed is trusted
                })
            
            return standardized_jobs
        
        except requests.exceptions.RequestException as e:
            raise JobIntegrationError(f"Indeed API error: {str(e)}")
    
    @classmethod
    def _fetch_jobs_fallback(cls, search_term: str, location: str, limit: int):
        """
        Fallback method for Indeed jobs
        Note: Indeed doesn't provide free public API, this returns empty
        Users need to provide INDEED_API_KEY environment variable
        """
        return []


class LinkedInIntegration:
    """
    Fetch jobs from LinkedIn
    Requires authentication (linkedin-api package)
    """
    
    @classmethod
    def fetch_jobs(cls, search_term: str = "software engineer", location: str = "USA") -> List[Dict]:
        """
        Fetch jobs from LinkedIn
        
        Requires linkedin-api package and valid credentials:
        - LINKEDIN_EMAIL environment variable
        - LINKEDIN_PASSWORD environment variable
        
        Args:
            search_term: Job title to search for
            location: Location to search
        
        Returns:
            List of job dictionaries
        """
        email = os.environ.get('LINKEDIN_EMAIL')
        password = os.environ.get('LINKEDIN_PASSWORD')
        
        if not email or not password:
            return cls._fetch_jobs_fallback()
        
        try:
            from linkedin_api import Linkedin
            
            # Connect to LinkedIn
            linkedin = Linkedin(email, password)
            
            # Search for jobs (LinkedIn API is limited, this is basic implementation)
            jobs = []
            
            # Note: LinkedIn's official API is restricted
            # The linkedin-api package uses unofficial API
            # Success depends on LinkedIn's current blocking policies
            
            return jobs
        
        except ImportError:
            return cls._fetch_jobs_fallback()
        except Exception as e:
            raise JobIntegrationError(f"LinkedIn integration error: {str(e)}")
    
    @classmethod
    def _fetch_jobs_fallback(cls):
        """
        Fallback for LinkedIn jobs
        LinkedIn requires special setup and is increasingly restrictive
        """
        print("LinkedIn integration requires: pip install linkedin-api")
        print("And valid LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables")
        return []


class JobAggregator:
    """
    Aggregate jobs from all sources
    """
    
    # Demo jobs for testing
    DEMO_JOBS = [
        {
            'title': 'Senior Python Developer',
            'company': 'Tech Startup Inc',
            'location': 'Remote',
            'description': 'We are looking for an experienced Python developer to join our growing team. You will work on backend services and APIs.',
            'job_url': 'https://example.com/jobs/1',
            'posted_at': '2026-04-10T00:00:00',
            'job_type': 'Job',
            'source': 'Demo',
            'salary': '$120,000 - $160,000',
            'trust_score': 100,
        },
        {
            'title': 'Frontend React Engineer',
            'company': 'Digital Solutions',
            'location': 'San Francisco, CA',
            'description': 'Join our design-focused team to build modern web applications. Experience with React, TypeScript, and Tailwind CSS preferred.',
            'job_url': 'https://example.com/jobs/2',
            'posted_at': '2026-04-09T00:00:00',
            'job_type': 'Job',
            'source': 'Demo',
            'salary': '$100,000 - $140,000',
            'trust_score': 100,
        },
        {
            'title': 'Full Stack Developer (JavaScript)',
            'company': 'Innovation Labs',
            'location': 'Remote',
            'description': 'Full-stack opportunity using Node.js and React. Work with cutting-edge technologies in a fast-paced environment.',
            'job_url': 'https://example.com/jobs/3',
            'posted_at': '2026-04-08T00:00:00',
            'job_type': 'Job',
            'source': 'Demo',
            'salary': '$110,000 - $150,000',
            'trust_score': 100,
        },
        {
            'title': 'Data Scientist',
            'company': 'AI Analytics Corp',
            'location': 'NYC, NY',
            'description': 'Apply machine learning to real-world problems. We use Python, TensorFlow, and cloud platforms.',
            'job_url': 'https://example.com/jobs/4',
            'posted_at': '2026-04-07T00:00:00',
            'job_type': 'Job',
            'source': 'Demo',
            'salary': '$130,000 - $180,000',
            'trust_score': 100,
        },
    ]
    
    @staticmethod
    def fetch_all_jobs(search_term: str = "", limit_per_source: int = 10) -> Dict[str, List[Dict]]:
        """
        Fetch jobs from all available sources
        
        Args:
            search_term: Job to search for
            limit_per_source: Max results per source
        
        Returns:
            Dictionary with source names as keys and job lists as values
        """
        results = {}
        
        # Fetch from RemoteOK (real remote jobs)
        try:
            results['remoteok'] = GitHubJobsIntegration.fetch_jobs(
                search_term=search_term, 
                page=1
            )[:limit_per_source]
        except JobIntegrationError as e:
            print(f"RemoteOK fetch failed: {e}")
            results['remoteok'] = []
        except Exception as e:
            print(f"RemoteOK fetch error: {e}")
            results['remoteok'] = []
        
        # Fetch from Dev.to (developer jobs)
        try:
            results['devto'] = DeveloperJobsIntegration.fetch_jobs(
                search_term=search_term,
                limit=limit_per_source
            )
        except JobIntegrationError as e:
            print(f"Dev.to fetch failed: {e}")
            results['devto'] = []
        except Exception as e:
            print(f"Dev.to fetch error: {e}")
            results['devto'] = []
        
        # Fetch from JustJoinIT (European tech jobs)
        try:
            results['justjoinit'] = JustJoinITIntegration.fetch_jobs(
                search_term=search_term,
                limit=limit_per_source
            )
        except Exception as e:
            print(f"JustJoinIT fetch error: {e}")
            results['justjoinit'] = []
        
        # Fetch from Stack Overflow (verified jobs)
        try:
            results['stackoverflow'] = StackOverflowJobsIntegration.fetch_jobs(
                search_term=search_term,
                limit=limit_per_source
            )
        except JobIntegrationError as e:
            print(f"Stack Overflow fetch failed: {e}")
            results['stackoverflow'] = []
        except Exception as e:
            print(f"Stack Overflow fetch error: {e}")
            results['stackoverflow'] = []
        
        # Fetch from Indeed (if API key available)
        try:
            results['indeed'] = IndeedIntegration.fetch_jobs(
                search_term=search_term,
                limit=limit_per_source
            )
        except JobIntegrationError as e:
            print(f"Indeed fetch failed: {e}")
            results['indeed'] = []
        except Exception as e:
            print(f"Indeed fetch error: {e}")
            results['indeed'] = []
        
        # Fetch from LinkedIn (if credentials available)
        try:
            results['linkedin'] = LinkedInIntegration.fetch_jobs(
                search_term=search_term
            )[:limit_per_source]
        except JobIntegrationError as e:
            print(f"LinkedIn fetch failed: {e}")
            results['linkedin'] = []
        except Exception as e:
            print(f"LinkedIn fetch error: {e}")
            results['linkedin'] = []
        
        return results
    
    @staticmethod
    def flatten_jobs(aggregated_jobs: Dict[str, List[Dict]]) -> List[Dict]:
        """
        Flatten aggregated jobs into single list
        
        Args:
            aggregated_jobs: Dictionary from fetch_all_jobs()
        
        Returns:
            Flattened list of all jobs
        """
        all_jobs = []
        for source, jobs in aggregated_jobs.items():
            all_jobs.extend(jobs)
        
        return all_jobs
