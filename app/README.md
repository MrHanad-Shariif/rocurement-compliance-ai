# 🏢 Procurement Compliance AI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A sophisticated AI-powered FastAPI application designed to streamline procurement processes by validating Purchase Requisitions (PR) against compliance rules and automatically generating Request for Quotation (RFQ) PDFs.

## 🚀 Features

- **AI-Powered Validation**: Intelligent validation of purchase requisitions using spaCy NLP
- **Compliance Checking**: Automated compliance rule enforcement
- **PDF Generation**: Dynamic RFQ PDF creation
- **Multi-Entity Support**: Support for multiple legal entities
- **Web Dashboard**: User-friendly web interface for managing procurement
- **Authentication System**: Secure user authentication and authorization
- **Real-time Processing**: Live validation and feedback

## 🛠️ Technology Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for building APIs
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - SQL toolkit and Object-Relational Mapping
- **[PostgreSQL](https://www.postgresql.org/)** - Advanced open source relational database
- **[spaCy](https://spacy.io/)** - Industrial-strength Natural Language Processing
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server

### Frontend
- **[Jinja2](https://jinja.palletsprojects.com/)** - Modern templating engine
- **HTML5/CSS3** - Modern web standards
- **JavaScript** - Interactive user interface

### Additional Libraries
- **[FPDF](https://pyfpdf.readthedocs.io/)** - PDF generation
- **[Passlib](https://passlib.readthedocs.io/)** - Password hashing
- **[Python-dotenv](https://python-dotenv.readthedocs.io/)** - Environment variable management

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** ([Download Python](https://python.org/downloads/))
- **pip** (Python package installer)
- **Git** ([Download Git](https://git-scm.com/downloads))
- **PostgreSQL** (Optional: for production database)

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/MrHanad-Shariif/rocurement-compliance-ai.git
cd rocurement-compliance-ai
```

### 2. Create and Activate Virtual Environment

#### 🐧 Linux / 🍎 macOS

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### 🪟 Windows

**Command Prompt:**
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat
```

**PowerShell:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**Note for Windows PowerShell users:** If you encounter execution policy restrictions, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies

```bash
# Navigate to app directory
cd app

# Install Python packages
pip install -r requirements.txt
```

### 4. Download spaCy Language Model

```bash
# Download English language model for NLP processing
python -m spacy download en_core_web_sm
```

### 5. Environment Configuration

Create a `.env` file in the `app` directory with your configuration:

```bash
# Copy example environment file (if available)
cp .env.example .env

# Edit the .env file with your settings
```

Example `.env` configuration:
```env
DATABASE_URL=postgresql://username:password@localhost/procurement_db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 6. Database Setup (Optional)

If using PostgreSQL:

```bash
# Create database tables
python create_tables.py
```

## 🚀 Running the Application

### Development Mode

#### 🐧 Linux / 🍎 macOS

```bash
# Start the development server
uvicorn main:app --reload --port 8080

# Alternative with host specification
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

#### 🪟 Windows

```cmd
# Start the development server
uvicorn main:app --reload --port 8080

# Alternative with host specification
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### Production Mode

```bash
# Start production server
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
```

## 🌐 Accessing the Application

Once the server is running, access the application at:

- **Local Development**: [http://localhost:8080](http://localhost:8080)
- **Network Access**: [http://your-ip-address:8080](http://your-ip-address:8080)

The application will automatically redirect to the dashboard at `/dashboard`.

## 📖 API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc**: [http://localhost:8080/redoc](http://localhost:8080/redoc)

## 🔍 Usage

1. **Access Dashboard**: Navigate to the application URL
2. **Create Purchase Requisition**: Use the PR creation form
3. **AI Validation**: The system automatically validates against compliance rules
4. **Review Results**: Check validation results and compliance status
5. **Generate RFQ**: Create PDF documents for approved requisitions

## 🛡️ Security Features

- Password hashing with bcrypt
- Session-based authentication
- Input validation and sanitization
- SQL injection prevention through SQLAlchemy ORM

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**spaCy model not found:**
```bash
python -m spacy download en_core_web_sm
```

**Port already in use:**
```bash
# Use a different port
uvicorn main:app --reload --port 8081
```

**Virtual environment issues:**
```bash
# Deactivate and recreate
deactivate
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows
python -m venv venv
```

## 📞 Support

For support and questions:
- Create an issue on [GitHub Issues](https://github.com/MrHanad-Shariif/rocurement-compliance-ai/issues)
- Contact: [hanadshariif18@gmail.com]

---

**Made with ❤️ for efficient procurement management**
