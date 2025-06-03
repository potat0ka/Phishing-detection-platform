from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to detection history
    detections = db.relationship('Detection', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username=None, email=None):
        if username:
            self.username = username
        if email:
            self.email = email
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    input_type = db.Column(db.String(20), nullable=False)  # 'url', 'email', 'message'
    input_content = db.Column(db.Text, nullable=False)
    result = db.Column(db.String(20), nullable=False)  # 'safe', 'phishing', 'suspicious'
    confidence_score = db.Column(db.Float, nullable=False)
    reasons = db.Column(db.Text)  # JSON string of reasons
    ai_analysis = db.Column(db.Text)  # AI model analysis details
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_id=None, input_type=None, input_content=None, result=None, confidence_score=None, reasons=None, ai_analysis=None):
        if user_id is not None:
            self.user_id = user_id
        if input_type:
            self.input_type = input_type
        if input_content:
            self.input_content = input_content
        if result:
            self.result = result
        if confidence_score is not None:
            self.confidence_score = confidence_score
        if reasons:
            self.reasons = reasons
        if ai_analysis:
            self.ai_analysis = ai_analysis
    
    def __repr__(self):
        return f'<Detection {self.id}: {self.result}>'

class PhishingTip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'email', 'url', 'general'
    priority = db.Column(db.Integer, default=1)  # 1=high, 2=medium, 3=low
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, title=None, content=None, category=None, priority=1):
        if title:
            self.title = title
        if content:
            self.content = content
        if category:
            self.category = category
        self.priority = priority
    
    def __repr__(self):
        return f'<PhishingTip {self.title}>'
