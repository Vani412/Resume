import re
from typing import Dict, List, Tuple
from domain_keywords import DomainKeywords

class ResumeScorer:
    """
    Advanced resume scoring engine that provides comprehensive analysis with section-wise breakdown
    """
    
    def __init__(self):
        self.domain_keywords = DomainKeywords()
        
        # Comprehensive soft skills database (30+ skills)
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving', 'analytical thinking',
            'attention to detail', 'time management', 'adaptability', 'creativity', 'critical thinking',
            'collaboration', 'project management', 'presentation skills', 'negotiation', 'mentoring',
            'strategic thinking', 'decision making', 'conflict resolution', 'emotional intelligence',
            'interpersonal skills', 'multitasking', 'organization', 'planning', 'innovation',
            'customer service', 'flexibility', 'reliability', 'initiative', 'patience',
            'stress management', 'delegation', 'coaching', 'public speaking', 'networking',
            'cultural awareness', 'empathy', 'persuasion', 'active listening', 'work ethic'
        ]
        
        # Hard skills database (technical skills)
        self.hard_skills = [
            'excel advanced', 'financial modeling', 'sql', 'python', 'r programming',
            'tableau', 'power bi', 'quickbooks', 'sap', 'oracle', 'bloomberg terminal',
            'financial analysis', 'data analysis', 'statistical analysis', 'regression analysis',
            'variance analysis', 'budgeting', 'forecasting', 'valuation', 'risk management',
            'audit procedures', 'compliance monitoring', 'internal controls', 'process improvement',
            'dashboard creation', 'pivot tables', 'vlookup', 'macros', 'vba programming',
            'financial reporting', 'gaap knowledge', 'ifrs knowledge', 'tax preparation'
        ]
        
        # Action words for impact assessment
        self.action_words = [
            'achieved', 'accomplished', 'implemented', 'developed', 'managed', 'led', 'created',
            'improved', 'increased', 'reduced', 'optimized', 'streamlined', 'enhanced', 'delivered',
            'coordinated', 'supervised', 'executed', 'initiated', 'designed', 'established',
            'generated', 'facilitated', 'analyzed', 'resolved', 'collaborated', 'mentored'
        ]
        
        # Education keywords
        self.education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'degree', 'university', 'college',
            'certification', 'certified', 'license', 'accredited', 'diploma', 'course',
            'training', 'workshop', 'seminar', 'continuing education', 'professional development'
        ]
        
        # Common spelling and grammar issues
        self.grammar_issues = {
            r'\bthere\s+are\s+\w+\s+that\s+is\b': 'Subject-verb disagreement',
            r'\bshould\s+of\b': 'Should use "should have"',
            r'\bcould\s+of\b': 'Should use "could have"',
            r'\bwould\s+of\b': 'Should use "would have"',
            r'\bit\'s\s+own\b': 'Should use "its own"',
            r'\byour\s+welcome\b': 'Should use "you\'re welcome"',
            r'\beffect\s+(on|upon)\b': 'Consider using "affect" instead',
            r'\bthen\s+I\s+will\b': 'Consider using "than" for comparisons'
        }

    def score_resume(self, resume_text: str, domain: str) -> Dict:
        """
        Comprehensive resume scoring with detailed section-wise analysis
        """
        cleaned_text = self._clean_text(resume_text)
        domain_data = self.domain_keywords.get_domain_keywords(domain)
        
        # Extract sections
        sections = self._extract_sections(cleaned_text)
        
        # Score each section out of 10
        about_score, about_feedback = self._score_about_section(sections.get('about', ''), cleaned_text)
        education_score, education_feedback = self._score_education_section(sections.get('education', ''), cleaned_text)
        experience_score, experience_feedback = self._score_experience_section(sections.get('experience', ''), cleaned_text)
        skills_score, skills_feedback = self._score_skills_section(sections.get('skills', ''), cleaned_text, domain_data)
        
        # Calculate total score out of 100 (weighted)
        total_score = (about_score * 2.5) + (education_score * 2.5) + (experience_score * 2.5) + (skills_score * 2.5)
        
        # Grammar and spelling analysis
        grammar_issues = self._check_grammar_spelling(cleaned_text)
        
        # Word count analysis
        word_count_analysis = self._analyze_word_count(cleaned_text)
        
        # Skills analysis with heatmap data
        hard_skills_analysis = self._analyze_hard_skills(cleaned_text, domain_data)
        soft_skills_analysis = self._analyze_soft_skills(cleaned_text)
        
        # Certification analysis
        cert_analysis = self._analyze_certifications(cleaned_text, domain)
        
        # Overall personalized recommendations
        recommendations = self._generate_personalized_recommendations(
            about_score, education_score, experience_score, skills_score,
            hard_skills_analysis, soft_skills_analysis, grammar_issues['issues'],
            cleaned_text, domain
        )
        
        return {
            'total_score': round(total_score, 1),
            'section_scores': {
                'about_me': about_score,
                'education': education_score,
                'experience': experience_score,
                'skills': skills_score
            },
            'section_feedback': {
                'about_me': about_feedback,
                'education': education_feedback,
                'experience': experience_feedback,
                'skills': skills_feedback
            },
            'grammar_issues': grammar_issues,
            'word_count_analysis': word_count_analysis,
            'hard_skills_analysis': hard_skills_analysis,
            'soft_skills_analysis': soft_skills_analysis,
            'certification_analysis': cert_analysis,
            'recommendations': recommendations,
            'heatmap_data': self._generate_heatmap_data(
                about_score, education_score, experience_score, skills_score,
                hard_skills_analysis, soft_skills_analysis
            )
        }

    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from resume text"""
        sections = {}
        
        # About/Summary section patterns - more precise extraction
        about_patterns = [
            r'(?:summary|about|profile|objective|professional summary|career objective|personal statement)[\s\n]*[:]*\s*(.*?)(?=\n\s*(?:education|experience|skills|work|employment|contact|phone|email)|$)',
            r'(?:^|\n)\s*([^.\n]*(?:years?\s+(?:of\s+)?experience|professional|specialist|expert|certified|skilled)[^.\n]*(?:\.[^.\n]*){0,2})(?=\n|\s*$)',
        ]
        
        # Education section
        education_pattern = r'(?:education|academic|qualification)[\s\n]*[:]*\s*(.*?)(?=\n\s*[A-Z][^a-z]*:|$)'
        
        # Experience section
        experience_pattern = r'(?:experience|employment|work|career|professional)[\s\n]*[:]*\s*(.*?)(?=\n\s*[A-Z][^a-z]*:|$)'
        
        # Skills section
        skills_pattern = r'(?:skills|competencies|expertise|technical)[\s\n]*[:]*\s*(.*?)(?=\n\s*[A-Z][^a-z]*:|$)'
        
        text_lower = text.lower()
        
        for pattern in about_patterns:
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            if match and len(match.group(1).strip()) > 20:
                sections['about'] = match.group(1).strip()
                break
        
        for section_name, pattern in [
            ('education', education_pattern),
            ('experience', experience_pattern), 
            ('skills', skills_pattern)
        ]:
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            if match:
                sections[section_name] = match.group(1).strip()
        
        return sections

    def _score_about_section(self, about_text: str, full_text: str) -> Tuple[float, Dict]:
        """Score About Me/Summary section out of 10 with detailed feedback"""
        score = 0.0
        feedback = {
            'strengths': [],
            'improvements': [],
            'errors': [],
            'detailed_analysis': {}
        }
        
        # Detailed length analysis with better text cleaning
        if about_text:
            # Clean the about text by removing extra whitespace and non-essential content
            cleaned_about = re.sub(r'\s+', ' ', about_text.strip())
            # Remove contact info patterns that might have been captured
            cleaned_about = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '', cleaned_about)  # emails
            cleaned_about = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', cleaned_about)  # phones
            cleaned_about = re.sub(r'\blinkedin\b|\bgithub\b|\btwitter\b', '', cleaned_about, re.IGNORECASE)  # social
            cleaned_about = cleaned_about.strip()
            
            char_count = len(cleaned_about)
            # More accurate word count - split by whitespace and filter empty strings
            words = [word for word in cleaned_about.split() if word.strip()]
            word_count = len(words)
        else:
            char_count = 0
            word_count = 0
            cleaned_about = ""
        
        # Check if section exists (2 points)
        if about_text and char_count > 10:
            score += 2
            feedback['strengths'].append("✅ About section is present")
            feedback['detailed_analysis']['section_exists'] = True
        else:
            feedback['errors'].append("❌ Missing or too short About/Summary section - this is critical for first impressions")
            feedback['improvements'].append("💡 Add a compelling 2-3 sentence summary highlighting your experience, skills, and career objectives")
            feedback['detailed_analysis']['section_exists'] = False
        
        # Comprehensive length analysis (2 points)
        if about_text and 50 <= char_count <= 300:
            score += 2
            feedback['strengths'].append("✅ Optimal length - concise yet informative")
        elif about_text and char_count < 50:
            feedback['improvements'].append("📝 Summary too brief. Expand to include: years of experience, key specialization, notable achievement")
            feedback['improvements'].append("💡 Example: 'Experienced CPA with 8+ years in financial auditing, specializing in SOX compliance and risk assessment. Led audit teams for Fortune 500 companies, reducing compliance issues by 40%.'")
        elif about_text and char_count > 300:
            feedback['improvements'].append("📝 Summary too lengthy. Condense to focus on most impactful achievements")
            feedback['improvements'].append("💡 Remove less relevant details and focus on quantifiable achievements and core competencies")
        
        # Detailed key elements analysis (3 points) - using cleaned text
        key_elements = 0
        experience_match = re.search(r'\b(\d+)\s*\+?\s*(?:years?|yrs?)\b', cleaned_about, re.IGNORECASE) if cleaned_about else None
        if experience_match:
            key_elements += 1
            years = experience_match.group(1)
            feedback['strengths'].append(f"✅ Quantifies experience ({years} years) - shows career progression")
        else:
            feedback['improvements'].append("📝 Add specific years of experience (e.g., '5+ years in auditing')")
            feedback['improvements'].append("💡 Quantifying experience immediately establishes credibility and seniority level")
        
        expertise_words = ['expert', 'experienced', 'skilled', 'proficient', 'specialist', 'certified']
        found_expertise = [word for word in expertise_words if word in cleaned_about.lower()] if cleaned_about else []
        if found_expertise:
            key_elements += 1
            feedback['strengths'].append(f"✅ Establishes expertise level ('{', '.join(found_expertise)}')")
        else:
            feedback['improvements'].append("📝 Include expertise indicators: 'experienced', 'certified', 'specialist', 'expert'")
            feedback['improvements'].append("💡 Example: 'Certified Public Accountant' or 'Experienced financial analyst'")
        
        action_words = ['achieve', 'deliver', 'improve', 'lead', 'manage', 'develop', 'implement', 'optimize']
        found_actions = [word for word in action_words if word in cleaned_about.lower()] if cleaned_about else []
        if found_actions:
            key_elements += 1
            feedback['strengths'].append(f"✅ Uses impactful action words ('{', '.join(found_actions)}')")
        else:
            feedback['improvements'].append("📝 Include strong action verbs: achieved, led, developed, implemented, optimized")
            feedback['improvements'].append("💡 Replace weak phrases like 'responsible for' with 'managed', 'led', 'achieved'")
        
        score += key_elements
        
        # Enhanced professional tone analysis (2 points) - using cleaned text
        first_person_matches = re.findall(r'\b(i am|i have|i do|my|me)\b', cleaned_about.lower()) if cleaned_about else []
        if first_person_matches:
            feedback['improvements'].append(f"📝 Uses first-person perspective ({len(first_person_matches)} instances: {', '.join(set(first_person_matches))})")
            feedback['improvements'].append("💡 Convert to third-person for professional tone: 'I am experienced' → 'Experienced professional'")
            feedback['improvements'].append("💡 Example transformation: 'I have 5 years experience' → 'Professional with 5 years experience'")
        elif cleaned_about:
            score += 1
            feedback['strengths'].append("✅ Maintains professional third-person tone throughout")
        
        # Detailed career focus analysis (1 point)
        domain_terms = {
            'audit': ['audit', 'auditing', 'auditor', 'sox', 'compliance', 'internal controls'],
            'tax': ['tax', 'taxation', 'tax planning', 'tax compliance', 'ctp'],
            'finance': ['finance', 'financial', 'cfa', 'investment', 'portfolio'],
            'accounting': ['accounting', 'accountant', 'cpa', 'gaap', 'financial reporting']
        }
        
        found_domains = []
        for domain, terms in domain_terms.items():
            if any(term in cleaned_about.lower() for term in terms) if cleaned_about else False:
                found_domains.append(domain)
        
        if found_domains:
            score += 1
            feedback['strengths'].append(f"✅ Clear specialization in {', '.join(found_domains)}")
        else:
            feedback['improvements'].append("📝 Specify your professional specialization (auditing, taxation, finance, accounting)")
            feedback['improvements'].append("💡 Example additions: 'specializing in internal audit', 'focused on tax compliance', 'expertise in financial analysis'")
        
        # Additional detailed analysis for About section
        if cleaned_about:
            # Check for quantifiable achievements
            numbers = re.findall(r'\d+[%$]?', cleaned_about)
            if numbers:
                feedback['strengths'].append(f"✅ Includes quantifiable metrics ({', '.join(numbers)})")
            else:
                feedback['improvements'].append("💡 Consider adding quantifiable achievements: '25% cost reduction', '$2M budget managed', '50+ audits completed'")
        
        # Analyze contact information presence in full text (not just about section)
        contact_analysis = self._analyze_contact_information(full_text)
        
        # Contact information feedback
        if contact_analysis['has_name']:
            feedback['strengths'].append("✅ Professional name clearly displayed")
        else:
            feedback['improvements'].append("📝 Ensure your full name is prominently displayed at the top")
            
        if contact_analysis['has_email']:
            feedback['strengths'].append("✅ Email address provided for contact")
        else:
            feedback['improvements'].append("📝 Include a professional email address")
            
        if contact_analysis['has_phone']:
            feedback['strengths'].append("✅ Phone number available for contact")
        else:
            feedback['improvements'].append("📝 Add your phone number for easy contact")
            
        if contact_analysis['has_linkedin']:
            feedback['strengths'].append("✅ LinkedIn profile linked for professional networking")
        else:
            feedback['improvements'].append("💡 Consider adding your LinkedIn profile URL to enhance professional presence")
        
        feedback['detailed_analysis'] = {
            'word_count': word_count,
            'char_count': char_count,
            'key_elements_found': key_elements,
            'first_person_usage': len(first_person_matches) if about_text else 0,
            'domain_focus': found_domains,
            'action_words_used': found_actions,
            'expertise_indicators': found_expertise
        }
        
        return min(score, 10), feedback

    def _score_education_section(self, education_text: str, full_text: str) -> Tuple[float, Dict]:
        """Score Education & Certifications section out of 10 with comprehensive analysis"""
        score = 0.0
        feedback = {
            'strengths': [],
            'improvements': [],
            'errors': [],
            'detailed_analysis': {}
        }
        
        # Detailed section analysis
        char_count = len(education_text.strip()) if education_text else 0
        entries = [line.strip() for line in education_text.split('\n') if line.strip()] if education_text else []
        
        # Check if education section exists (2 points)
        if education_text and char_count > 10:
            score += 2
            feedback['strengths'].append(f"✅ Education section present with {len(entries)} entries ({char_count} characters)")
        else:
            feedback['errors'].append("❌ Missing or incomplete education section - employers expect detailed educational background")
            feedback['improvements'].append("💡 Include: Degree, Institution, Graduation Year, Major/Field")
            feedback['improvements'].append("💡 Format: 'Bachelor of Science in Accounting, State University, 2020'")
        
        # Enhanced degree analysis (3 points)
        degree_patterns = {
            'Bachelor': r'\b(?:bachelor|b\.?[as]\.?|undergraduate|bsc|bba|ba|bs)\b',
            'Master': r'\b(?:master|m\.?[as]\.?|mba|graduate|msc|ma|ms)\b',
            'Doctorate': r'\b(?:phd|doctorate|doctoral|ph\.?d\.?|dba)\b',
            'Professional': r'\b(?:cpa|ca|acca|cma|jd|md|pharmd)\b',
            'Associate': r'\b(?:associate|a\.?[as]\.?|diploma)\b'
        }
        
        found_degrees = []
        for degree_type, pattern in degree_patterns.items():
            if re.search(pattern, education_text, re.IGNORECASE) if education_text else False:
                found_degrees.append(degree_type)
        
        if found_degrees:
            score += 3
            feedback['strengths'].append(f"✅ {len(found_degrees)} degree type(s): {', '.join(found_degrees)}")
            if len(found_degrees) > 1:
                feedback['strengths'].append("✅ Multiple degrees demonstrate commitment to education")
        else:
            feedback['improvements'].append("📝 Specify exact degree type: Bachelor's/Master's/MBA/PhD")
            feedback['improvements'].append("💡 Examples: 'Bachelor of Science in Accounting' or 'Master of Business Administration'")
        
        # Institution analysis (2 points)
        institution_indicators = ['university', 'college', 'institute', 'school', 'academy']
        institution_found = any(indicator in education_text.lower() for indicator in institution_indicators) if education_text else False
        
        if institution_found:
            score += 2
            # Check for specific institution names
            if re.search(r'\b[A-Z][a-z]+\s+(University|College|Institute)\b', education_text) if education_text else False:
                feedback['strengths'].append("✅ Specific educational institution names provided")
            else:
                feedback['strengths'].append("✅ Educational institution type mentioned")
                feedback['improvements'].append("💡 Include specific institution names for better credibility")
        else:
            feedback['improvements'].append("📝 Include specific educational institution names")
            feedback['improvements'].append("💡 Examples: 'Harvard University', 'State University', 'Community College'")
        
        # Graduation year analysis (1 point)
        year_matches = re.findall(r'\b(19|20)(\d{2})\b', education_text) if education_text else []
        if year_matches:
            score += 1
            years = [f"{y[0]}{y[1]}" for y in year_matches]
            feedback['strengths'].append(f"✅ Graduation year(s) specified: {', '.join(years)}")
            
            # Check for recent graduation
            recent_years = [y for y in years if int(y) >= 2020]
            if recent_years:
                feedback['strengths'].append(f"✅ Recent education ({', '.join(recent_years)}) shows current knowledge")
        else:
            feedback['improvements'].append("📝 Add graduation year or expected completion date")
            feedback['improvements'].append("💡 Include format: 'May 2020' or 'Expected Dec 2025'")
        
        # Enhanced certification analysis (2 points)
        cert_categories = {
            'Accounting': ['cpa', 'ca', 'acca', 'cma'],
            'Audit': ['cia', 'cisa', 'crma'],
            'Finance': ['cfa', 'frm', 'cfp'],
            'Tax': ['ea', 'ctp', 'cmt'],
            'General': ['certified', 'licensed']
        }
        
        found_certs = {}
        for category, certs in cert_categories.items():
            category_certs = [cert for cert in certs if cert in education_text.lower()] if education_text else []
            if category_certs:
                found_certs[category] = category_certs
        
        if found_certs:
            score += 2
            cert_summary = []
            for category, certs in found_certs.items():
                cert_summary.append(f"{category}: {', '.join(certs).upper()}")
            feedback['strengths'].append(f"✅ Professional certifications: {'; '.join(cert_summary)}")
        else:
            feedback['improvements'].append("📝 Add relevant professional certifications (CPA, CMA, CIA, CFA)")
            feedback['improvements'].append("💡 Include status: 'CPA Licensed' or 'CPA Candidate - Exam in Progress'")
        
        # Additional detailed enhancements
        if education_text:
            # Check for field of study
            study_fields = ['accounting', 'finance', 'business', 'economics', 'audit', 'taxation']
            found_fields = [field for field in study_fields if field in education_text.lower()]
            if found_fields:
                feedback['strengths'].append(f"✅ Relevant field of study: {', '.join(found_fields)}")
            else:
                feedback['improvements'].append("💡 Specify field of study: 'Major in Accounting' or 'Concentration in Finance'")
            
            # Check for GPA mention
            if re.search(r'\b(?:gpa|grade)\s*:?\s*(\d+\.?\d*)', education_text, re.IGNORECASE):
                gpa_match = re.search(r'\b(?:gpa|grade)\s*:?\s*(\d+\.?\d*)', education_text, re.IGNORECASE)
                gpa_val = float(gpa_match.group(1))
                if gpa_val >= 3.5:
                    feedback['strengths'].append(f"✅ Excellent academic performance (GPA: {gpa_val})")
            else:
                feedback['improvements'].append("💡 Include GPA if 3.5+ to showcase academic excellence")
            
            # Check for honors
            honors_keywords = ['magna cum laude', 'summa cum laude', 'cum laude', 'honors', 'dean\'s list']
            found_honors = [honor for honor in honors_keywords if honor in education_text.lower()]
            if found_honors:
                feedback['strengths'].append(f"✅ Academic honors: {', '.join(found_honors)}")
        
        feedback['detailed_analysis'] = {
            'degrees_found': found_degrees,
            'certification_categories': list(found_certs.keys()),
            'graduation_years': [f"{y[0]}{y[1]}" for y in year_matches] if year_matches else [],
            'entry_count': len(entries),
            'section_length': char_count,
            'institution_mentioned': institution_found
        }
        
        return min(score, 10), feedback

    def _score_experience_section(self, experience_text: str, full_text: str) -> Tuple[float, Dict]:
        """Score Work Experience section out of 10"""
        score = 0.0
        feedback = {
            'strengths': [],
            'improvements': [],
            'errors': []
        }
        
        # Check if experience section exists (2 points)
        if experience_text and len(experience_text.strip()) > 20:
            score += 2
            feedback['strengths'].append("✅ Work experience section is present")
        else:
            feedback['errors'].append("❌ Missing or incomplete work experience section")
        
        # Check for company names and job titles (2 points)
        if re.search(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*(?:inc|corp|llc|ltd|company|group|firm)\b', experience_text, re.IGNORECASE):
            score += 1
            feedback['strengths'].append("✅ Company names mentioned")
        
        if re.search(r'\b(?:manager|senior|analyst|associate|director|specialist|lead|coordinator)\b', experience_text, re.IGNORECASE):
            score += 1
            feedback['strengths'].append("✅ Job titles clearly stated")
        
        # Check for dates/duration (1 point)
        if re.search(r'\b(?:19|20)\d{2}\b.*?(?:19|20)\d{2}\b', experience_text) or re.search(r'\b\d+\s*(?:years?|months?)\b', experience_text):
            score += 1
            feedback['strengths'].append("✅ Employment dates/duration provided")
        else:
            feedback['improvements'].append("📝 Add employment dates and duration")
        
        # Check for action words and achievements (3 points)
        action_count = sum(1 for action in self.action_words if action in experience_text.lower())
        if action_count >= 5:
            score += 2
            feedback['strengths'].append("✅ Strong use of action words")
        elif action_count >= 3:
            score += 1
            feedback['strengths'].append("✅ Good use of action words")
        else:
            feedback['improvements'].append("📝 Add more strong action words (achieved, managed, led, etc.)")
        
        # Check for quantifiable results (2 points)
        numbers_pattern = r'\b\d+(?:\.\d+)?%?(?:\s*(?:million|thousand|k|m))?\b'
        if re.search(numbers_pattern, experience_text):
            score += 2
            feedback['strengths'].append("✅ Quantifiable achievements mentioned")
        else:
            feedback['improvements'].append("📝 Add specific numbers and metrics to show impact")
        
        return min(score, 10), feedback

    def _score_skills_section(self, skills_text: str, full_text: str, domain_data: Dict) -> Tuple[float, Dict]:
        """Score Skills section out of 10"""
        score = 0.0
        feedback = {
            'strengths': [],
            'improvements': [],
            'errors': []
        }
        
        # Check if skills section exists (2 points)
        if skills_text and len(skills_text.strip()) > 10:
            score += 2
            feedback['strengths'].append("✅ Skills section is present")
        else:
            feedback['errors'].append("❌ Missing or incomplete skills section")
        
        # Check for domain-specific technical skills (4 points)
        domain_keywords = domain_data.get('keywords', [])
        found_domain_skills = [skill for skill in domain_keywords if skill.lower() in full_text.lower()]
        
        if len(found_domain_skills) >= 10:
            score += 4
            feedback['strengths'].append(f"✅ Excellent domain expertise: {len(found_domain_skills)} relevant skills")
        elif len(found_domain_skills) >= 5:
            score += 3
            feedback['strengths'].append(f"✅ Good domain knowledge: {len(found_domain_skills)} relevant skills")
        elif len(found_domain_skills) >= 3:
            score += 2
            feedback['improvements'].append(f"📝 Add more domain-specific skills (found {len(found_domain_skills)})")
        else:
            feedback['improvements'].append("📝 Add more industry-specific technical skills")
        
        # Check for soft skills (2 points)
        found_soft_skills = [skill for skill in self.soft_skills if skill.lower() in full_text.lower()]
        if len(found_soft_skills) >= 5:
            score += 2
            feedback['strengths'].append(f"✅ Good soft skills coverage: {len(found_soft_skills)} skills")
        elif len(found_soft_skills) >= 3:
            score += 1
            feedback['improvements'].append("📝 Add a few more soft skills")
        else:
            feedback['improvements'].append("📝 Add relevant soft skills (leadership, communication, etc.)")
        
        # Check for technology/software skills (2 points)
        tech_keywords = ['excel', 'sap', 'quickbooks', 'sql', 'python', 'tableau', 'power bi', 'sage', 'peachtree']
        found_tech = [tech for tech in tech_keywords if tech.lower() in full_text.lower()]
        
        if found_tech:
            score += 2
            feedback['strengths'].append(f"✅ Technology skills mentioned: {', '.join(found_tech)}")
        else:
            feedback['improvements'].append("📝 Add relevant software/technology skills")
        
        return min(score, 10), feedback

    def _check_grammar_spelling(self, text: str) -> Dict:
        """Comprehensive grammar and spelling check with sentence improvement suggestions"""
        issues = []
        correct_elements = []
        improvements = []
        
        # Check common grammar patterns
        grammar_errors_found = 0
        for pattern, description in self.grammar_issues.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                issues.append({
                    'type': 'grammar',
                    'issue': match.group(),
                    'description': description,
                    'position': match.start(),
                    'context': text[max(0, match.start()-20):match.end()+20]
                })
                grammar_errors_found += 1
        
        # Check for basic formatting issues
        formatting_issues = 0
        if re.search(r'\s{3,}', text):
            issues.append({
                'type': 'formatting',
                'issue': 'Multiple spaces',
                'description': 'Remove extra spaces between words',
                'position': 0,
                'context': 'Multiple   spaces   found'
            })
            formatting_issues += 1
        
        if re.search(r'[a-z]\.[A-Z]', text):
            issues.append({
                'type': 'formatting',
                'issue': 'Missing space after period',
                'description': 'Add space after periods',
                'position': 0,
                'context': 'word.Next word'
            })
            formatting_issues += 1
        
        # Check for common spelling patterns
        spelling_issues = 0
        common_mistakes = {
            r'\brecieve\b': 'receive',
            r'\baccommodate\b': 'accommodate', 
            r'\boccurence\b': 'occurrence',
            r'\bseperate\b': 'separate',
            r'\bdefinately\b': 'definitely',
            r'\benvironment\b': 'environment',
            r'\bmaintenance\b': 'maintenance'
        }
        
        for mistake_pattern, correction in common_mistakes.items():
            match = re.search(mistake_pattern, text, re.IGNORECASE)
            if match:
                issues.append({
                    'type': 'spelling',
                    'issue': match.group(),
                    'description': f'Correct spelling: {correction}',
                    'position': match.start(),
                    'context': f'Change to: {correction}'
                })
                spelling_issues += 1
        
        # Check for positive elements
        if not grammar_errors_found:
            correct_elements.append("✅ No common grammar errors detected")
        
        if not formatting_issues:
            correct_elements.append("✅ Good formatting and spacing")
            
        if not spelling_issues:
            correct_elements.append("✅ No obvious spelling mistakes found")
        
        # Sentence improvement suggestions
        sentences = re.split(r'[.!?]+', text)
        for i, sentence in enumerate(sentences[:10]):  # Check first 10 sentences
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
                
            # Check for weak verbs that could be improved
            if re.search(r'\b(was|were|is|are)\s+responsible\s+for\b', sentence, re.IGNORECASE):
                improvements.append({
                    'type': 'sentence_improvement',
                    'issue': sentence,
                    'suggestion': 'Replace "was responsible for" with strong action verbs like "managed", "led", "developed"',
                    'example': 'Instead of "Was responsible for audits" → "Conducted comprehensive audits"'
                })
            
            # Check for vague statements
            if re.search(r'\b(many|various|several|some)\b', sentence, re.IGNORECASE) and not re.search(r'\d+', sentence):
                improvements.append({
                    'type': 'sentence_improvement',
                    'issue': sentence,
                    'suggestion': 'Add specific numbers or quantify achievements',
                    'example': 'Instead of "managed various projects" → "managed 15+ concurrent projects"'
                })
            
            # Check for missing quantification
            if re.search(r'\b(improved|increased|reduced|saved|managed)\b', sentence, re.IGNORECASE) and not re.search(r'\d+|%', sentence):
                improvements.append({
                    'type': 'sentence_improvement',
                    'issue': sentence,
                    'suggestion': 'Quantify your achievements with specific numbers or percentages',
                    'example': 'Instead of "improved efficiency" → "improved efficiency by 25%"'
                })

        # Check for professional language
        if re.search(r'\b(achieved|managed|led|developed|implemented|improved)\b', text, re.IGNORECASE):
            correct_elements.append("✅ Uses professional action words")
        
        if not re.search(r'\b(um|uh|like|you know)\b', text, re.IGNORECASE):
            correct_elements.append("✅ Professional tone maintained")
            
        # Check for quantified achievements
        if re.search(r'\d+%|\$\d+|\d+\s*(million|thousand|projects|clients|team)', text, re.IGNORECASE):
            correct_elements.append("✅ Includes quantified achievements")
        
        return {
            'issues': issues[:15],  # Top 15 issues
            'improvements': improvements[:10],  # Top 10 sentence improvements
            'correct_elements': correct_elements,
            'total_issues': len(issues),
            'total_improvements': len(improvements),
            'grammar_errors': grammar_errors_found,
            'formatting_issues': formatting_issues,
            'spelling_issues': spelling_issues,
            'overall_score': max(0, 10 - len(issues))  # Score out of 10
        }

    def _analyze_hard_skills(self, text: str, domain_data: Dict) -> Dict:
        """Analyze hard skills with heatmap data using ordered keyword checking"""
        # Use the new method to get keywords in order
        domain_name = domain_data.get('name', 'Unknown')
        
        # Get the domain key from the domain name
        domain_key = None
        for key, data in self.domain_keywords.domains.items():
            if data.get('name') == domain_name:
                domain_key = key
                break
        
        if domain_key:
            keyword_analysis = self.domain_keywords.check_keywords_in_order(text, domain_key)
            found_skills = keyword_analysis['present_keywords']
            missing_skills = keyword_analysis['missing_keywords']
            relevance_score = keyword_analysis['coverage_percentage']
        else:
            # Fallback to old method if domain not found
            domain_keywords = domain_data.get('keywords', [])
            found_skills = []
            missing_skills = []
            
            for skill in domain_keywords:
                if skill.lower() in text.lower():
                    found_skills.append(skill)
                else:
                    missing_skills.append(skill)
            
            total_keywords = len(domain_keywords)
            relevance_score = (len(found_skills) / total_keywords * 100) if total_keywords > 0 else 0
        
        return {
            'found_skills': found_skills,  # All found skills in order
            'missing_skills': missing_skills,  # All missing skills in order
            'relevance_score': round(relevance_score, 1),
            'density': 'High' if relevance_score >= 70 else 'Medium' if relevance_score >= 40 else 'Low',
            'total_found': len(found_skills),
            'total_available': len(found_skills) + len(missing_skills)
        }

    def _analyze_soft_skills(self, text: str) -> Dict:
        """Analyze soft skills presence"""
        found_soft_skills = []
        missing_soft_skills = []
        
        for skill in self.soft_skills:
            if skill.lower() in text.lower():
                found_soft_skills.append(skill)
            else:
                missing_soft_skills.append(skill)
        
        soft_score = (len(found_soft_skills) / len(self.soft_skills) * 100)
        
        return {
            'found_skills': found_soft_skills,
            'missing_skills': missing_soft_skills[:10],  # Top 10 missing
            'coverage_score': round(soft_score, 1),
            'assessment': 'Excellent' if soft_score >= 60 else 'Good' if soft_score >= 40 else 'Needs Improvement'
        }

    def _analyze_certifications(self, text: str, domain: str) -> Dict:
        """Analyze certifications and their relevance"""
        cert_mappings = {
            'auditing': ['cpa', 'cia', 'cisa', 'ca', 'acca', 'cma'],
            'taxation': ['cpa', 'ea', 'ctp', 'cmt', 'ca'],
            'finance': ['cfa', 'frm', 'cpa', 'ca', 'acca', 'cma']
        }
        
        relevant_certs = cert_mappings.get(domain, [])
        found_certs = []
        
        for cert in relevant_certs:
            if cert.upper() in text.upper():
                found_certs.append(cert.upper())
        
        return {
            'found_certifications': found_certs,
            'relevant_for_domain': relevant_certs,
            'missing_key_certs': [cert.upper() for cert in relevant_certs if cert.upper() not in found_certs],
            'value_assessment': 'High Value' if found_certs else 'Consider Adding'
        }

    def _generate_personalized_recommendations(self, about_score: float, edu_score: float, 
                                              exp_score: float, skills_score: float,
                                              hard_skills: Dict, soft_skills: Dict, 
                                              grammar_issues: List, resume_text: str, domain: str) -> List[str]:
        """Generate highly personalized recommendations based on actual resume content"""
        recommendations = []
        text_lower = resume_text.lower()
        
        # Analyze resume context and detect experience level
        experience_level = self._detect_experience_level(text_lower)
        current_roles = self._extract_current_roles(text_lower)
        
        # Critical missing elements (highest priority)
        missing_critical = self._identify_missing_critical_elements(text_lower, domain)
        for element in missing_critical[:2]:  # Top 2 critical items
            recommendations.append(f"🚨 CRITICAL: {element}")
        
        # Experience-level specific recommendations
        if experience_level == "entry":
            if not re.search(r'\b(?:project|coursework|internship|volunteer)\b', text_lower):
                recommendations.append("📚 Add academic projects, internships, or relevant coursework to strengthen entry-level profile")
            if not re.search(r'\b(?:gpa|honor|award|scholarship)\b', text_lower):
                recommendations.append("🏆 Include academic achievements (GPA 3.5+, honors, awards) to demonstrate excellence")
        
        elif experience_level == "mid":
            if not re.search(r'\b(?:led|managed|supervised|coordinated)\b', text_lower):
                recommendations.append("👥 Highlight leadership experience - show how you've guided teams or projects")
            if not re.search(r'\d+%|\$\d+|improved.*\d+|increased.*\d+', text_lower):
                recommendations.append("📊 Quantify your impact with specific percentages and dollar amounts")
        
        elif experience_level == "senior":
            if not re.search(r'\b(?:strategy|vision|transformation|initiative|mentored)\b', text_lower):
                recommendations.append("🎯 Emphasize strategic leadership and mentoring - show your senior-level contributions")
        
        # Domain-specific content analysis
        domain_recs = self._get_domain_specific_recommendations(text_lower, domain, hard_skills)
        recommendations.extend(domain_recs[:2])  # Top 2 domain recommendations
        
        # Content-specific improvements
        content_improvements = self._analyze_content_for_improvements(text_lower, current_roles)
        recommendations.extend(content_improvements[:2])  # Top 2 content improvements
        
        # Section-specific personalized advice
        if about_score < 7:
            about_rec = self._get_personalized_about_improvement(text_lower, experience_level, current_roles)
            recommendations.append(about_rec)
        
        if exp_score < 7:
            exp_rec = self._get_personalized_experience_improvement(text_lower, experience_level)
            recommendations.append(exp_rec)
        
        # Language and grammar improvements
        if grammar_issues:
            language_rec = self._get_personalized_language_improvement(grammar_issues, text_lower)
            recommendations.append(language_rec)
        
        # Remove duplicates and return top recommendations
        seen = set()
        final_recs = []
        for rec in recommendations:
            if rec not in seen and len(final_recs) < 8:
                seen.add(rec)
                final_recs.append(rec)
        
        return final_recs
    
    def _analyze_contact_information(self, text: str) -> Dict[str, bool]:
        """Analyze contact information presence in resume"""
        text_lower = text.lower()
        
        # Check for name (assumes proper capitalization in original text)
        has_name = bool(re.search(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', text))
        
        # Check for email
        has_email = bool(re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text))
        
        # Check for phone number (various formats)
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # US format
            r'\+\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b',  # International
            r'\(\d{3}\)\s*\d{3}[-.]?\d{4}\b'  # (xxx) xxx-xxxx
        ]
        has_phone = any(re.search(pattern, text) for pattern in phone_patterns)
        
        # Check for LinkedIn
        linkedin_patterns = [
            r'linkedin\.com',
            r'linkedin',
            r'/in/',
            r'linkedin\.in'
        ]
        has_linkedin = any(pattern in text_lower for pattern in linkedin_patterns)
        
        return {
            'has_name': has_name,
            'has_email': has_email, 
            'has_phone': has_phone,
            'has_linkedin': has_linkedin
        }
    
    def _analyze_word_count(self, text: str) -> Dict[str, any]:
        """Analyze word count and provide recommendations based on experience level"""
        words = text.split()
        word_count = len(words)
        
        # Define word count ranges
        fresher_min, fresher_max = 450, 600
        experienced_min, experienced_max = 600, 800
        
        # Determine experience level from text
        experience_indicators = ['years', 'year', 'experience', 'experienced', 'senior', 'lead', 'manager', 'director']
        years_mentioned = []
        
        # Look for year patterns
        import re
        year_patterns = re.findall(r'(\d+)\s*(?:years?|yrs?)', text.lower())
        if year_patterns:
            years_mentioned = [int(year) for year in year_patterns if int(year) <= 50]
        
        # Determine if fresher or experienced
        max_experience = max(years_mentioned) if years_mentioned else 0
        is_fresher = max_experience < 2
        
        # Calculate recommendations
        if is_fresher:
            is_optimal = fresher_min <= word_count <= fresher_max
            if word_count < fresher_min:
                recommendation = f"Consider expanding your resume. Add {fresher_min - word_count} more words to reach the optimal range for freshers (450-600 words)."
                status = "too_short"
            elif word_count > fresher_max:
                recommendation = f"Consider condensing your resume. Remove {word_count - fresher_max} words to stay within the optimal range for freshers (450-600 words)."
                status = "too_long"
            else:
                recommendation = "Your resume length is optimal for a fresher profile."
                status = "optimal"
        else:
            is_optimal = experienced_min <= word_count <= experienced_max
            if word_count < experienced_min:
                recommendation = f"Consider expanding your resume. Add {experienced_min - word_count} more words to reach the optimal range for experienced professionals (600-800 words)."
                status = "too_short"
            elif word_count > experienced_max:
                recommendation = f"Consider condensing your resume. Remove {word_count - experienced_max} words to stay within the optimal range for experienced professionals (600-800 words)."
                status = "too_long"
            else:
                recommendation = "Your resume length is optimal for an experienced professional."
                status = "optimal"
        
        return {
            'word_count': word_count,
            'is_fresher': is_fresher,
            'is_optimal': is_optimal,
            'status': status,
            'recommendation': recommendation,
            'target_range': f"{fresher_min}-{fresher_max} words" if is_fresher else f"{experienced_min}-{experienced_max} words"
        }
    
    def _analyze_resume_context(self, text_lower: str, recommendations: List[str], domain: str):
        """Analyze the actual resume content for context-aware recommendations"""
        # Check for specific industry context
        if domain == "auditing" and "sox" not in text_lower and "compliance" not in text_lower:
            recommendations.append("🔍 Add SOX compliance or regulatory experience to strengthen auditing profile")
        
        if domain == "taxation" and "tax" not in text_lower:
            recommendations.append("📋 Include specific tax-related experience (preparation, planning, compliance)")
    
    def _detect_experience_level(self, text_lower: str) -> str:
        """Detect experience level from resume content"""
        if re.search(r'\b(?:senior|director|manager|lead|vp|vice president|head of)\b', text_lower):
            return "senior"
        elif re.search(r'\b(?:analyst|associate|specialist|coordinator)\b', text_lower):
            return "mid"
        elif re.search(r'\b(?:intern|trainee|entry|graduate|junior|assistant)\b', text_lower):
            return "entry"
        
        # Check years of experience
        years_match = re.search(r'\b(\d+)\+?\s*years?\b', text_lower)
        if years_match:
            years = int(years_match.group(1))
            if years >= 8: return "senior"
            elif years >= 3: return "mid"
            else: return "entry"
        
        return "mid"  # default
    
    def _extract_current_roles(self, text_lower: str) -> List[str]:
        """Extract current or recent role titles from resume"""
        roles = []
        role_patterns = [
            r'\b(senior|lead|principal|director|manager|analyst|associate|specialist|coordinator|auditor|accountant)\b'
        ]
        
        for pattern in role_patterns:
            matches = re.findall(pattern, text_lower)
            roles.extend(matches)
        
        return list(set(roles))
    
    def _identify_target_improvements(self, text_lower: str, domain: str, experience_level: str) -> List[str]:
        """Identify specific improvements based on career level and domain"""
        improvements = []
        
        # Experience-level specific gaps
        if experience_level == "entry" and not re.search(r'\b(?:project|coursework|volunteer)\b', text_lower):
            improvements.append("Add relevant projects or coursework to strengthen entry-level profile")
        
        if experience_level == "senior" and not re.search(r'\b(?:strategy|transformation|leadership)\b', text_lower):
            improvements.append("Emphasize strategic leadership and transformation initiatives")
        
        return improvements
    
    def _identify_missing_critical_elements(self, text_lower: str, domain: str) -> List[str]:
        """Identify critical missing elements based on domain"""
        missing = []
        
        # Universal critical elements
        if not re.search(r'\d+', text_lower):
            missing.append("Add quantifiable achievements (percentages, dollar amounts, numbers)")
        
        if not re.search(r'\b(?:achieved|managed|led|developed|implemented)\b', text_lower):
            missing.append("Use strong action verbs to start experience bullet points")
        
        # Domain-specific critical elements
        domain_requirements = {
            "auditing": ["audit", "compliance", "risk", "controls"],
            "taxation": ["tax", "return", "planning", "compliance"],
            "finance": ["financial", "analysis", "budget", "forecasting"]
        }
        
        if domain in domain_requirements:
            required_terms = domain_requirements[domain]
            missing_terms = [term for term in required_terms if term not in text_lower]
            if missing_terms:
                missing.append(f"Include {domain} keywords: {', '.join(missing_terms)}")
        
        return missing
    
    def _get_domain_specific_recommendations(self, text_lower: str, domain: str, hard_skills: Dict) -> List[str]:
        """Get domain-specific recommendations based on actual content"""
        recommendations = []
        
        if domain == "auditing":
            if "sox" not in text_lower:
                recommendations.append("🔍 Add SOX compliance experience - critical for auditing roles")
            if "gaap" not in text_lower and "ifrs" not in text_lower:
                recommendations.append("📊 Include GAAP/IFRS knowledge - fundamental for auditing")
        
        elif domain == "taxation":
            if "tax preparation" not in text_lower:
                recommendations.append("📋 Specify tax preparation experience (individual, corporate, partnership)")
            if not re.search(r'\b(?:1040|1120|1065)\b', text_lower):
                recommendations.append("📄 Add specific tax form experience (1040, 1120, 1065)")
        
        elif domain == "finance":
            if "financial modeling" not in text_lower:
                recommendations.append("📈 Include financial modeling experience - highly valued in finance")
            if "excel" not in text_lower:
                recommendations.append("💻 Emphasize Excel proficiency - essential for finance roles")
        
        return recommendations
    
    def _analyze_content_for_improvements(self, text_lower: str, current_roles: List[str]) -> List[str]:
        """Analyze actual content for specific improvements"""
        improvements = []
        
        # Check for weak language
        if "responsible for" in text_lower:
            improvements.append("💪 Replace 'responsible for' with strong action verbs like 'managed', 'led', 'executed'")
        
        if "helped" in text_lower or "assisted" in text_lower:
            improvements.append("🎯 Replace 'helped/assisted' with specific contributions you made")
        
        # Check for missing quantification
        sentences = text_lower.split('.')
        unquantified_achievements = []
        for sentence in sentences[:10]:  # Check first 10 sentences
            if any(word in sentence for word in ['improved', 'increased', 'reduced', 'saved']) and not re.search(r'\d+', sentence):
                unquantified_achievements.append(sentence.strip()[:50] + "...")
        
        if unquantified_achievements:
            improvements.append(f"📊 Quantify achievements like: '{unquantified_achievements[0]}'")
        
        return improvements
    
    def _get_personalized_about_improvement(self, text_lower: str, experience_level: str, current_roles: List[str]) -> str:
        """Get personalized about section improvement"""
        if experience_level == "entry":
            return "📝 Strengthen summary with academic achievements, relevant coursework, and career objectives"
        elif experience_level == "senior":
            return "🎯 Enhance summary to emphasize strategic leadership and business impact"
        else:
            return "📝 Improve summary with quantified achievements and specific expertise areas"
    
    def _get_personalized_experience_improvement(self, text_lower: str, experience_level: str) -> str:
        """Get personalized experience section improvement"""
        if not re.search(r'\d+%|\$\d+', text_lower):
            return "📊 Add specific metrics to quantify your impact (percentages, dollar amounts, timeframes)"
        elif experience_level == "senior" and not re.search(r'\bteam\b|\bstaff\b', text_lower):
            return "👥 Highlight team leadership and staff development responsibilities"
        else:
            return "💼 Strengthen experience descriptions with more specific achievements and outcomes"
    
    def _get_personalized_language_improvement(self, grammar_issues: List, text_lower: str) -> str:
        """Get personalized language improvement based on actual issues found"""
        if grammar_issues:
            issue_types = [issue.get('type', 'grammar') for issue in grammar_issues[:3]]
            return f"✏️ Address {len(grammar_issues)} language issues: focus on {', '.join(set(issue_types))}"
        else:
            return "✏️ Review for consistency in tense usage and professional language throughout"

    def _generate_heatmap_data(self, about_score: float, edu_score: float, 
                              exp_score: float, skills_score: float,
                              hard_skills: Dict, soft_skills: Dict) -> Dict:
        """Generate heatmap visualization data"""
        return {
            'section_scores': {
                'About Me': about_score,
                'Education': edu_score,
                'Experience': exp_score,
                'Skills': skills_score
            },
            'skills_density': {
                'Hard Skills': hard_skills['relevance_score'],
                'Soft Skills': soft_skills['coverage_score']
            },
            'overall_health': {
                'Content Quality': (about_score + exp_score) / 2 * 10,
                'Qualifications': (edu_score + skills_score) / 2 * 10,
                'Professional Impact': exp_score * 10
            }
        }

    def _clean_text(self, text: str) -> str:
        """Clean and normalize resume text"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.,;:()\-]', '', text)
        return text.strip()