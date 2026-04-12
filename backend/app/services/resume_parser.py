"""
Resume Parser Service
Extracts text and skills from PDF/DOC resume files
"""

import PyPDF2
from docx import Document
import io
from typing import Tuple, List


class ResumeParser:
    """
    Parse resume files and extract text content
    """
    
    @staticmethod
    def extract_from_pdf(file_content: bytes) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_content: Binary PDF content
        
        Returns:
            Extracted text
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")
    
    @staticmethod
    def extract_from_docx(file_content: bytes) -> str:
        """
        Extract text from DOCX file
        
        Args:
            file_content: Binary DOCX content
        
        Returns:
            Extracted text
        """
        try:
            doc = Document(io.BytesIO(file_content))
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {str(e)}")
    
    @staticmethod
    def extract_from_resume(file_content: bytes, filename: str) -> str:
        """
        Extract text from resume file (PDF or DOCX)
        
        Args:
            file_content: Binary file content
            filename: Original filename
        
        Returns:
            Extracted resume text
        """
        filename_lower = filename.lower()
        
        if filename_lower.endswith('.pdf'):
            return ResumeParser.extract_from_pdf(file_content)
        elif filename_lower.endswith(('.docx', '.doc')):
            return ResumeParser.extract_from_docx(file_content)
        else:
            raise ValueError("Only PDF and DOCX files are supported")
    
    @staticmethod
    def parse_resume(file_content: bytes, filename: str) -> Tuple[str, List[str]]:
        """
        Parse resume and extract skills
        
        Args:
            file_content: Binary file content
            filename: Original filename
        
        Returns:
            Tuple of (resume_text, extracted_skills)
        """
        from app.services.skill_matching import SkillMatcher
        
        # Extract text
        resume_text = ResumeParser.extract_from_resume(file_content, filename)
        
        # Extract skills
        skills = SkillMatcher.extract_skills_from_text(resume_text)
        
        return resume_text, skills
