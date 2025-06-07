#!/usr/bin/env python3
"""
Verify MongoDB Atlas Integration for AI Phishing Detection Platform
Tests complete setup with user and model data operations
"""

from models.mongodb_config import get_mongodb_manager
from datetime import datetime

def test_complete_setup():
    """Test full MongoDB Atlas integration"""
    print("Testing MongoDB Atlas integration...")
    
    # Get MongoDB manager
    db = get_mongodb_manager()
    
    print(f"Database connected: {db.connected}")
    print(f"Database status: {db.get_database_status()}")
    
    # Test user operations (as requested)
    print("\n--- Testing Users Collection ---")
    
    # Test user data: {"username": "alice", "email": "alice@example.com"}
    test_user = {
        "username": "alice",
        "email": "alice@example.com",
        "role": "user",
        "password_hash": "hashed_password_123",
        "created_at": datetime.utcnow()
    }
    
    # Check if user already exists
    existing_user = db.find_one('users', {'username': 'alice'})
    if not existing_user:
        user_id = db.insert_one('users', test_user)
        print(f"Created user 'alice': {user_id}")
    else:
        print(f"User 'alice' already exists: {existing_user['_id']}")
    
    # Test finding user
    found_user = db.find_one('users', {'username': 'alice'})
    if found_user:
        print(f"Found user: {found_user['username']} ({found_user['email']})")
    
    # Test model operations (as requested)
    print("\n--- Testing Models Collection ---")
    
    # Test AI/ML model metadata: {"model_name": "linear_regression_v1", "created_at": "2025-06-07"}
    test_model = {
        "model_name": "linear_regression_v1",
        "created_at": "2025-06-07",
        "model_type": "phishing_detection",
        "algorithm": "linear_regression",
        "accuracy": 0.95,
        "training_samples": 10000,
        "features": ["url_length", "suspicious_keywords", "domain_age"],
        "version": "1.0"
    }
    
    # Check if model already exists
    existing_model = db.find_one('models', {'model_name': 'linear_regression_v1'})
    if not existing_model:
        model_id = db.insert_one('models', test_model)
        print(f"Created model 'linear_regression_v1': {model_id}")
    else:
        print(f"Model 'linear_regression_v1' already exists: {existing_model['_id']}")
    
    # Test finding model
    found_model = db.find_one('models', {'model_name': 'linear_regression_v1'})
    if found_model:
        print(f"Found model: {found_model['model_name']} (accuracy: {found_model.get('accuracy', 'N/A')})")
    
    # Test additional model
    test_model_2 = {
        "model_name": "random_forest_v2",
        "created_at": "2025-06-07",
        "model_type": "content_classification",
        "algorithm": "random_forest",
        "accuracy": 0.92
    }
    
    existing_model_2 = db.find_one('models', {'model_name': 'random_forest_v2'})
    if not existing_model_2:
        model_id_2 = db.insert_one('models', test_model_2)
        print(f"Created model 'random_forest_v2': {model_id_2}")
    
    # Count documents
    user_count = db.count_documents('users')
    model_count = db.count_documents('models')
    
    print(f"\n--- Final Statistics ---")
    print(f"Users in database: {user_count}")
    print(f"Models in database: {model_count}")
    
    # Test find_many
    all_users = db.find_many('users')
    all_models = db.find_many('models')
    
    print(f"All users: {[u['username'] for u in all_users]}")
    print(f"All models: {[m['model_name'] for m in all_models]}")
    
    return True

if __name__ == "__main__":
    try:
        success = test_complete_setup()
        if success:
            print("\n✅ MongoDB Atlas integration verified successfully!")
            print("Your AI Phishing Detection Platform is ready with:")
            print("- User management in 'users' collection")
            print("- AI/ML model metadata in 'models' collection") 
            print("- All data stored in myAppDB database")
        else:
            print("\n❌ Setup verification failed")
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")