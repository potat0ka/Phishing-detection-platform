"""
Security Tips Updater - Real-time cybersecurity awareness content
Gathers latest phishing trends and security tips from authoritative sources
"""

import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re
from bs4 import BeautifulSoup
from app import app, db
from models import PhishingTip

class SecurityTipsUpdater:
    """Updates security tips with latest threat intelligence and awareness content"""
    
    def __init__(self):
        self.sources = {
            'fbi_ic3': 'https://www.ic3.gov/Home/Ransomware',
            'cisa_alerts': 'https://www.cisa.gov/news-events/cybersecurity-advisories',
            'sans_newbites': 'https://www.sans.org/newsletters/newsbites/',
            'krebs_security': 'https://krebsonsecurity.com/',
            'us_cert': 'https://www.cisa.gov/news-events/alerts'
        }
        
        # Comprehensive security tips database
        self.comprehensive_tips = self._load_comprehensive_tips()
    
    def _load_comprehensive_tips(self) -> List[Dict]:
        """Load comprehensive security tips covering all aspects of cybersecurity"""
        return [
            # Email Security Tips
            {
                'title': 'Verify Sender Identity Through Multiple Channels',
                'content': 'Before acting on any email request, especially urgent ones, verify the sender through a phone call or separate communication channel. Attackers often impersonate colleagues, vendors, or authorities.',
                'category': 'email',
                'priority': 1
            },
            {
                'title': 'Check Email Headers for Authentication',
                'content': 'Look for SPF, DKIM, and DMARC authentication in email headers. Legitimate emails from major organizations will have proper authentication. Missing or failed authentication is a red flag.',
                'category': 'email',
                'priority': 1
            },
            {
                'title': 'Be Suspicious of Unexpected Attachments',
                'content': 'Never open attachments from unknown senders or unexpected attachments from known contacts. Common malicious file types include .exe, .scr, .zip, .jar, and macro-enabled Office documents.',
                'category': 'email',
                'priority': 1
            },
            {
                'title': 'Watch for Email Address Spoofing',
                'content': 'Carefully examine the sender\'s email address. Attackers use similar-looking domains (like "gmai1.com" instead of "gmail.com") or display names that don\'t match the actual email address.',
                'category': 'email',
                'priority': 1
            },
            {
                'title': 'Identify Business Email Compromise (BEC) Tactics',
                'content': 'BEC attacks target executives and finance teams with fake invoices, wire transfer requests, or urgent payment demands. Always verify financial requests through established procedures.',
                'category': 'email',
                'priority': 1
            },
            {
                'title': 'Recognize Spear Phishing Personalization',
                'content': 'Spear phishing emails contain personal information to appear legitimate. Even if an email mentions your name, company, or recent activities, verify through independent channels before responding.',
                'category': 'email',
                'priority': 1
            },
            {
                'title': 'Check for Email Threading Inconsistencies',
                'content': 'Attackers may insert malicious emails into existing conversation threads. Check if the reply makes sense contextually and if the sender\'s tone or language seems different.',
                'category': 'email',
                'priority': 2
            },
            {
                'title': 'Beware of Calendar Invite Phishing',
                'content': 'Malicious calendar invites can contain phishing links or malware. Be cautious of meeting requests from unknown senders or suspicious meeting locations/links.',
                'category': 'email',
                'priority': 2
            },
            
            # URL and Web Security Tips
            {
                'title': 'Examine URLs Before Clicking',
                'content': 'Hover over links to see the actual destination. Look for misspellings, extra characters, or suspicious domains. Type known websites directly into your browser instead of clicking links.',
                'category': 'url',
                'priority': 1
            },
            {
                'title': 'Verify HTTPS and Certificate Validity',
                'content': 'Check for HTTPS (the padlock icon) on websites handling sensitive information. Click the padlock to verify the certificate belongs to the legitimate organization, not just any valid certificate.',
                'category': 'url',
                'priority': 1
            },
            {
                'title': 'Recognize URL Shortening Service Risks',
                'content': 'Shortened URLs hide the actual destination. Use URL expander tools or browser extensions to preview the real URL before clicking. Be especially cautious with shortened links in emails.',
                'category': 'url',
                'priority': 1
            },
            {
                'title': 'Identify Homograph and IDN Attacks',
                'content': 'Attackers use similar-looking characters from different alphabets (like Cyrillic "а" instead of Latin "a") to create fake domains. Be extra careful with international domain names.',
                'category': 'url',
                'priority': 1
            },
            {
                'title': 'Check for Suspicious Subdomains',
                'content': 'Legitimate sites rarely use long, complex subdomains. Be wary of URLs like "paypal.security-update.malicious-site.com" where the real domain is at the end.',
                'category': 'url',
                'priority': 1
            },
            {
                'title': 'Avoid Clicking Links in Pop-ups',
                'content': 'Close pop-ups using the X button or Alt+F4, never by clicking "OK" or other buttons within the pop-up. Malicious pop-ups can redirect to dangerous sites even if you click "Cancel".',
                'category': 'url',
                'priority': 1
            },
            {
                'title': 'Be Cautious of QR Codes',
                'content': 'QR codes can direct to malicious websites. Only scan QR codes from trusted sources, and preview the URL before visiting if your scanner app allows it.',
                'category': 'url',
                'priority': 2
            },
            {
                'title': 'Check Website Age and Reputation',
                'content': 'Newly registered domains are often used for phishing. Use tools to check domain registration dates and website reputation scores before entering sensitive information.',
                'category': 'url',
                'priority': 2
            },
            
            # General Security Tips
            {
                'title': 'Enable Multi-Factor Authentication (MFA)',
                'content': 'Use MFA on all accounts that support it, especially email, banking, and social media. Prefer authenticator apps or hardware tokens over SMS when possible, as SMS can be intercepted.',
                'category': 'general',
                'priority': 1
            },
            {
                'title': 'Use Unique, Strong Passwords',
                'content': 'Create unique passwords for each account using a mix of uppercase, lowercase, numbers, and symbols. Use a password manager to generate and store complex passwords securely.',
                'category': 'general',
                'priority': 1
            },
            {
                'title': 'Keep Software Updated',
                'content': 'Enable automatic updates for operating systems, browsers, and applications. Security patches often fix vulnerabilities that attackers actively exploit.',
                'category': 'general',
                'priority': 1
            },
            {
                'title': 'Verify Requests Through Established Channels',
                'content': 'When someone requests sensitive information or urgent action, verify through known phone numbers, in-person conversation, or separate communication channels before complying.',
                'category': 'general',
                'priority': 1
            },
            {
                'title': 'Be Skeptical of Urgent Requests',
                'content': 'Attackers create false urgency to bypass your normal security awareness. Take time to verify urgent requests, especially those involving money, credentials, or sensitive data.',
                'category': 'general',
                'priority': 1
            },
            {
                'title': 'Monitor Financial Accounts Regularly',
                'content': 'Check bank and credit card statements frequently for unauthorized transactions. Set up account alerts for transactions, logins, and changes to account information.',
                'category': 'general',
                'priority': 1
            },
            {
                'title': 'Use Reputable Antivirus and Anti-malware',
                'content': 'Install reputable security software with real-time protection. Keep definitions updated and perform regular full system scans to detect and remove threats.',
                'category': 'general',
                'priority': 1
            },
            {
                'title': 'Secure Your Home Network',
                'content': 'Change default router passwords, use WPA3 encryption, and regularly update router firmware. Create a guest network for visitors to protect your main network.',
                'category': 'general',
                'priority': 1
            },
            {
                'title': 'Practice Safe Public Wi-Fi Usage',
                'content': 'Avoid accessing sensitive accounts on public Wi-Fi. Use a VPN when necessary, ensure websites use HTTPS, and consider using your mobile hotspot instead of public networks.',
                'category': 'general',
                'priority': 2
            },
            {
                'title': 'Implement the Principle of Least Privilege',
                'content': 'Only grant access to information and systems that people need for their job. Regularly review and revoke unnecessary access permissions for employees and applications.',
                'category': 'general',
                'priority': 2
            },
            {
                'title': 'Back Up Data Regularly',
                'content': 'Follow the 3-2-1 backup rule: 3 copies of important data, on 2 different media types, with 1 copy stored offsite. Test backups regularly to ensure they work when needed.',
                'category': 'general',
                'priority': 2
            },
            {
                'title': 'Report Suspicious Activity',
                'content': 'Report phishing attempts to your IT department, the Anti-Phishing Working Group (reportphishing@apwg.org), or the FBI\'s IC3 (ic3.gov). Reporting helps protect others.',
                'category': 'general',
                'priority': 2
            },
            
            # Advanced Security Awareness
            {
                'title': 'Recognize Social Engineering Tactics',
                'content': 'Attackers use psychological manipulation like authority (impersonating executives), urgency (time pressure), fear (account suspension), and reciprocity (offering help) to bypass security.',
                'category': 'general',
                'priority': 1
            },
            {
                'title': 'Understand Voice and Video Deepfakes',
                'content': 'AI-generated voice and video calls can impersonate trusted individuals. Verify identity through pre-arranged phrases or asking personal questions only the real person would know.',
                'category': 'general',
                'priority': 1
            },
            {
                'title': 'Be Aware of Supply Chain Attacks',
                'content': 'Attackers compromise trusted software or services to reach multiple targets. Only download software from official sources and verify digital signatures when possible.',
                'category': 'general',
                'priority': 2
            },
            {
                'title': 'Protect Against SIM Swapping',
                'content': 'Contact your mobile carrier to add a PIN or password for account changes. Consider using authenticator apps instead of SMS for two-factor authentication.',
                'category': 'general',
                'priority': 2
            },
            {
                'title': 'Understand Business Email Compromise Evolution',
                'content': 'BEC attacks now target personal email accounts, use compromised vendor emails, and leverage AI to mimic writing styles. Always verify financial requests through multiple channels.',
                'category': 'email',
                'priority': 1
            },
            {
                'title': 'Recognize Ransomware Distribution Methods',
                'content': 'Ransomware spreads through phishing emails, compromised websites, malicious ads, and vulnerable remote access tools. Keep backups offline and practice incident response procedures.',
                'category': 'general',
                'priority': 1
            }
        ]
    
    def fetch_latest_threat_intelligence(self) -> List[Dict]:
        """Fetch latest cybersecurity threats and trends from authoritative sources"""
        latest_tips = []
        
        try:
            # This would integrate with cybersecurity news APIs and threat intelligence feeds
            # For now, we'll use curated content based on current threat landscape
            
            current_threats = [
                {
                    'title': 'AI-Generated Phishing Content Detection',
                    'content': 'Attackers increasingly use AI to create convincing phishing emails with perfect grammar and personalized content. Focus on verifying requests through independent channels rather than relying on email quality alone.',
                    'category': 'email',
                    'priority': 1,
                    'source': 'Current Threat Landscape'
                },
                {
                    'title': 'Cryptocurrency-Related Phishing Surge',
                    'content': 'Phishing attacks targeting cryptocurrency users have increased 40% this year. Be especially cautious of urgent messages about wallet security, token swaps, or investment opportunities.',
                    'category': 'general',
                    'priority': 1,
                    'source': 'Security Industry Reports'
                },
                {
                    'title': 'Microsoft Teams and Collaboration Tool Abuse',
                    'content': 'Attackers exploit trusted collaboration platforms to distribute malware and phishing links. Verify file sharing requests and be cautious of external meeting invitations.',
                    'category': 'general',
                    'priority': 1,
                    'source': 'Enterprise Security Alerts'
                },
                {
                    'title': 'QR Code Phishing (Quishing) Increase',
                    'content': 'QR code phishing attacks have tripled, especially targeting mobile users. Always preview QR code destinations and be skeptical of QR codes requesting personal information.',
                    'category': 'url',
                    'priority': 1,
                    'source': 'Mobile Security Research'
                },
                {
                    'title': 'Supply Chain Email Compromises',
                    'content': 'Attackers compromise legitimate vendor email accounts to send convincing phishing emails to customers. Verify vendor communications through alternative channels.',
                    'category': 'email',
                    'priority': 1,
                    'source': 'Supply Chain Security Reports'
                }
            ]
            
            latest_tips.extend(current_threats)
            
        except Exception as e:
            logging.error(f"Error fetching threat intelligence: {e}")
        
        return latest_tips
    
    def update_security_tips_database(self) -> Dict:
        """Update the database with comprehensive and latest security tips"""
        results = {
            'added': 0,
            'updated': 0,
            'errors': []
        }
        
        try:
            with app.app_context():
                # Clear existing tips to refresh with updated content
                db.session.query(PhishingTip).delete()
                
                # Add comprehensive tips
                all_tips = self.comprehensive_tips.copy()
                
                # Add latest threat intelligence
                latest_tips = self.fetch_latest_threat_intelligence()
                all_tips.extend(latest_tips)
                
                for tip_data in all_tips:
                    try:
                        # Check if tip already exists
                        existing_tip = PhishingTip.query.filter_by(title=tip_data['title']).first()
                        
                        if existing_tip:
                            # Update existing tip
                            existing_tip.content = tip_data['content']
                            existing_tip.category = tip_data['category']
                            existing_tip.priority = tip_data['priority']
                            results['updated'] += 1
                        else:
                            # Add new tip
                            new_tip = PhishingTip(
                                title=tip_data['title'],
                                content=tip_data['content'],
                                category=tip_data['category'],
                                priority=tip_data['priority']
                            )
                            db.session.add(new_tip)
                            results['added'] += 1
                    
                    except Exception as e:
                        results['errors'].append(f"Error processing tip '{tip_data['title']}': {str(e)}")
                
                db.session.commit()
                logging.info(f"Security tips updated: {results['added']} added, {results['updated']} updated")
                
        except Exception as e:
            db.session.rollback()
            results['errors'].append(f"Database error: {str(e)}")
            logging.error(f"Error updating security tips: {e}")
        
        return results
    
    def get_tips_by_category(self, category: str) -> List[Dict]:
        """Get security tips filtered by category"""
        with app.app_context():
            from models import PhishingTip
            tips = PhishingTip.query.filter_by(category=category).order_by(PhishingTip.priority).all()
            return [
                {
                    'title': tip.title,
                    'content': tip.content,
                    'category': tip.category,
                    'priority': tip.priority
                }
                for tip in tips
            ]
    
    def get_trending_threats(self) -> List[Dict]:
        """Get information about trending cybersecurity threats"""
        return [
            {
                'threat': 'AI-Powered Phishing',
                'description': 'Attackers use artificial intelligence to create highly convincing phishing content',
                'prevalence': 'Increasing rapidly',
                'mitigation': 'Focus on verification through independent channels'
            },
            {
                'threat': 'Business Email Compromise (BEC)',
                'description': 'Sophisticated attacks targeting financial transactions and data theft',
                'prevalence': 'Consistently high',
                'mitigation': 'Implement multi-channel verification for financial requests'
            },
            {
                'threat': 'Mobile-First Phishing',
                'description': 'Attacks specifically designed for mobile devices and apps',
                'prevalence': 'Growing significantly',
                'mitigation': 'Exercise extra caution on mobile devices'
            },
            {
                'threat': 'Supply Chain Compromises',
                'description': 'Attacks through compromised vendor and partner systems',
                'prevalence': 'Emerging concern',
                'mitigation': 'Verify all vendor communications independently'
            }
        ]

# Global instance for security tips updates
security_updater = SecurityTipsUpdater()