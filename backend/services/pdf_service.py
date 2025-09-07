import os
import base64
from datetime import datetime
from typing import Dict, List, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io

class PDFService:
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "exports")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize ReportLab styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the PDF."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#007bff')
        ))
        
        # Header style
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            textColor=colors.HexColor('#007bff')
        ))
        
        # Subheader style
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.HexColor('#333333')
        ))
        
        # Question style
        self.styles.add(ParagraphStyle(
            name='Question',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            leftIndent=20,
            textColor=colors.HexColor('#007bff'),
            fontName='Helvetica-Bold'
        ))
        
        # Answer style
        self.styles.add(ParagraphStyle(
            name='Answer',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leftIndent=20,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica-Oblique'
        ))
        
        # Feedback style
        self.styles.add(ParagraphStyle(
            name='Feedback',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leftIndent=20,
            textColor=colors.HexColor('#333333')
        ))
    
    def generate_interview_report_pdf(self, session_data: Dict[str, Any], report_data: Dict[str, Any]) -> str:
        """Generate a comprehensive PDF report for an interview session."""
        
        # Validate input data
        if not session_data:
            raise ValueError("Session data is required")
        if not report_data:
            raise ValueError("Report data is required")
        
        # Prepare data with validation
        meta = session_data.get("meta", {})
        candidate_name = meta.get("name", "Anonymous")
        role = meta.get("role", "Unknown Role")
        domain = meta.get("domain", "General")
        experience = meta.get("experience", "Unknown")
        mode = meta.get("mode", "technical").title()
        questions = session_data.get("questions", [])
        answers = session_data.get("answers", [])
        
        if not questions:
            raise ValueError("No questions found in session data")
        if not answers:
            raise ValueError("No answers found in session data")
        
        # Generate filename and filepath
        filename = f"interview_report_{candidate_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4, 
                                  rightMargin=72, leftMargin=72, 
                                  topMargin=72, bottomMargin=18)
            
            # Build content
            story = []
            
            # Title
            story.append(Paragraph("AI Interview Report", self.styles['CustomTitle']))
            story.append(Spacer(1, 12))
            
            # Candidate info
            story.append(Paragraph(f"<b>Candidate:</b> {candidate_name}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Role:</b> {role}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Domain:</b> {domain}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Experience:</b> {experience}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Interview Mode:</b> {mode}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Overall Performance Section
            story.append(Paragraph("Overall Performance", self.styles['CustomHeading1']))
            story.append(Spacer(1, 12))
            
            # Create scores table
            scores_data = [
                ['Metric', 'Score'],
                ['Overall Score', f"{report_data.get('overall_score', 0):.1f}/10"],
                ['Technical', f"{report_data.get('avg_technical', 0):.1f}/10"],
                ['Communication', f"{report_data.get('avg_communication', 0):.1f}/10"],
                ['Confidence', f"{report_data.get('avg_confidence', 0):.1f}/10"]
            ]
            
            scores_table = Table(scores_data, colWidths=[2*inch, 1.5*inch])
            scores_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(scores_table)
            story.append(Spacer(1, 20))
            
            # Questions and Answers Section
            story.append(Paragraph("Interview Questions & Answers", self.styles['CustomHeading1']))
            story.append(Spacer(1, 12))
            
            for answer in answers:
                # Find the corresponding question
                question = next((q for q in questions if q["id"] == answer["question_id"]), None)
                
                if question:
                    # Question header with scores
                    eval_data = answer.get("evaluation", {})
                    scores = eval_data.get("scores", {})
                    
                    question_header = f"<b>Question {answer['question_id']}</b>"
                    if scores:
                        question_header += f" | Technical: {scores.get('technical', 0)}/10 | Communication: {scores.get('communication', 0)}/10 | Confidence: {scores.get('confidence', 0)}/10"
                    
                    story.append(Paragraph(question_header, self.styles['CustomHeading2']))
                    story.append(Spacer(1, 6))
                    
                    # Question text
                    story.append(Paragraph(f"<b>Question:</b> {question['question']}", self.styles['Question']))
                    story.append(Spacer(1, 6))
                    
                    # Answer
                    story.append(Paragraph(f"<b>Your Answer:</b>", self.styles['Normal']))
                    story.append(Paragraph(answer['answer'], self.styles['Answer']))
                    story.append(Spacer(1, 6))
                    
                    # Feedback
                    if eval_data.get('feedback'):
                        story.append(Paragraph(f"<b>AI Feedback:</b>", self.styles['Normal']))
                        story.append(Paragraph(eval_data['feedback'], self.styles['Feedback']))
                        story.append(Spacer(1, 6))
                    
                    # Improvement suggestions
                    if eval_data.get('examples_or_corrections'):
                        story.append(Paragraph(f"<b>Suggested Improvement:</b>", self.styles['Normal']))
                        story.append(Paragraph(eval_data['examples_or_corrections'], self.styles['Feedback']))
                        story.append(Spacer(1, 6))
                    
                    story.append(Spacer(1, 12))
            
            # Resources Section
            resources = report_data.get("resources", [])
            if resources:
                story.append(Paragraph("Recommended Resources", self.styles['CustomHeading1']))
                story.append(Spacer(1, 12))
                
                for resource in resources:
                    story.append(Paragraph(f"• {resource}", self.styles['Normal']))
                    story.append(Spacer(1, 4))
            
            # Footer
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"Generated by AI Interview Prep Bot on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                                 self.styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            # Verify file was created
            if not os.path.exists(filepath):
                raise RuntimeError("PDF file was not created successfully")
            
            return filepath
        except (OSError, IOError) as e:
            raise RuntimeError(f"File system error while generating PDF: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to generate PDF: {str(e)}")
    
    def generate_summary_pdf(self, session_data: Dict[str, Any], report_data: Dict[str, Any]) -> str:
        """Generate a concise summary PDF."""
        
        # Validate input data
        if not session_data:
            raise ValueError("Session data is required")
        if not report_data:
            raise ValueError("Report data is required")
        
        # Prepare data with validation
        meta = session_data.get("meta", {})
        candidate_name = meta.get("name", "Anonymous")
        role = meta.get("role", "Unknown Role")
        mode = meta.get("mode", "technical").title()
        
        # Generate filename and filepath
        filename = f"interview_summary_{candidate_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4, 
                                  rightMargin=72, leftMargin=72, 
                                  topMargin=72, bottomMargin=18)
            
            # Build content
            story = []
            
            # Title
            story.append(Paragraph("Interview Summary", self.styles['CustomTitle']))
            story.append(Spacer(1, 12))
            
            # Candidate info
            story.append(Paragraph(f"<b>Candidate:</b> {candidate_name}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Role:</b> {role}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Mode:</b> {mode}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Performance Overview
            story.append(Paragraph("Performance Overview", self.styles['CustomHeading1']))
            story.append(Spacer(1, 12))
            
            # Overall score (highlighted)
            overall_score = report_data.get('overall_score', 0)
            story.append(Paragraph(f"<b>Overall Score: {overall_score:.1f}/10</b>", self.styles['CustomHeading1']))
            story.append(Spacer(1, 12))
            
            # Detailed scores table
            scores_data = [
                ['Metric', 'Score'],
                ['Technical', f"{report_data.get('avg_technical', 0):.1f}/10"],
                ['Communication', f"{report_data.get('avg_communication', 0):.1f}/10"],
                ['Confidence', f"{report_data.get('avg_confidence', 0):.1f}/10"]
            ]
            
            scores_table = Table(scores_data, colWidths=[2*inch, 1.5*inch])
            scores_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(scores_table)
            story.append(Spacer(1, 20))
            
            # Session Details
            story.append(Paragraph("Session Details", self.styles['CustomHeading1']))
            story.append(Spacer(1, 12))
            
            session_details = [
                ['Questions Answered', str(report_data.get('n_questions', 0))],
                ['Interview Mode', mode],
                ['Target Role', role]
            ]
            
            details_table = Table(session_details, colWidths=[2*inch, 2*inch])
            details_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(details_table)
            story.append(Spacer(1, 20))
            
            # Resources Section
            resources = report_data.get("resources", [])
            if resources:
                story.append(Paragraph("Key Resources", self.styles['CustomHeading1']))
                story.append(Spacer(1, 12))
                
                for resource in resources:
                    story.append(Paragraph(f"• {resource}", self.styles['Normal']))
                    story.append(Spacer(1, 4))
            
            # Footer
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"Generated by AI Interview Prep Bot on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                                 self.styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            # Verify file was created
            if not os.path.exists(filepath):
                raise RuntimeError("Summary PDF file was not created successfully")
            
            return filepath
        except (OSError, IOError) as e:
            raise RuntimeError(f"File system error while generating summary PDF: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to generate summary PDF: {str(e)}")
    
    def get_pdf_as_base64(self, filepath: str) -> str:
        """Convert PDF file to base64 string for download."""
        try:
            with open(filepath, 'rb') as pdf_file:
                pdf_data = pdf_file.read()
                return base64.b64encode(pdf_data).decode('utf-8')
        except Exception as e:
            raise Exception(f"Failed to read PDF file: {str(e)}")
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """Clean up old PDF files to save disk space."""
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        try:
            for filename in os.listdir(self.output_dir):
                if filename.endswith('.pdf'):
                    filepath = os.path.join(self.output_dir, filename)
                    file_age = current_time - os.path.getctime(filepath)
                    if file_age > max_age_seconds:
                        os.remove(filepath)
        except Exception as e:
            print(f"Warning: Failed to cleanup old files: {str(e)}")
