"""
Social Media Automation Platform for Newsletter Publishers
Handles scheduling, publishing, and A/B testing across multiple platforms
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import random

class Platform(Enum):
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"

class PostStatus(Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ABTestStatus(Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class SocialMediaPost:
    """Represents a social media post with all its metadata"""
    id: str
    title: str
    content: str
    platforms: List[Platform]
    scheduled_time: datetime
    status: PostStatus = PostStatus.DRAFT
    created_at: datetime = None
    published_at: datetime = None
    media_urls: List[str] = None
    hashtags: List[str] = None
    mentions: List[str] = None
    newsletter_link: str = None
    ab_test_id: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.media_urls is None:
            self.media_urls = []
        if self.hashtags is None:
            self.hashtags = []
        if self.mentions is None:
            self.mentions = []

@dataclass
class ABTestVariant:
    """Represents a variant in an A/B test"""
    id: str
    name: str
    content: str
    platforms: List[Platform]
    media_urls: List[str] = None
    hashtags: List[str] = None
    impressions: int = 0
    clicks: int = 0
    shares: int = 0
    comments: int = 0
    likes: int = 0
    engagement_rate: float = 0.0
    
    def __post_init__(self):
        if self.media_urls is None:
            self.media_urls = []
        if self.hashtags is None:
            self.hashtags = []

@dataclass
class ABTest:
    """Represents an A/B test configuration"""
    id: str
    name: str
    description: str
    variants: List[ABTestVariant]
    start_time: datetime
    end_time: datetime
    status: ABTestStatus = ABTestStatus.RUNNING
    traffic_split: List[int] = None  # Percentage split for each variant
    winner_variant_id: str = None
    confidence_level: float = 0.0
    
    def __post_init__(self):
        if self.traffic_split is None:
            # Equal split by default
            num_variants = len(self.variants)
            split = 100 // num_variants
            self.traffic_split = [split] * num_variants

class SocialMediaAutomation:
    """Main automation class for social media posting and A/B testing"""
    
    def __init__(self):
        self.posts: Dict[str, SocialMediaPost] = {}
        self.ab_tests: Dict[str, ABTest] = {}
        self.scheduled_posts = []
        self.analytics_data = {}
        
        # Platform API configurations (would be loaded from environment)
        self.platform_configs = {
            Platform.TWITTER: {"api_key": None, "api_secret": None, "access_token": None},
            Platform.FACEBOOK: {"app_id": None, "app_secret": None, "access_token": None},
            Platform.LINKEDIN: {"client_id": None, "client_secret": None, "access_token": None},
            Platform.INSTAGRAM: {"access_token": None, "business_account_id": None},
            Platform.TIKTOK: {"client_key": None, "client_secret": None, "access_token": None}
        }
    
    def generate_id(self, prefix: str = "") -> str:
        """Generate a unique ID"""
        timestamp = str(int(datetime.now().timestamp()))
        random_str = str(random.randint(1000, 9999))
        return f"{prefix}{timestamp}_{random_str}"
    
    def create_post(self, title: str, content: str, platforms: List[Platform], 
                   scheduled_time: datetime, **kwargs) -> str:
        """Create a new social media post"""
        post_id = self.generate_id("post_")
        
        post = SocialMediaPost(
            id=post_id,
            title=title,
            content=content,
            platforms=platforms,
            scheduled_time=scheduled_time,
            **kwargs
        )
        
        self.posts[post_id] = post
        self._schedule_post(post)
        
        logging.info(f"Created post {post_id} scheduled for {scheduled_time}")
        return post_id
    
    def create_ab_test(self, name: str, description: str, variants: List[Dict],
                      start_time: datetime, end_time: datetime) -> str:
        """Create a new A/B test"""
        test_id = self.generate_id("abtest_")
        
        # Convert variant dictionaries to ABTestVariant objects
        ab_variants = []
        for i, variant_data in enumerate(variants):
            variant_id = f"{test_id}_variant_{i}"
            variant = ABTestVariant(
                id=variant_id,
                name=variant_data.get('name', f'Variant {i+1}'),
                content=variant_data['content'],
                platforms=variant_data['platforms'],
                media_urls=variant_data.get('media_urls', []),
                hashtags=variant_data.get('hashtags', [])
            )
            ab_variants.append(variant)
        
        ab_test = ABTest(
            id=test_id,
            name=name,
            description=description,
            variants=ab_variants,
            start_time=start_time,
            end_time=end_time
        )
        
        self.ab_tests[test_id] = ab_test
        
        # Create posts for each variant
        for variant in ab_variants:
            post_id = self.create_post(
                title=f"{name} - {variant.name}",
                content=variant.content,
                platforms=variant.platforms,
                scheduled_time=start_time,
                ab_test_id=test_id,
                media_urls=variant.media_urls,
                hashtags=variant.hashtags
            )
            
        logging.info(f"Created A/B test {test_id} with {len(ab_variants)} variants")
        return test_id
    
    def _schedule_post(self, post: SocialMediaPost):
        """Add post to scheduling queue"""
        self.scheduled_posts.append(post)
        self.scheduled_posts.sort(key=lambda p: p.scheduled_time)
    
    def publish_post(self, post_id: str) -> Dict[str, bool]:
        """Publish a post to all specified platforms"""
        if post_id not in self.posts:
            raise ValueError(f"Post {post_id} not found")
        
        post = self.posts[post_id]
        results = {}
        
        for platform in post.platforms:
            try:
                success = self._publish_to_platform(post, platform)
                results[platform.value] = success
                
                if success:
                    logging.info(f"Successfully published post {post_id} to {platform.value}")
                else:
                    logging.error(f"Failed to publish post {post_id} to {platform.value}")
                    
            except Exception as e:
                logging.error(f"Error publishing to {platform.value}: {e}")
                results[platform.value] = False
        
        # Update post status based on results
        if all(results.values()):
            post.status = PostStatus.PUBLISHED
            post.published_at = datetime.now()
        elif any(results.values()):
            post.status = PostStatus.PUBLISHED  # Partial success
            post.published_at = datetime.now()
        else:
            post.status = PostStatus.FAILED
        
        return results
    
    def _publish_to_platform(self, post: SocialMediaPost, platform: Platform) -> bool:
        """Publish content to a specific platform (mock implementation)"""
        # In a real implementation, this would use actual platform APIs
        config = self.platform_configs[platform]
        
        if not config.get("access_token"):
            logging.warning(f"No access token configured for {platform.value}")
            return False
        
        # Mock API call - would be replaced with actual platform API calls
        logging.info(f"Publishing to {platform.value}: {post.content[:50]}...")
        
        # Simulate platform-specific formatting
        formatted_content = self._format_content_for_platform(post, platform)
        
        # Simulate API response
        success_rate = 0.95  # 95% success rate for simulation
        return random.random() < success_rate
    
    def _format_content_for_platform(self, post: SocialMediaPost, platform: Platform) -> str:
        """Format content according to platform requirements"""
        content = post.content
        
        if platform == Platform.TWITTER:
            # Twitter character limit
            if len(content) > 280:
                content = content[:277] + "..."
            
        elif platform == Platform.LINKEDIN:
            # LinkedIn prefers professional tone
            if post.newsletter_link:
                content += f"\n\nRead more: {post.newsletter_link}"
                
        elif platform == Platform.INSTAGRAM:
            # Instagram loves hashtags
            if post.hashtags:
                content += "\n\n" + " ".join([f"#{tag}" for tag in post.hashtags])
        
        elif platform == Platform.FACEBOOK:
            # Facebook allows longer content
            if post.newsletter_link:
                content += f"\n\nSubscribe to our newsletter: {post.newsletter_link}"
        
        return content
    
    def get_pending_posts(self) -> List[SocialMediaPost]:
        """Get posts that are ready to be published"""
        now = datetime.now()
        return [post for post in self.scheduled_posts 
                if post.scheduled_time <= now and post.status == PostStatus.SCHEDULED]
    
    def process_scheduled_posts(self):
        """Process all pending scheduled posts"""
        pending_posts = self.get_pending_posts()
        
        for post in pending_posts:
            try:
                results = self.publish_post(post.id)
                logging.info(f"Processed scheduled post {post.id}: {results}")
            except Exception as e:
                logging.error(f"Error processing post {post.id}: {e}")
                post.status = PostStatus.FAILED
    
    def update_analytics(self, post_id: str, platform: Platform, metrics: Dict):
        """Update analytics data for a post"""
        if post_id not in self.analytics_data:
            self.analytics_data[post_id] = {}
        
        if platform.value not in self.analytics_data[post_id]:
            self.analytics_data[post_id][platform.value] = {}
        
        self.analytics_data[post_id][platform.value].update(metrics)
        
        # Update A/B test data if applicable
        post = self.posts.get(post_id)
        if post and post.ab_test_id:
            self._update_ab_test_metrics(post.ab_test_id, post_id, metrics)
    
    def _update_ab_test_metrics(self, test_id: str, post_id: str, metrics: Dict):
        """Update A/B test metrics"""
        if test_id not in self.ab_tests:
            return
        
        ab_test = self.ab_tests[test_id]
        
        # Find the variant for this post
        for variant in ab_test.variants:
            if variant.id in post_id:  # Simple matching - would be more robust in production
                variant.impressions += metrics.get('impressions', 0)
                variant.clicks += metrics.get('clicks', 0)
                variant.shares += metrics.get('shares', 0)
                variant.comments += metrics.get('comments', 0)
                variant.likes += metrics.get('likes', 0)
                
                # Calculate engagement rate
                if variant.impressions > 0:
                    total_engagement = variant.clicks + variant.shares + variant.comments + variant.likes
                    variant.engagement_rate = (total_engagement / variant.impressions) * 100
                
                break
    
    def analyze_ab_test(self, test_id: str) -> Dict:
        """Analyze A/B test results and determine winner"""
        if test_id not in self.ab_tests:
            raise ValueError(f"A/B test {test_id} not found")
        
        ab_test = self.ab_tests[test_id]
        
        if ab_test.status != ABTestStatus.RUNNING:
            return {"status": "Test is not running"}
        
        # Check if test period has ended
        if datetime.now() < ab_test.end_time:
            return {"status": "Test still running", "variants": ab_test.variants}
        
        # Analyze results
        best_variant = max(ab_test.variants, key=lambda v: v.engagement_rate)
        
        # Simple statistical significance check (would be more robust in production)
        total_impressions = sum(v.impressions for v in ab_test.variants)
        if total_impressions < 1000:  # Minimum sample size
            confidence = 0.0
        else:
            # Simplified confidence calculation
            confidence = min(95.0, (total_impressions / 1000) * 80)
        
        ab_test.winner_variant_id = best_variant.id
        ab_test.confidence_level = confidence
        ab_test.status = ABTestStatus.COMPLETED
        
        return {
            "status": "completed",
            "winner": best_variant,
            "confidence": confidence,
            "variants": ab_test.variants
        }
    
    def get_analytics_report(self, start_date: datetime, end_date: datetime) -> Dict:
        """Generate analytics report for specified date range"""
        report = {
            "period": {"start": start_date, "end": end_date},
            "total_posts": 0,
            "successful_posts": 0,
            "failed_posts": 0,
            "platforms": {},
            "ab_tests": {},
            "top_performing_posts": []
        }
        
        # Analyze posts in date range
        relevant_posts = [
            post for post in self.posts.values()
            if start_date <= post.created_at <= end_date
        ]
        
        report["total_posts"] = len(relevant_posts)
        report["successful_posts"] = len([p for p in relevant_posts if p.status == PostStatus.PUBLISHED])
        report["failed_posts"] = len([p for p in relevant_posts if p.status == PostStatus.FAILED])
        
        # Platform breakdown
        for platform in Platform:
            platform_posts = [p for p in relevant_posts if platform in p.platforms]
            report["platforms"][platform.value] = {
                "posts": len(platform_posts),
                "success_rate": len([p for p in platform_posts if p.status == PostStatus.PUBLISHED]) / max(len(platform_posts), 1) * 100
            }
        
        # A/B test results
        relevant_tests = [
            test for test in self.ab_tests.values()
            if start_date <= test.start_time <= end_date
        ]
        
        for test in relevant_tests:
            report["ab_tests"][test.id] = {
                "name": test.name,
                "status": test.status.value,
                "winner": test.winner_variant_id,
                "confidence": test.confidence_level
            }
        
        return report
    
    def export_data(self) -> Dict:
        """Export all data for backup or migration"""
        return {
            "posts": {pid: asdict(post) for pid, post in self.posts.items()},
            "ab_tests": {tid: asdict(test) for tid, test in self.ab_tests.items()},
            "analytics": self.analytics_data,
            "export_timestamp": datetime.now().isoformat()
        }
    
    def import_data(self, data: Dict):
        """Import data from backup"""
        # Clear existing data
        self.posts.clear()
        self.ab_tests.clear()
        self.analytics_data.clear()
        
        # Import posts
        for post_data in data.get("posts", {}).values():
            post = SocialMediaPost(**post_data)
            self.posts[post.id] = post
        
        # Import A/B tests
        for test_data in data.get("ab_tests", {}).values():
            ab_test = ABTest(**test_data)
            self.ab_tests[ab_test.id] = ab_test
        
        # Import analytics
        self.analytics_data = data.get("analytics", {})
        
        logging.info("Data import completed successfully")

# Example usage and test functions
def create_sample_automation():
    """Create a sample automation setup for demonstration"""
    automation = SocialMediaAutomation()
    
    # Create a simple post
    post_id = automation.create_post(
        title="Newsletter Announcement",
        content="Check out our latest newsletter with insights on digital marketing trends! 🚀",
        platforms=[Platform.TWITTER, Platform.LINKEDIN, Platform.FACEBOOK],
        scheduled_time=datetime.now() + timedelta(hours=1),
        newsletter_link="https://newsletter.example.com/latest",
        hashtags=["marketing", "newsletter", "digitalmarketing"]
    )
    
    # Create an A/B test
    variants = [
        {
            "name": "Emoji Version",
            "content": "🚀 Discover the latest digital marketing trends in our new newsletter! Don't miss out on expert insights. 📊",
            "platforms": [Platform.TWITTER, Platform.FACEBOOK],
            "hashtags": ["marketing", "trends", "newsletter"]
        },
        {
            "name": "Professional Version", 
            "content": "Our latest newsletter features comprehensive analysis of digital marketing trends and expert insights.",
            "platforms": [Platform.TWITTER, Platform.FACEBOOK],
            "hashtags": ["marketing", "analysis", "newsletter"]
        }
    ]
    
    test_id = automation.create_ab_test(
        name="Newsletter Promotion Test",
        description="Testing emoji vs professional tone for newsletter promotion",
        variants=variants,
        start_time=datetime.now() + timedelta(hours=2),
        end_time=datetime.now() + timedelta(days=3)
    )
    
    return automation, post_id, test_id

if __name__ == "__main__":
    # Demo the automation system
    automation, post_id, test_id = create_sample_automation()
    
    print(f"Created post: {post_id}")
    print(f"Created A/B test: {test_id}")
    
    # Simulate some analytics data
    automation.update_analytics(post_id, Platform.TWITTER, {
        "impressions": 1500,
        "clicks": 45,
        "shares": 12,
        "likes": 89
    })
    
    # Generate report
    report = automation.get_analytics_report(
        start_date=datetime.now() - timedelta(days=7),
        end_date=datetime.now()
    )
    
    print("\nAnalytics Report:")
    print(json.dumps(report, default=str, indent=2))