import win32com.client
import os
from openpyxl import Workbook
from docx import Document

def check_outlook_inbox(limit=5):
    """Read top emails from Outlook inbox."""
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # Inbox
    messages = inbox.Items
    emails = []
    for i, message in enumerate(messages, start=1):
        if i > limit:
            break
        emails.append(f"From: {message.SenderName}, Subject: {message.Subject}")
    return emails

def create_excel(file_path="example.xlsx"):
    """Create a sample Excel file."""
    wb = Workbook()
    ws = wb.active
    if ws is None:
        ws = wb.create_sheet()
    ws['A1'] = "Hello"
    ws['B1'] = "World"
    wb.save(file_path)
    return f"Excel file created at {file_path}"

def create_word_doc(file_path="example.docx", text="Hello from AI Agent!"):
    """Create a sample Word document."""
    doc = Document()
    doc.add_paragraph(text)
    doc.save(file_path)
    return f"Word document created at {file_path}"

def open_app(app_name="notepad.exe"):
    """Open a local application."""
    os.startfile(app_name)
    return f"Opened {app_name}"
