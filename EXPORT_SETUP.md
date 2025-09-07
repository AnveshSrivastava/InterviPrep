# 📄 PDF Export Functionality Setup Guide

This guide explains how to set up and use the PDF export functionality for the AI Interview Prep application.

## 🚀 Quick Setup

### 1. Install Dependencies

The export functionality requires additional Python packages. Install them using:

```bash
pip install -r requirements.txt
```

**New dependencies added:**
- `weasyprint` - For HTML to PDF conversion
- `reportlab` - Alternative PDF generation library
- `python-multipart` - For file uploads in FastAPI

### 2. System Requirements

**For WeasyPrint (recommended):**
- **Windows**: No additional setup required
- **macOS**: Install system dependencies:
  ```bash
  brew install cairo pango gdk-pixbuf libffi
  ```
- **Linux**: Install system dependencies:
  ```bash
  sudo apt-get install python3-dev python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
  ```

### 3. Directory Structure

The export functionality creates the following directories:
```
InterviPrep/
├── exports/                 # Generated PDF files (auto-created)
├── backend/
│   ├── templates/          # HTML templates (auto-created)
│   └── services/
│       └── pdf_service.py  # PDF generation service
└── test_export.py          # Test script
```

## 🎯 Features

### Export Options

1. **Full Report PDF** (`/session/{id}/export/full`)
   - Complete interview with all questions and answers
   - Detailed AI feedback for each response
   - Suggested improvements and examples
   - Recommended resources
   - Professional formatting with scores

2. **Summary Report PDF** (`/session/{id}/export/summary`)
   - Concise overview of performance
   - Overall scores and breakdown
   - Key recommendations
   - Session details

3. **Base64 Export** (`/session/{id}/export/full/base64`)
   - Returns PDF as base64 string
   - Useful for web applications
   - No temporary files created

4. **Print-Friendly View**
   - Browser-based PDF viewer
   - Direct printing capability
   - No download required

### Frontend Integration

The Streamlit frontend now includes:
- **Download Full Report** button
- **Download Summary** button  
- **Print Report** button
- **New Session** button
- Export instructions and help text

## 🧪 Testing

### Manual Testing

1. **Start the backend server:**
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

2. **Start the frontend:**
   ```bash
   cd frontend
   streamlit run app.py
   ```

3. **Complete an interview session:**
   - Fill out the interview form
   - Answer all questions
   - Click "Finish & Get Report"
   - Use the export buttons

### Automated Testing

Run the test script to verify all export functionality:

```bash
python test_export.py
```

This script will:
- Create a test session
- Submit sample answers
- Finalize the session
- Test all export endpoints
- Verify PDF generation

## 📋 API Endpoints

### Export Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/session/{id}/export/full` | GET | Download complete report PDF |
| `/session/{id}/export/summary` | GET | Download summary PDF |
| `/session/{id}/export/full/base64` | GET | Get full report as base64 |
| `/session/{id}/export/summary/base64` | GET | Get summary as base64 |

### Example Usage

```python
import requests

# Download full report
response = requests.get("http://localhost:8000/interview/session/{session_id}/export/full")
with open("report.pdf", "wb") as f:
    f.write(response.content)

# Get base64 report
response = requests.get("http://localhost:8000/interview/session/{session_id}/export/full/base64")
pdf_data = response.json()
```

## 🎨 PDF Styling

The PDF reports include:
- **Professional header** with candidate information
- **Score visualization** with color-coded metrics
- **Question blocks** with clear formatting
- **Feedback sections** with improved examples
- **Resource recommendations** with icons
- **Print-friendly** layout and typography

### Customization

To customize PDF styling, edit the CSS in `backend/services/pdf_service.py`:
- Modify the `_get_pdf_css()` method
- Update colors, fonts, and layout
- Add company branding or logos

## 🔧 Troubleshooting

### Common Issues

1. **WeasyPrint Installation Issues**
   ```bash
   # Try alternative installation
   pip install --upgrade weasyprint
   # Or use reportlab instead
   pip install reportlab
   ```

2. **Permission Errors**
   - Ensure the `exports/` directory is writable
   - Check file permissions on the backend directory

3. **Memory Issues with Large Reports**
   - The system automatically cleans up old files
   - Adjust `max_age_hours` in `cleanup_old_files()`

4. **Font Issues**
   - WeasyPrint includes fallback fonts
   - Custom fonts can be added to the CSS

### Error Handling

The export functionality includes comprehensive error handling:
- Graceful fallbacks for PDF generation failures
- Clear error messages in the frontend
- Automatic cleanup of temporary files
- Validation of session completion before export

## 📈 Performance

### Optimization Features

- **Lazy loading** of PDF generation
- **Automatic cleanup** of old files
- **Efficient HTML templating** with Jinja2
- **Base64 encoding** for web delivery
- **Streaming responses** for large files

### File Management

- PDFs are stored in the `exports/` directory
- Automatic cleanup removes files older than 24 hours
- Unique filenames prevent conflicts
- Base64 exports don't create permanent files

## 🚀 Production Deployment

### Environment Variables

Add these to your production environment:
```bash
# Optional: Custom PDF output directory
PDF_OUTPUT_DIR=/path/to/exports

# Optional: Custom template directory  
PDF_TEMPLATE_DIR=/path/to/templates
```

### Security Considerations

- Validate session IDs before export
- Implement rate limiting for export endpoints
- Consider authentication for sensitive reports
- Sanitize user input in PDF content

### Scaling

For high-traffic deployments:
- Use a dedicated file storage service (S3, etc.)
- Implement PDF caching
- Consider async PDF generation
- Use a CDN for PDF delivery

## 📚 Additional Resources

- [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/)
- [Jinja2 Template Engine](https://jinja.palletsprojects.com/)
- [FastAPI File Responses](https://fastapi.tiangolo.com/tutorial/request-files/)
- [Streamlit Download Button](https://docs.streamlit.io/library/api-reference/widgets/st.download_button)

---

**Note**: The export functionality is fully integrated and ready to use. All dependencies are included in the updated `requirements.txt` file.
