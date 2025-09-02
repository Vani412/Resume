from typing import Dict, List

class DomainKeywords:
    """
    Contains domain-specific keywords and skills for resume evaluation
    """
    
    def __init__(self):
        self.domains = {
            'general': {
                'name': 'General',
                'keywords': [
                    'finance basics', 'business strategy', 'corporate structure', 
                    'communication skills', 'excel', 'ethics in finance'
                ]
            },
            
            'accounting': {
                'name': 'Accounting',
                'keywords': [
                    'journal entries', 'ledger posting', 'trial balance', 'balance sheet', 
                    'profit & loss', 'depreciation', 'accruals', 'accounts payable', 
                    'accounts receivable'
                ]
            },
            
            'banking': {
                'name': 'Banking – Credit Manager / Debt Management',
                'keywords': [
                    'credit appraisal', 'loan underwriting', 'risk assessment', 
                    'npa management', 'debt restructuring', 'collateral evaluation', 
                    'cibil score'
                ]
            },
            
            'direct_tax': {
                'name': 'Direct Tax / Income Tax / Corporate Tax',
                'keywords': [
                    'income tax returns', 'tds', 'tcs', 'corporate tax planning', 
                    'tax audit', 'section 80c', 'section 10(10d)', 'mat', 'amt', 
                    'transfer pricing'
                ]
            },
            
            'fpa': {
                'name': 'FP&A (Financial Planning & Analysis)',
                'keywords': [
                    'forecasting', 'budgeting', 'variance analysis', 'financial modeling', 
                    'kpi tracking', 'dashboarding', 'scenario analysis'
                ]
            },
            
            'gst': {
                'name': 'GST / Indirect Taxes',
                'keywords': [
                    'gst compliance', 'input tax credit', 'e-way bill', 'gst return filing', 
                    'vat', 'excise', 'customs duty', 'indirect tax audit'
                ]
            },
            
            'internal_audit': {
                'name': 'Internal Audit',
                'keywords': [
                    'risk assessment', 'process control', 'sox compliance', 'internal controls', 
                    'audit trail', 'fraud detection', 'operational audit', 'control testing'
                ]
            },
            
            'investment_banking': {
                'name': 'Investment Banking',
                'keywords': [
                    'ipo', 'mergers & acquisitions (m&a)', 'valuation models', 'pitchbook', 
                    'equity financing', 'debt financing', 'dcf', 'lbo', 
                    'comparable companies analysis', 'capital markets'
                ]
            },
            
            'r2r': {
                'name': 'R2R (Record to Report)',
                'keywords': [
                    'financial closing', 'journal entries', 'general ledger', 'financial statements', 
                    'reconciliation', 'month-end close', 'trial balance', 'fixed assets accounting'
                ]
            },
            
            'statutory_audit': {
                'name': 'Statutory Audit',
                'keywords': [
                    'ifrs', 'gaap', 'audit report', 'external audit', 'compliance', 
                    'internal control', 'sampling techniques', 'auditor independence'
                ]
            },
            
            'wealth_management': {
                'name': 'Wealth Management',
                'keywords': [
                    'asset allocation', 'portfolio management', 'financial planning', 'risk tolerance', 
                    'retirement planning', 'investment advisory', 'mutual funds', 
                    'high-net-worth individuals (hnis)'
                ]
            },
            
            # Legacy domains for backward compatibility
            'auditing': {
                'name': 'Internal Audit',
                'keywords': [
                    'risk assessment', 'process control', 'sox compliance', 'internal controls', 
                    'audit trail', 'fraud detection', 'operational audit', 'control testing'
                ]
            },
            
            'taxation': {
                'name': 'Direct Tax / Income Tax / Corporate Tax',
                'keywords': [
                    'income tax returns', 'tds', 'tcs', 'corporate tax planning', 
                    'tax audit', 'section 80c', 'section 10(10d)', 'mat', 'amt', 
                    'transfer pricing'
                ]
            },
            
            'finance': {
                'name': 'FP&A (Financial Planning & Analysis)',
                'keywords': [
                    'forecasting', 'budgeting', 'variance analysis', 'financial modeling', 
                    'kpi tracking', 'dashboarding', 'scenario analysis'
                ]
            }
        }
    
    def get_domain_keywords(self, domain: str) -> Dict:
        """
        Get keywords for a specific domain
        
        Args:
            domain (str): Domain name
            
        Returns:
            Dict: Domain data including keywords
        """
        if domain not in self.domains:
            # Default to general if domain not found
            return self.domains.get('general', self.domains['accounting'])
        
        return self.domains[domain]
    
    def get_all_domains(self) -> List[str]:
        """Get list of all available domains"""
        # Return only the new domains, not legacy ones
        return [
            'general', 'accounting', 'banking', 'direct_tax', 'fpa', 
            'gst', 'internal_audit', 'investment_banking', 'r2r', 
            'statutory_audit', 'wealth_management'
        ]
    
    def get_legacy_domains(self) -> List[str]:
        """Get list of legacy domains for backward compatibility"""
        return ['auditing', 'taxation', 'finance']
    
    def search_keywords(self, query: str, domain: str = None) -> List[str]:
        """
        Search for keywords containing the query string
        
        Args:
            query (str): Search query
            domain (str, optional): Specific domain to search in
            
        Returns:
            List[str]: Matching keywords
        """
        query = query.lower()
        matching_keywords = []
        
        domains_to_search = [domain] if domain else list(self.domains.keys())
        
        for domain_name in domains_to_search:
            domain_data = self.domains[domain_name]
            for keyword in domain_data['keywords']:
                if query in keyword.lower():
                    matching_keywords.append(keyword)
        
        return list(set(matching_keywords))  # Remove duplicates
    
    def get_keyword_count(self, domain: str) -> int:
        """Get total number of keywords for a domain"""
        if domain not in self.domains:
            return 0
        return len(self.domains[domain]['keywords'])
    
    def add_custom_keywords(self, domain: str, keywords: List[str]):
        """
        Add custom keywords to a domain
        
        Args:
            domain (str): Target domain
            keywords (List[str]): List of keywords to add
        """
        if domain not in self.domains:
            raise ValueError(f"Domain '{domain}' not supported")
        
        existing_keywords = set(kw.lower() for kw in self.domains[domain]['keywords'])
        new_keywords = [kw for kw in keywords if kw.lower() not in existing_keywords]
        self.domains[domain]['keywords'].extend(new_keywords)
    
    def check_keywords_in_order(self, text: str, domain: str) -> Dict:
        """
        Check keywords in the exact order they appear in the domain definition
        
        Args:
            text (str): Resume text to check
            domain (str): Target domain
            
        Returns:
            Dict: Present and missing keywords in order
        """
        domain_data = self.get_domain_keywords(domain)
        keywords = domain_data['keywords']
        text_lower = text.lower()
        
        present_keywords = []
        missing_keywords = []
        
        for keyword in keywords:
            if keyword.lower() in text_lower:
                present_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        return {
            'present_keywords': present_keywords,
            'missing_keywords': missing_keywords,
            'total_keywords': len(keywords),
            'present_count': len(present_keywords),
            'missing_count': len(missing_keywords),
            'coverage_percentage': round((len(present_keywords) / len(keywords)) * 100, 1) if keywords else 0
        }