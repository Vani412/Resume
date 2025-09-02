import streamlit as st
import base64
from io import BytesIO
from text_extractor import TextExtractor
from resume_scorer import ResumeScorer

# Page configuration
st.set_page_config(
    page_title="Resume Scorer - AI-Powered Resume Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for minimalist professional styling  
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 1px solid #e2e8f0;
        padding: 3rem 2rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: #1a202c;
        font-size: 2.5rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.025em;
    }
    
    .main-header p {
        color: #64748b;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a202c;
        margin: 2rem 0 1rem 0;
        letter-spacing: -0.025em;
    }
    
    .score-card {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 2rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .score-number {
        font-size: 3rem;
        font-weight: 700;
        color: #1a202c;
        line-height: 1;
    }
    
    .score-text {
        color: #64748b;
        font-size: 0.875rem;
        margin-top: 0.5rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .metric-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-score {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a202c;
        margin-bottom: 0.75rem;
    }
    
    .progress-bar {
        width: 100%;
        height: 4px;
        background-color: #f1f5f9;
        border-radius: 2px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: #1a202c;
        border-radius: 2px;
        transition: width 0.8s ease;
    }
    
    .feedback-section {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .strength-item {
        background: #f0fdf4;
        border: 1px solid #dcfce7;
        border-radius: 6px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        color: #166534;
        font-size: 0.875rem;
    }
    
    .improvement-item {
        background: #fffbeb;
        border: 1px solid #fed7aa;
        border-radius: 6px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        color: #9a3412;
        font-size: 0.875rem;
    }
    
    .keyword-tag {
        display: inline-block;
        background: #f1f5f9;
        color: #334155;
        border: 1px solid #e2e8f0;
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        margin: 0.25rem;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .grammar-correction {
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 6px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        color: #0c4a6e;
        font-size: 0.875rem;
    }
    
    .word-count-section {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .word-count-good {
        color: #166534;
        font-weight: 600;
    }
    
    .word-count-warning {
        color: #9a3412;
        font-weight: 600;
    }
    
    .improvement-suggestion {
        background: #f8fafc;
        border-left: 3px solid #64748b;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 6px 6px 0;
        color: #334155;
        font-size: 0.875rem;
    }
    
    .stButton > button {
        background: #1a202c;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: #374151;
    }
    
    .stSelectbox > div > div {
        border-radius: 6px;
        border: 1px solid #d1d5db;
    }
    
    .stRadio > div {
        border-radius: 6px;
        padding: 1rem;
        border: 1px solid #e5e7eb;
        background: white;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state variables
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'category' not in st.session_state:
        st.session_state.category = None
    if 'domain' not in st.session_state:
        st.session_state.domain = None
    if 'resume_uploaded' not in st.session_state:
        st.session_state.resume_uploaded = False

    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>Resume Scorer</h1>
        <p>AI-Powered Professional Resume Analysis & Optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress indicator
    progress_steps = ["Category Selection", "Domain Selection", "Resume Upload & Analysis"]
    current_step = st.session_state.step
    
    progress_html = '<div style="display: flex; justify-content: space-between; margin: 20px 0;">'
    for i, step_name in enumerate(progress_steps, 1):
        if i <= current_step:
            progress_html += f'<div style="background: #4CAF50; color: white; padding: 8px 16px; border-radius: 20px; font-weight: bold;">{i}. {step_name}</div>'
        else:
            progress_html += f'<div style="background: #f0f0f0; color: #666; padding: 8px 16px; border-radius: 20px;">{i}. {step_name}</div>'
    progress_html += '</div>'
    st.markdown(progress_html, unsafe_allow_html=True)
    
    # Step 1: Category Selection
    if st.session_state.step == 1:
        show_category_selection()
    
    # Step 2: Domain Selection
    elif st.session_state.step == 2:
        show_domain_selection()
    
    # Step 3: Resume Upload and Analysis
    elif st.session_state.step == 3:
        show_resume_upload_and_analysis()

def show_category_selection():
    st.markdown('<div class="section-title">Select Your Professional Category</div>', unsafe_allow_html=True)
    
    categories = [
        "CA Fresher",
        "Experienced Professional (1–5 Yrs)",
        "Experienced Professional (>5 Yrs)",
        "Articleship",
        "Industrial Training",
        "Semi Qualified / CA Drop-out",
        "Graduate",
        "MBA / Post Graduate",
        "ACCA",
        "CS",
        "CMA",
        "Others"
    ]
    
    st.markdown("Please select the category that best describes your current professional status:")
    
    # Create radio buttons for category selection
    selected_category = st.radio(
        "Choose your category:",
        categories,
        index=None,
        key="category_radio"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Next: Select Domain", disabled=(selected_category is None), use_container_width=True):
            st.session_state.category = selected_category
            st.session_state.step = 2
            st.rerun()
    
    if selected_category is None:
        st.warning("Please select a category to proceed to domain selection.")

def show_domain_selection():
    st.markdown('<div class="section-title">Select Your Target Domain</div>', unsafe_allow_html=True)
    
    st.markdown(f"**Selected Category:** {st.session_state.category}")
    st.markdown("Now choose your target domain/specialization:")
    
    domains = [
        "General",
        "Accounting",
        "Statutory Audit",
        "Internal Audit",
        "Record to Report (R2R)",
        "Indirect Tax / GST",
        "Direct Tax / Corporate Tax / International Tax",
        "Transfer Pricing",
        "FP&A (Financial Planning & Analysis)",
        "Financial Reporting / IND AS Advisory / Financial Accounting & Advisory Service (FAAS)",
        "Management Consulting / Strategy Consulting",
        "Investment Banking",
        "Wealth Management",
        "Treasury / Equity Research",
        "Banking - Credit Manager / Debt Management / RM",
        "Commercial Finance / AP/AR Specialist",
        "Data Analytics",
        "ERP Consulting / SAP FICO",
        "ESG",
        "Finance Controller",
        "Financial Due Diligence",
        "M&A (Mergers & Acquisitions)",
        "M&A Tax",
        "Valuations",
        "Forensic Audit",
        "Management Trainee"
    ]
    
    selected_domain = st.selectbox(
        "Choose your target domain:",
        options=[None] + domains,
        format_func=lambda x: "-- Select a domain --" if x is None else x,
        key="domain_selectbox"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back to Category", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    
    with col3:
        if st.button("Next: Upload Resume", disabled=(selected_domain is None), use_container_width=True):
            st.session_state.domain = selected_domain
            st.session_state.step = 3
            st.rerun()
    
    if selected_domain is None:
        st.warning("Please select a domain to proceed to resume upload.")

def show_resume_upload_and_analysis():
    st.markdown('<div class="section-title">Upload Your Resume</div>', unsafe_allow_html=True)
    
    st.markdown(f"**Selected Category:** {st.session_state.category}")
    st.markdown(f"**Selected Domain:** {st.session_state.domain}")
    
    # Initialize components
    text_extractor = TextExtractor()
    resume_scorer = ResumeScorer()
    
    uploaded_file = st.file_uploader(
        "Choose your resume file (PDF or DOCX)",
        type=['pdf', 'docx'],
        help="Upload a PDF or Word document",
        key="resume_uploader"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back to Domain", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    
    if uploaded_file is not None:
        st.session_state.resume_uploaded = True
        
        try:
            # Extract text from uploaded file
            with st.spinner("Extracting text from your resume..."):
                file_details = text_extractor.get_file_info(uploaded_file)
                
                # Save uploaded file temporarily
                temp_file_path = f"temp_{uploaded_file.name}"
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Extract text
                resume_text = text_extractor.extract_text(temp_file_path, file_details['type'])
                
                if not resume_text.strip():
                    st.error("❌ Could not extract text from the file. Please ensure your resume contains readable text.")
                    return
            
            # Map domain to internal domain key
            domain_mapping = get_domain_mapping()
            internal_domain = domain_mapping.get(st.session_state.domain, "general")
            
            # Analyze resume
            with st.spinner("Analyzing your resume with AI..."):
                score_result = resume_scorer.score_resume(resume_text, internal_domain)
            
            # Create two-panel layout
            left_col, right_col = st.columns([3, 2])
            
            with left_col:
                display_analysis_panel(score_result, resume_text, internal_domain, st.session_state.category)
            
            with right_col:
                display_pdf_preview(uploaded_file, temp_file_path)
                
        except Exception as e:
            st.error(f"❌ Error processing resume: {str(e)}")
            st.info("Please try uploading a different file or contact support if the issue persists.")
    else:
        st.warning("Please upload your resume file to begin analysis.")

def get_domain_mapping():
    """Map user-friendly domain names to internal domain keys"""
    return {
        "General": "general",
        "Accounting": "accounting",
        "Statutory Audit": "statutory_audit",
        "Internal Audit": "internal_audit",
        "Record to Report (R2R)": "r2r",
        "Indirect Tax / GST": "gst",
        "Direct Tax / Corporate Tax / International Tax": "direct_tax",
        "Transfer Pricing": "direct_tax",
        "FP&A (Financial Planning & Analysis)": "fpa",
        "Financial Reporting / IND AS Advisory / Financial Accounting & Advisory Service (FAAS)": "accounting",
        "Management Consulting / Strategy Consulting": "general",
        "Investment Banking": "investment_banking",
        "Wealth Management": "wealth_management",
        "Treasury / Equity Research": "general",
        "Banking - Credit Manager / Debt Management / RM": "banking",
        "Commercial Finance / AP/AR Specialist": "general",
        "Data Analytics": "general",
        "ERP Consulting / SAP FICO": "general",
        "ESG": "general",
        "Finance Controller": "general",
        "Financial Due Diligence": "general",
        "M&A (Mergers & Acquisitions)": "general",
        "M&A Tax": "direct_tax",
        "Valuations": "general",
        "Forensic Audit": "statutory_audit",
        "Management Trainee": "general"
    }

def display_analysis_panel(score_result, resume_text, domain, category=None):
    """Display comprehensive analysis in the left panel"""
    
    # Total Score Card
    st.markdown(f"""
    <div class="score-card">
        <div class="score-number">{score_result['total_score']}</div>
        <div class="score-text">Total Score out of 100</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section-wise Scores
    st.markdown('<div class="section-title">Section-wise Scores (out of 10)</div>', unsafe_allow_html=True)
    
    sections = score_result['section_scores']
    for section_name, score in sections.items():
        section_display = section_name.replace('_', ' ').title()
        color = get_score_color(score)
        
        st.markdown(f"""
        <div class="heatmap-item">
            <span style="font-weight: 600;">{section_display}</span>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {score * 10}%; background-color: {color};"></div>
                </div>
                <span style="font-weight: 600; color: {color};">{score}/10</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Word Count Analysis
    word_count_data = score_result['word_count_analysis']
    st.markdown('<div class="section-title">Word Count Analysis</div>', unsafe_allow_html=True)
    
    with st.expander(f"Resume Length: {word_count_data['word_count']} words", expanded=True):
        status_class = "word-count-good" if word_count_data['is_optimal'] else "word-count-warning"
        
        st.markdown(f"""
        <div class="word-count-section">
            <div class="{status_class}">
                <strong>Current Length:</strong> {word_count_data['word_count']} words<br>
                <strong>Profile Type:</strong> {'Fresher' if word_count_data['is_fresher'] else 'Experienced Professional'}<br>
                <strong>Target Range:</strong> {word_count_data['target_range']}<br>
                <strong>Status:</strong> {'Optimal' if word_count_data['is_optimal'] else 'Needs Adjustment'}
            </div>
            <br>
            <strong>Recommendation:</strong><br>
            {word_count_data['recommendation']}
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Section Feedback
    st.markdown('<div class="section-title">Detailed Section-wise Feedback</div>', unsafe_allow_html=True)
    
    section_names = {
        'about_me': 'About Me / Summary',
        'education': 'Education & Certifications', 
        'experience': 'Work Experience',
        'skills': 'Skills Assessment'
    }
    
    for section_key, section_title in section_names.items():
        with st.expander(f"{section_title} (Score: {sections[section_key]}/10)", expanded=True):
            feedback = score_result['section_feedback'][section_key]
            
            if feedback['strengths']:
                st.markdown("**Strengths:**")
                for strength in feedback['strengths']:
                    st.markdown(f'<div class="feedback-item strength-item">{strength}</div>', unsafe_allow_html=True)
            
            if feedback['improvements']:
                st.markdown("**Areas for Improvement:**")
                for improvement in feedback['improvements']:
                    st.markdown(f'<div class="feedback-item improvement-item">{improvement}</div>', unsafe_allow_html=True)
            
            if feedback['errors']:
                st.markdown("**Issues Found:**")
                for error in feedback['errors']:
                    st.markdown(f'<div class="feedback-item error-item">{error}</div>', unsafe_allow_html=True)
    
    # Skills Analysis with Heatmap
    display_skills_analysis(score_result)
    
    # Grammar & Spelling Analysis
    st.markdown('<div class="section-title">Grammar & Spelling Corrections</div>', unsafe_allow_html=True)
    
    grammar_analysis = score_result['grammar_issues']
    with st.expander(f"Grammar & Spelling Analysis (Score: {grammar_analysis['overall_score']}/10)", expanded=True):
        
        # Show correct elements first
        if grammar_analysis['correct_elements']:
            st.markdown("**Correct Elements:**")
            for correct_item in grammar_analysis['correct_elements']:
                st.markdown(f'<div class="feedback-item strength-item">{correct_item}</div>', unsafe_allow_html=True)
        
        # Show issues if any
        if grammar_analysis['issues']:
            st.markdown("**Issues Found:**")
            for issue in grammar_analysis['issues']:
                issue_type = issue['type'].title()
                st.markdown(f"""
                <div class="grammar-correction">
                    <strong>{issue_type} Error:</strong> "{issue['issue']}"<br>
                    <strong>Correction:</strong> {issue['description']}<br>
                    <small><em>Context: {issue.get('context', 'N/A')}</em></small>
                </div>
                """, unsafe_allow_html=True)
            
            # Summary of issues
            st.markdown(f"""
            <div class="word-count-section">
                <strong>Summary:</strong> {grammar_analysis['total_issues']} total issues found 
                ({grammar_analysis['grammar_errors']} grammar, {grammar_analysis['formatting_issues']} formatting, 
                {grammar_analysis['spelling_issues']} spelling)
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="feedback-item strength-item">Excellent! No grammar or spelling issues detected.</div>', unsafe_allow_html=True)
        
        # Show sentence improvement suggestions
        if grammar_analysis.get('improvements'):
            st.markdown("**Sentence Improvement Suggestions:**")
            for improvement in grammar_analysis['improvements']:
                st.markdown(f"""
                <div class="improvement-suggestion">
                    <strong>Original:</strong> "{improvement['issue'][:100]}..."<br>
                    <strong>Improved:</strong> {improvement['suggestion']}<br>
                    <strong>Example:</strong> <em>{improvement['example']}</em>
                </div>
                """, unsafe_allow_html=True)
        elif not grammar_analysis['issues']:
            st.markdown('<div class="feedback-item strength-item">Sentences are well-structured and impactful!</div>', unsafe_allow_html=True)
    
    # Overall Heatmap
    display_overall_heatmap(score_result['heatmap_data'])
    
    # Keyword Suggestions Section
    st.markdown('<div class="section-title">Keyword Suggestions to Improve Your Score</div>', unsafe_allow_html=True)
    
    with st.expander("Top 10 Missing Keywords", expanded=True):
        hard_skills = score_result['hard_skills_analysis']
        soft_skills = score_result['soft_skills_analysis']
        
        st.markdown("**Top 10 Missing Domain Keywords:**")
        missing_domain = hard_skills['missing_skills'][:10]
        if missing_domain:
            keyword_tags = ""
            for keyword in missing_domain:
                keyword_tags += f'<span class="keyword-tag">{keyword}</span>'
            st.markdown(f'<div style="margin: 1rem 0;">{keyword_tags}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="feedback-item strength-item">All domain keywords present!</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**🔧 Top 10 Hard Skills to Add:**")
            suggested_hard_skills = [
                'Excel Advanced', 'Financial Modeling', 'SQL', 'Python', 'Data Analysis',
                'Tableau', 'Power BI', 'SAP', 'QuickBooks', 'Bloomberg Terminal'
            ]
            for i, skill in enumerate(suggested_hard_skills, 1):
                st.markdown(f"{i}. {skill}")
        
        with col3:
            st.markdown("**🤝 Top 10 Soft Skills to Add:**")
            missing_soft = soft_skills['missing_skills'][:10]
            if len(missing_soft) < 10:
                additional_soft_skills = [
                    'Leadership', 'Communication', 'Problem Solving', 'Analytical Thinking',
                    'Time Management', 'Adaptability', 'Project Management', 'Teamwork',
                    'Critical Thinking', 'Decision Making'
                ]
                missing_soft.extend(additional_soft_skills[:10 - len(missing_soft)])
            
            for i, skill in enumerate(missing_soft[:10], 1):
                st.markdown(f"{i}. {skill}")

    # Recommendations
    st.markdown('<div class="section-title">🚀 Priority Recommendations</div>', unsafe_allow_html=True)
    for i, recommendation in enumerate(score_result['recommendations'], 1):
        st.markdown(f"""
        <div class="recommendation-item">
            <strong>{i}.</strong> {recommendation}
        </div>
        """, unsafe_allow_html=True)

def display_skills_analysis(score_result):
    """Display comprehensive skills analysis"""
    
    st.markdown('<div class="section-title">🎯 Skills Analysis & Heatmap</div>', unsafe_allow_html=True)
    
    # Hard Skills Analysis
    hard_skills = score_result['hard_skills_analysis']
    with st.expander(f"💼 Industry Keywords Analysis - {hard_skills['density']} Density ({hard_skills['relevance_score']:.1f}%)", expanded=True):
        
        st.markdown(f"**Found {hard_skills['total_found']} out of {hard_skills['total_available']} domain-specific keywords**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ Present Keywords (in order):**")
            if hard_skills['found_skills']:
                skills_html = ""
                for i, skill in enumerate(hard_skills['found_skills'], 1):
                    skills_html += f'<span class="skill-tag">{i}. {skill}</span> '
                st.markdown(f'<div class="skills-grid">{skills_html}</div>', unsafe_allow_html=True)
                st.markdown(f"*{len(hard_skills['found_skills'])} keywords found*")
            else:
                st.markdown("No domain-specific keywords detected")
        
        with col2:
            st.markdown("**❌ Missing Keywords (in order):**")
            if hard_skills['missing_skills']:
                missing_html = ""
                for i, skill in enumerate(hard_skills['missing_skills'], 1):
                    missing_html += f'<span class="missing-skill-tag">{i}. {skill}</span> '
                st.markdown(f'<div class="skills-grid">{missing_html}</div>', unsafe_allow_html=True)
                st.markdown(f"*{len(hard_skills['missing_skills'])} keywords missing*")
            else:
                st.markdown("Excellent! All domain keywords are present!")
    
    # Soft Skills Analysis
    soft_skills = score_result['soft_skills_analysis']
    with st.expander(f"🤝 Soft Skills Analysis - {soft_skills['assessment']} ({soft_skills['coverage_score']:.1f}%)", expanded=True):
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ Found Soft Skills:**")
            if soft_skills['found_skills']:
                soft_html = ""
                for skill in soft_skills['found_skills'][:12]:
                    soft_html += f'<span class="skill-tag">{skill}</span> '
                st.markdown(f'<div class="skills-grid">{soft_html}</div>', unsafe_allow_html=True)
            else:
                st.markdown("No soft skills detected")
        
        with col2:
            st.markdown("**📝 Recommended Additions:**")
            if soft_skills['missing_skills']:
                missing_soft_html = ""
                for skill in soft_skills['missing_skills'][:8]:
                    missing_soft_html += f'<span class="missing-skill-tag">{skill}</span> '
                st.markdown(f'<div class="skills-grid">{missing_soft_html}</div>', unsafe_allow_html=True)
    
    # Certification Analysis
    cert_analysis = score_result['certification_analysis']
    with st.expander(f"🏆 Certification Analysis - {cert_analysis['value_assessment']}", expanded=False):
        if cert_analysis['found_certifications']:
            st.markdown("**✅ Found Certifications:**")
            for cert in cert_analysis['found_certifications']:
                st.markdown(f"• {cert}")
        
        if cert_analysis['missing_key_certs']:
            st.markdown("**📝 Recommended Certifications:**")
            for cert in cert_analysis['missing_key_certs']:
                st.markdown(f"• {cert}")

def display_overall_heatmap(heatmap_data):
    """Display overall performance heatmap"""
    
    st.markdown('<div class="section-title">🌡️ Performance Heatmap</div>', unsafe_allow_html=True)
    
    categories = [
        ("Content Quality", heatmap_data['overall_health']['Content Quality']),
        ("Qualifications", heatmap_data['overall_health']['Qualifications']),
        ("Professional Impact", heatmap_data['overall_health']['Professional Impact']),
        ("Hard Skills Density", heatmap_data['skills_density']['Hard Skills']),
        ("Soft Skills Coverage", heatmap_data['skills_density']['Soft Skills'])
    ]
    
    for category, score in categories:
        color = get_score_color(score / 10)
        st.markdown(f"""
        <div class="heatmap-item">
            <span style="font-weight: 600;">{category}</span>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {score}%; background-color: {color};"></div>
                </div>
                <span style="font-weight: 600; color: {color};">{score:.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

import streamlit.components.v1 as components

def display_pdf_preview(uploaded_file, temp_file_path):
    """Display PDF preview in the right panel"""
    st.markdown("### 📄 Resume Preview", unsafe_allow_html=True)

    try:
        st.write(f"File type detected: {uploaded_file.type}")
        st.write(f"File name: {uploaded_file.name}")

        if uploaded_file.name.lower().endswith(".pdf"):
            with open(temp_file_path, "rb") as f:
                pdf_data = f.read()

            if not pdf_data:
                st.error("❌ PDF file is empty or could not be read.")
                return

            base64_pdf = base64.b64encode(pdf_data).decode("utf-8")
            pdf_display = f"""
                data:application/pdf;base64,{base64_pdf}</iframe>
            """
            components.html(pdf_display, height=620)
        else:
            st.markdown(f"""
                #### 📄 {uploaded_file.name}
                DOCX files cannot be previewed directly.
                File size: {uploaded_file.size / 1024:.1f} KB  
                ✅ Text extracted successfully
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error displaying resume preview: {str(e)}")



def get_score_color(score):
    """Get color based on score (0-10 scale)"""
    if score >= 8:
        return "#28a745"  # Green
    elif score >= 6:
        return "#ffc107"  # Yellow
    elif score >= 4:
        return "#fd7e14"  # Orange
    else:
        return "#dc3545"  # Red

if __name__ == "__main__":
    main()
