import io
from unittest.mock import AsyncMock, patch

import docx
import PyPDF2
import pytest

from api.utils.text_processing import extract_text_from_file


@pytest.mark.asyncio
async def test_extract_text_from_txt_file():
    # Mock the file
    mock_file = AsyncMock()
    mock_file.filename = "test.txt"
    mock_file.read = AsyncMock(return_value=b"This is a text file.")

    # Call the function
    result = await extract_text_from_file(mock_file)

    # Assert that the text is returned correctly
    assert result == "This is a text file."


@pytest.mark.asyncio
async def test_extract_text_from_pdf_file():
    # Mock the file
    mock_file = AsyncMock()
    mock_file.filename = "test.pdf"

    # Create a mock PDF content with PyPDF2
    mock_pdf_content = io.BytesIO()
    mock_pdf_writer = PyPDF2.PdfWriter()
    mock_pdf_writer.add_blank_page(width=72, height=72)
    mock_pdf_writer.write(mock_pdf_content)

    mock_file.read = AsyncMock(return_value=mock_pdf_content.getvalue())

    with patch(
        "api.utils.text_processing.extract_text_from_pdf", return_value="Mock PDF text"
    ):
        # Call the function
        result = await extract_text_from_file(mock_file)

        # Assert that the PDF text is returned correctly
        assert result == "Mock PDF text"


@pytest.mark.asyncio
async def test_extract_text_from_docx_file():
    # Mock the file
    mock_file = AsyncMock()
    mock_file.filename = "test.docx"

    # Create a mock DOCX content with docx.Document
    mock_docx_content = io.BytesIO()
    doc = docx.Document()
    doc.add_paragraph("This is a test DOCX file.")
    doc.save(mock_docx_content)

    mock_file.read = AsyncMock(return_value=mock_docx_content.getvalue())

    with patch(
        "api.utils.text_processing.extract_text_from_docx",
        return_value="Mock DOCX text",
    ):
        # Call the function
        result = await extract_text_from_file(mock_file)

        # Assert that the DOCX text is returned correctly
        assert result == "Mock DOCX text"


@pytest.mark.asyncio
async def test_extract_text_from_unsupported_file():
    # Mock the file
    mock_file = AsyncMock()
