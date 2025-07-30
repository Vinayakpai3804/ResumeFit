FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install complete LaTeX distribution
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-lang-english \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "resume_analyser.py", "--server.port=8501", "--server.address=0.0.0.0"]
