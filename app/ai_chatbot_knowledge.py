# Help assistant knowledge base for Procurement Compliance AI chatbot
knowledge_base = [
    # Friendly conversational/assistant entries
    {
        "keywords": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"],
        "answer": "Hello! 👋 I'm your Procurement Compliance AI Assistant. How can I help you today?"
    },
    {
        "keywords": ["help", "help me", "assist", "support", "stuck", "confused"],
        "answer": "I'm here to help! Please describe your issue or what you're trying to do in the Procurement Compliance AI system. I can guide you through PRs, vendors, errors, and more."
    },
    {
        "keywords": ["thank you", "thanks", "appreciate"],
        "answer": "You're welcome! 😊 If you have more questions or need help, just ask."
    },
    {
        "keywords": ["who are you", "what can you do", "your name", "about you"],
        "answer": "I'm your friendly Procurement Compliance AI Assistant. I can help you with anything related to the system: PRs, vendors, troubleshooting, and best practices."
    },
    # System overview
    {
        "keywords": ["what is procurement compliance ai", "about procurement compliance ai", "system overview", "platform"],
        "answer": "Procurement Compliance AI is a web-based platform designed to streamline, automate, and ensure compliance in the procurement process for organizations. It uses AI to validate purchase requisitions, manage vendors, generate RFQ/RFP documents, and maintain audit trails, all while ensuring adherence to organizational and regulatory policies."
    },
    # Key features
    {
        "keywords": ["features", "key features", "capabilities", "what can it do"],
        "answer": "Key features include: 1) Purchase Requisition (PR) Management, 2) Vendor Management, 3) AI Validation, 4) RFQ/RFP Generation, 5) Automated Email Notifications, 6) User Roles and Access Control, 7) Dashboard and Reporting."
    },
    # PR Management
    {
        "keywords": ["create pr", "add pr", "new pr", "purchase requisition", "how to pr", "pr management"],
        "answer": "To create a new Purchase Requisition (PR), click the 'Add New PR' button on the PR Table page. Fill in the legal entity, select one or more vendors, add item details, and submit. The AI will validate your request for completeness and compliance."
    },
    # Vendor Management
    {
        "keywords": ["add vendor", "new vendor", "create vendor", "vendor management"],
        "answer": "Admins can add, edit, and remove vendors. Each vendor has a name, email, and preferred language. Vendors can be selected for PRs and notified automatically. To add a new vendor, go to the Vendors page (admins only), click 'Add Vendor,' and fill in the required details."
    },
    # AI Validation
    {
        "keywords": ["ai validation", "validate", "check pr", "compliance", "validation fail", "validation error"],
        "answer": "The AI agent checks PRs for: valid legal entity, approved item types, reasonable quantities, and clear descriptions. If validation fails, you'll get a detailed error message."
    },
    # RFQ/RFP Generation
    {
        "keywords": ["rfq", "rfp", "generate document", "send to vendor", "quotation", "proposal"],
        "answer": "You can generate RFQ (Request for Quotation) or RFP (Request for Proposal) documents from the PR Table. Select the PR, choose the document type, and vendors will be notified automatically. Documents are generated as PDFs and can be downloaded or sent to vendors in their preferred language."
    },
    # Automated Email Notifications
    {
        "keywords": ["email notification", "vendor email", "notify vendor", "send email"],
        "answer": "When an RFQ or RFP is generated, selected vendors receive an email with the document attached, in their preferred language."
    },
    # User Roles and Access Control
    {
        "keywords": ["role", "admin", "user", "permission", "access", "who can manage"],
        "answer": "The system supports different user roles (admin, user). Only admins can manage vendors and users. If you need access, contact your administrator."
    },
    # Dashboard and Reporting
    {
        "keywords": ["dashboard", "report", "status", "pr status", "download documents", "zip"],
        "answer": "You can view the status of all PRs (pending, approved, rejected) on the dashboard. To download all generated documents, click the 'Download All PDFs' button on the PR Table page."
    },
    # Troubleshooting and error messages
    {
        "keywords": ["error", "issue", "problem", "not working", "failed", "can't", "cannot", "troubleshoot"],
        "answer": "I'm sorry you're having trouble. Please tell me the error message or describe the problem, and I'll do my best to help you solve it! Common issues include: missing required fields, invalid data, or lack of permissions."
    },
    {
        "keywords": ["legal entity is required", "missing legal entity"],
        "answer": "Make sure you have selected a legal entity from the dropdown."
    },
    {
        "keywords": ["at least one vendor must be selected", "missing vendor", "no vendor selected"],
        "answer": "Use the vendor selection dropdown to choose one or more vendors."
    },
    {
        "keywords": ["item type is required", "missing item type"],
        "answer": "Select an item type from the approved list."
    },
    {
        "keywords": ["quantity must be at least 1", "invalid quantity"],
        "answer": "Enter a valid quantity greater than zero."
    },
    {
        "keywords": ["do not have permission", "permission denied", "access denied", "not allowed"],
        "answer": "Only admins can access this feature. If you need access, please contact your administrator."
    },
    {
        "keywords": ["invalid or expired token", "reset password", "forgot password", "change password"],
        "answer": "If resetting your password, the link may have expired. Try again. To reset your password, click 'Forgot Password' on the login page and follow the instructions."
    },
    # Best practices
    {
        "keywords": ["best practice", "tips", "recommend", "how to use", "suggestion"],
        "answer": "Here are some best practices: Always provide clear and detailed descriptions for items in PRs. Select all relevant vendors to ensure competitive quotations. Keep vendor information up to date. Regularly check the dashboard for PR status and compliance alerts."
    },
    # About the chatbot
    {
        "keywords": ["about chatbot", "what is this", "what is the chatbot for", "purpose chatbot"],
        "answer": "This chatbot is designed to answer questions only about the Procurement Compliance AI system. For questions outside this system, please contact your administrator."
    },
    # Fallback
    {
        "keywords": [],
        "answer": "I'm here to help with anything about Procurement Compliance AI. Please ask your question or describe your issue!"
    }
] 