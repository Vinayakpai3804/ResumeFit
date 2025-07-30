import streamlit as st

def load_modern_professional_css():
    """Advanced professional CSS with fixed header sizing and proper grid rendering"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');
    
    /* CSS Variables for Professional Dashboard */
    :root {
        --primary-blue: #2563eb;
        --secondary-blue: #3b82f6;
        --accent-blue: #60a5fa;
        --success-green: #10b981;
        --warning-amber: #f59e0b;
        --error-red: #ef4444;
        --dark-slate: #0f172a;
        --medium-slate: #1e293b;
        --light-slate: #334155;
        --surface-slate: #475569;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --border-color: #374151;
        --surface-elevated: rgba(71, 85, 105, 0.3);
        --gradient-primary: linear-gradient(135deg, #2563eb 0%, #3b82f6 50%, #60a5fa 100%);
        --gradient-success: linear-gradient(135deg, #059669 0%, #10b981 100%);
        --gradient-warning: linear-gradient(135deg, #d97706 0%, #f59e0b 100%);
        --gradient-error: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    /* Global Application Styling */
    .stApp {
        background: linear-gradient(135deg, var(--dark-slate) 0%, #1a202c 50%, var(--dark-slate) 100%);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main .block-container {
        max-width: 1400px;
        padding: 1.5rem 1rem;
    }
    
    /* Professional Sidebar Design */
    .css-1d391kg, .css-1lcbmhc {
        background: var(--medium-slate);
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--border-color);
    }
    
    .sidebar-brand {
        background: var(--gradient-primary);
        color: white;
        padding: 1.5rem;
        margin: -1rem -1.5rem 2rem -1.5rem;
        border-radius: 0 0 16px 16px;
        text-align: center;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-brand::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='7' cy='7' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
        opacity: 0.3;
    }
    
    .sidebar-brand h1 {
        margin: 0;
        font-size: 1.6rem;
        font-weight: 800;
        position: relative;
        z-index: 2;
    }
    
    .sidebar-brand p {
        margin: 0.5rem 0 0 0;
        font-size: 0.85rem;
        opacity: 0.9;
        position: relative;
        z-index: 2;
    }
    
    .sidebar-brand .icon {
        font-size: 2.5rem;
        display: block;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .nav-section {
        background: var(--light-slate);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .nav-section:hover {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 1px var(--primary-blue), var(--shadow-md);
    }
    
    .nav-section h3 {
        color: var(--text-primary);
        font-size: 1rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Compact Header - Made Smaller */
    .main-header {
        background: var(--gradient-primary);
        padding: 2rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shine 4s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 500;
        position: relative;
        z-index: 2;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Upload Section Design */
    .upload-section {
        background: var(--medium-slate);
        border: 2px solid var(--border-color);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: var(--shadow-lg);
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 1px var(--primary-blue), var(--shadow-xl);
    }
    
    .upload-section h2 {
        color: var(--primary-blue);
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
    }
    
    .section-divider {
        background: var(--medium-slate);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: var(--shadow-md);
    }
    
    .section-divider h3 {
        color: var(--text-primary);
        font-size: 1.3rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Enhanced Input Controls */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--dark-slate) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 1rem 1.25rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
    }
    
    .stTextInput label,
    .stTextArea label {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    /* Enhanced File Uploader */
    .stFileUploader {
        background: var(--light-slate);
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid var(--border-color);
    }
    
    .stFileUploader > div {
        background: var(--dark-slate) !important;
        border-radius: 16px !important;
        border: 2px dashed var(--border-color) !important;
        padding: 2.5rem 2rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--primary-blue) !important;
        background: rgba(37, 99, 235, 0.05) !important;
    }
    
    /* Professional Button Styling */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: var(--shadow-md) !important;
        text-transform: none !important;
        letter-spacing: 0.025em !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-xl) !important;
        filter: brightness(1.1) !important;
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: var(--medium-slate);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }
    
    .metric-card.blue::before {
        background: var(--gradient-primary);
    }
    
    .metric-card.green::before {
        background: var(--gradient-success);
    }
    
    .metric-card.amber::before {
        background: var(--gradient-warning);
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        border-color: var(--primary-blue);
        box-shadow: var(--shadow-xl);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
        position: relative;
        z-index: 2;
    }
    
    .metric-value.blue {
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-value.green {
        background: var(--gradient-success);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-value.amber {
        background: var(--gradient-warning);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 1rem;
        color: var(--text-muted);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Status Messages */
    .success-message {
        background: var(--gradient-success);
        color: white;
        padding: 1.25rem 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        font-weight: 600;
        box-shadow: var(--shadow-lg);
        border-left: 4px solid #34d399;
    }
    
    .error-message {
        background: var(--gradient-error);
        color: white;
        padding: 1.25rem 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        font-weight: 600;
        box-shadow: var(--shadow-lg);
        border-left: 4px solid #f87171;
    }
    
    .warning-message {
        background: var(--gradient-warning);
        color: white;
        padding: 1.25rem 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        font-weight: 600;
        box-shadow: var(--shadow-lg);
        border-left: 4px solid #fbbf24;
    }
    
    .info-message {
        background: var(--light-slate);
        color: var(--text-primary);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-md);
        border-left: 4px solid var(--primary-blue);
    }
    
    /* Welcome Container - Using Streamlit Native Components */
    .welcome-title {
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        font-size: 1.2rem;
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Enhanced Chat Interface */
    .chat-message-user {
        background: var(--gradient-primary);
        color: white;
        padding: 1.25rem 1.75rem;
        border-radius: 20px 20px 8px 20px;
        margin: 1rem 0 1rem auto;
        max-width: 85%;
        box-shadow: var(--shadow-md);
        animation: slideInRight 0.4s ease-out;
    }
    
    .chat-message-assistant {
        background: var(--medium-slate);
        color: var(--text-secondary);
        padding: 1.25rem 1.75rem;
        border-radius: 20px 20px 20px 8px;
        margin: 1rem auto 1rem 0;
        max-width: 85%;
        box-shadow: var(--shadow-md);
        border-left: 4px solid var(--success-green);
        animation: slideInLeft 0.4s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Tab Enhancement */
    .stTabs > div > div > div > div {
        background: var(--light-slate);
        color: var(--text-secondary);
        border-radius: 12px 12px 0 0;
        border: 1px solid var(--border-color);
        font-weight: 600;
        padding: 1rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs > div > div > div > div[aria-selected="true"] {
        background: var(--primary-blue);
        color: white;
        border-color: var(--primary-blue);
    }
    
    /* Card Styling for Step Cards */
    .step-card {
        background: var(--medium-slate);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
        position: relative;
    }
    
    .step-card:hover {
        transform: translateY(-4px);
        border-color: var(--primary-blue);
        box-shadow: var(--shadow-lg);
    }
    
    .step-number {
        background: var(--gradient-primary);
        color: white;
        width: 3rem;
        height: 3rem;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem 1rem;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
        
        .upload-section {
            padding: 1.5rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .chat-message-user,
        .chat-message-assistant {
            max-width: 95%;
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
