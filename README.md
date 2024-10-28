# Project Description

**Project Description: Document Analyzer and Organizer**

**Overview:**
This project is a Python-based Document Analyzer and Organizer, designed to efficiently categorize and organize various types of documents using OpenAI GPT models for text analysis. The application leverages a graphical user interface (GUI) built with Tkinter to facilitate user interaction, allowing users to select input and output directories easily.

**Key Features:**

1. **File Type Handling:**
   - Supports text extraction from multiple file types including PDF, DOCX, Excel, TXT, HTML, CSS, JS, and more.
   - Utilizes the PyPDF2 library for PDF processing, docx for Word documents, and pandas for Excel files.

2. **AI-Powered Analysis:**
   - Leverages OpenAI's GPT-4 model to analyze extracted text and suggest appropriate categories and brief descriptions for the documents.
   - Automatically handles long texts by breaking them into manageable chunks for analysis.

3. **File Organization:**
   - Organizes files into categorized folders within a specified output directory.
   - Ensures that files are placed in existing categorized folders if they match, otherwise creates new folders.
   - Limits and sanitizes filenames and paths to ensure compatibility with file system constraints.

4. **User Interface:**
   - Interactive GUI for easy folder selection and instruction input.
   - Users can provide optional custom instructions to tailor the analysis process.

5. **Error Handling and Robustness:**
   - Implements retry mechanisms for API requests to OpenAI, enhancing robustness against temporary failures.
   - Includes comprehensive error handling for file operations to ensure seamless execution.

**Technical Details:**
- **Programming Language:** Python
- **Libraries and Frameworks:** Tkinter, PyPDF2, docx, pandas, OpenAI's API, mimetypes, and more.
- **File Operations:** Uses `os` and `shutil` for file and directory management.
- **Natural Language Processing:** Integrates OpenAI's GPT for advanced text analysis and categorization.

**Potential Use Cases:**
- Automating document classification in corporate settings.
- Creating organized digital archives for easier retrieval of documents.
- Reducing manual effort in sorting and describing collections of diverse file types.

**Setup and Execution:**
1. Users need an API key from OpenAI to enable text analysis features.
2. Execute the script to open the GUI, select input/output directories, and optionally provide analysis instructions.
3. The program processes and organizes the documents, displaying a completion message upon finishing.

Overall, this project serves as a powerful tool for document management, offering seamless integration of AI capabilities for enhancing productivity and organization.
