#!/usr/bin/env python3
"""
Reddit User Persona Generator

This script scrapes a Reddit user's profile and generates a comprehensive user persona
based on their posts and comments, with citations for each characteristic.

Requirements:
- requests
- beautifulsoup4
- textstat (for readability analysis)
- collections
- datetime
- re

Usage:
python reddit_persona.py https://www.reddit.com/user/username/
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import os
import sys
from urllib.parse import urljoin, urlparse
import textstat

class RedditPersonaGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Common indicators for persona analysis
        self.age_indicators = {
            'young': ['college', 'school', 'student', 'homework', 'class', 'dorm', 'freshman', 'sophomore', 'junior', 'senior'],
            'middle': ['work', 'job', 'career', 'mortgage', 'kids', 'children', 'family', 'spouse', 'marriage'],
            'older': ['retirement', 'grandkids', 'pension', 'medicare', 'social security', 'arthritis', 'back pain']
        }
        
        self.gender_indicators = {
            'male': ['girlfriend', 'wife', 'my girl', 'she said', 'boyfriend', 'gay', 'straight guy'],
            'female': ['boyfriend', 'husband', 'my guy', 'he said', 'girlfriend', 'lesbian', 'straight girl']
        }
        
        self.location_patterns = [
            r'\b(in|from|live in|living in|moved to|visiting)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            r'\b([A-Z][a-z]+,\s*[A-Z]{2})\b',  # City, State
            r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b'  # Two word places
        ]
    
    def extract_username_from_url(self, url):
        """Extract username from Reddit profile URL"""
        match = re.search(r'/user/([^/]+)', url)
        if match:
            return match.group(1)
        return None
    
    def get_account_info(self, username):
        """Get basic account information from Reddit"""
        try:
            url = f"https://www.reddit.com/user/{username}/about/.json"
            response = self.session.get(url)
            time.sleep(0.5)
            
            if response.status_code == 200:
                data = response.json()
                user_data = data.get('data', {})
                
                return {
                    'created_utc': user_data.get('created_utc', 0),
                    'link_karma': user_data.get('link_karma', 0),
                    'comment_karma': user_data.get('comment_karma', 0),
                    'total_karma': user_data.get('total_karma', 0),
                    'is_gold': user_data.get('is_gold', False),
                    'is_mod': user_data.get('is_mod', False),
                    'verified': user_data.get('verified', False)
                }
        except Exception as e:
            print(f"Error getting account info: {e}")
        
        return {}
    
    def scrape_user_content(self, username, limit=1000):
        """Scrape user's posts and comments from Reddit with pagination"""
        print(f"Scraping content for user: {username}")
        
        posts = []
        comments = []
        
        # Scrape posts with pagination
        posts = self._scrape_with_pagination(username, 'submitted', limit)
        print(f"Scraped {len(posts)} posts")
        
        # Scrape comments with pagination
        comments = self._scrape_with_pagination(username, 'comments', limit)
        print(f"Scraped {len(comments)} comments")
        
        return posts, comments
    
    def _scrape_with_pagination(self, username, content_type, limit):
        """Scrape content with pagination support"""
        items = []
        after = None
        items_per_request = 100  # Reddit's max per request
        
        while len(items) < limit:
            try:
                url = f"https://www.reddit.com/user/{username}/{content_type}/.json?limit={items_per_request}"
                if after:
                    url += f"&after={after}"
                
                response = self.session.get(url)
                time.sleep(0.5)  # Reduced rate limiting
                
                if response.status_code != 200:
                    print(f"Error: HTTP {response.status_code} for {content_type}")
                    break
                
                data = response.json()
                children = data.get('data', {}).get('children', [])
                
                if not children:
                    print(f"No more {content_type} found")
                    break
                
                for item in children:
                    item_data = item.get('data', {})
                    
                    if content_type == 'submitted':
                        items.append({
                            'type': 'post',
                            'title': item_data.get('title', ''),
                            'content': item_data.get('selftext', ''),
                            'subreddit': item_data.get('subreddit', ''),
                            'score': item_data.get('score', 0),
                            'created_utc': item_data.get('created_utc', 0),
                            'url': f"https://reddit.com{item_data.get('permalink', '')}"
                        })
                    else:  # comments
                        items.append({
                            'type': 'comment',
                            'content': item_data.get('body', ''),
                            'subreddit': item_data.get('subreddit', ''),
                            'score': item_data.get('score', 0),
                            'created_utc': item_data.get('created_utc', 0),
                            'url': f"https://reddit.com{item_data.get('permalink', '')}"
                        })
                
                # Get the 'after' token for pagination
                after = data.get('data', {}).get('after')
                if not after:
                    print(f"Reached end of {content_type}")
                    break
                
                print(f"Scraped {len(items)} {content_type} so far...")
                
            except Exception as e:
                print(f"Error scraping {content_type}: {e}")
                break
        
        return items[:limit]
    
    def analyze_activity_patterns(self, posts, comments, account_info=None):
        """Analyze user's activity patterns"""
        all_content = posts + comments
        
        if not all_content:
            return {}
        
        # Time analysis - use account creation time if available
        if account_info and account_info.get('created_utc'):
            account_created = account_info['created_utc']
            current_time = time.time()
            account_age_days = (current_time - account_created) / (24 * 3600)
            account_age_years = account_age_days / 365.25
        else:
            # Fallback to oldest post/comment
            timestamps = [item['created_utc'] for item in all_content if item['created_utc']]
            if timestamps:
                earliest = min(timestamps)
                current_time = time.time()
                account_age_days = (current_time - earliest) / (24 * 3600)
                account_age_years = account_age_days / 365.25
            else:
                account_age_days = 0
                account_age_years = 0
        
        # Activity by hour (assuming UTC)
        timestamps = [item['created_utc'] for item in all_content if item['created_utc']]
        if timestamps:
            hours = [datetime.utcfromtimestamp(ts).hour for ts in timestamps]
            peak_hours = Counter(hours).most_common(3)
        else:
            peak_hours = []
        
        # Subreddit analysis
        subreddits = [item['subreddit'] for item in all_content if item['subreddit']]
        top_subreddits = Counter(subreddits).most_common(10)
        
        # Engagement analysis
        total_posts = len(posts)
        total_comments = len(comments)
        avg_post_score = sum(p['score'] for p in posts) / len(posts) if posts else 0
        avg_comment_score = sum(c['score'] for c in comments) / len(comments) if comments else 0
        
        return {
            'account_age_days': account_age_days,
            'account_age_years': account_age_years,
            'peak_hours': peak_hours,
            'top_subreddits': top_subreddits,
            'total_posts': total_posts,
            'total_comments': total_comments,
            'avg_post_score': avg_post_score,
            'avg_comment_score': avg_comment_score,
            'post_to_comment_ratio': total_posts / (total_comments + 1)
        }
    
    def extract_demographics(self, posts, comments):
        """Extract demographic information from content"""
        all_text = []
        citations = defaultdict(list)
        
        for item in posts + comments:
            text = (item.get('title', '') + ' ' + item.get('content', '')).lower()
            all_text.append(text)
            
            # Age indicators
            for age_group, indicators in self.age_indicators.items():
                for indicator in indicators:
                    if indicator in text:
                        citations[f'age_{age_group}'].append({
                            'text': text[:200] + '...' if len(text) > 200 else text,
                            'url': item.get('url', ''),
                            'indicator': indicator
                        })
            
            # Gender indicators
            for gender, indicators in self.gender_indicators.items():
                for indicator in indicators:
                    if indicator in text:
                        citations[f'gender_{gender}'].append({
                            'text': text[:200] + '...' if len(text) > 200 else text,
                            'url': item.get('url', ''),
                            'indicator': indicator
                        })
            
            # Location indicators
            for pattern in self.location_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    location = match if isinstance(match, str) else match[1]
                    citations['location'].append({
                        'text': text[:200] + '...' if len(text) > 200 else text,
                        'url': item.get('url', ''),
                        'location': location
                    })
        
        return citations
    
    def analyze_interests_and_personality(self, posts, comments):
        """Analyze interests and personality traits"""
        all_text = ' '.join([
            (item.get('title', '') + ' ' + item.get('content', ''))
            for item in posts + comments
        ]).lower()
        
        citations = defaultdict(list)
        
        # Interest categories
        interest_keywords = {
            'gaming': ['game', 'gaming', 'steam', 'console', 'pc', 'xbox', 'playstation', 'nintendo'],
            'tech': ['programming', 'code', 'software', 'computer', 'tech', 'developer', 'python', 'javascript'],
            'fitness': ['gym', 'workout', 'exercise', 'fitness', 'running', 'lifting', 'diet', 'protein'],
            'food': ['cooking', 'recipe', 'food', 'restaurant', 'chef', 'kitchen', 'meal', 'dinner'],
            'travel': ['travel', 'trip', 'vacation', 'flight', 'hotel', 'country', 'city', 'tourist'],
            'entertainment': ['movie', 'film', 'tv', 'show', 'netflix', 'actor', 'music', 'band'],
            'education': ['university', 'college', 'degree', 'professor', 'study', 'exam', 'homework'],
            'finance': ['money', 'investment', 'stock', 'crypto', 'bitcoin', 'salary', 'budget', 'savings']
        }
        
        interests = {}
        for category, keywords in interest_keywords.items():
            count = sum(all_text.count(keyword) for keyword in keywords)
            if count > 0:
                interests[category] = count
                
                # Find citations
                for item in posts + comments:
                    text = (item.get('title', '') + ' ' + item.get('content', '')).lower()
                    for keyword in keywords:
                        if keyword in text:
                            citations[f'interest_{category}'].append({
                                'text': text[:200] + '...' if len(text) > 200 else text,
                                'url': item.get('url', ''),
                                'keyword': keyword
                            })
                            break
        
        # Personality traits (basic sentiment analysis)
        personality_indicators = {
            'helpful': ['help', 'advice', 'recommend', 'suggest', 'guide', 'explain'],
            'humorous': ['lol', 'haha', 'funny', 'joke', 'hilarious', 'lmao'],
            'analytical': ['analyze', 'data', 'statistics', 'research', 'study', 'evidence'],
            'creative': ['art', 'design', 'creative', 'original', 'innovative', 'artistic'],
            'social': ['friend', 'community', 'social', 'group', 'together', 'meetup']
        }
        
        personality = {}
        for trait, indicators in personality_indicators.items():
            count = sum(all_text.count(indicator) for indicator in indicators)
            if count > 0:
                personality[trait] = count
        
        return interests, personality, citations
    
    def generate_persona(self, username, posts, comments, account_info=None):
        """Generate comprehensive user persona"""
        print("Generating user persona...")
        
        # Analyze different aspects
        activity = self.analyze_activity_patterns(posts, comments, account_info)
        demographics = self.extract_demographics(posts, comments)
        interests, personality, interest_citations = self.analyze_interests_and_personality(posts, comments)
        
        # Combine all citations
        all_citations = {**demographics, **interest_citations}
        
        # Generate persona
        persona = {
            'username': username,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'profile_url': f'https://www.reddit.com/user/{username}/',
            
            'basic_info': {
                'account_age_days': activity.get('account_age_days', 0),
                'account_age_years': activity.get('account_age_years', 0),
                'total_posts': activity.get('total_posts', 0),
                'total_comments': activity.get('total_comments', 0),
                'engagement_style': 'Commenter' if activity.get('post_to_comment_ratio', 0) < 0.5 else 'Poster'
            },
            
            'activity_patterns': {
                'peak_hours': activity.get('peak_hours', []),
                'top_subreddits': activity.get('top_subreddits', []),
                'avg_post_score': activity.get('avg_post_score', 0),
                'avg_comment_score': activity.get('avg_comment_score', 0)
            },
            
            'demographics': self._infer_demographics(demographics),
            'interests': dict(sorted(interests.items(), key=lambda x: x[1], reverse=True)),
            'personality_traits': dict(sorted(personality.items(), key=lambda x: x[1], reverse=True)),
            'citations': all_citations
        }
        
        return persona
    
    def _infer_demographics(self, demographics):
        """Infer demographics from citations"""
        inferred = {}
        
        # Age inference
        age_scores = {}
        for age_group in ['young', 'middle', 'older']:
            age_scores[age_group] = len(demographics.get(f'age_{age_group}', []))
        
        if age_scores:
            likely_age = max(age_scores, key=age_scores.get)
            if age_scores[likely_age] > 0:
                inferred['likely_age_group'] = likely_age
        
        # Gender inference
        gender_scores = {}
        for gender in ['male', 'female']:
            gender_scores[gender] = len(demographics.get(f'gender_{gender}', []))
        
        if gender_scores:
            likely_gender = max(gender_scores, key=gender_scores.get)
            if gender_scores[likely_gender] > 0:
                inferred['likely_gender'] = likely_gender
        
        # Location inference
        locations = demographics.get('location', [])
        if locations:
            location_counts = Counter([loc['location'] for loc in locations])
            inferred['possible_locations'] = location_counts.most_common(5)
        
        return inferred
    
    def save_persona_to_file(self, persona, filename=None):
        """Save persona to text file with citations"""
        if filename is None:
            filename = f"{persona['username']}_persona.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"REDDIT USER PERSONA REPORT\n")
            f.write(f"{'='*50}\n\n")
            
            f.write(f"Username: {persona['username']}\n")
            f.write(f"Profile URL: {persona['profile_url']}\n")
            f.write(f"Generated: {persona['generated_at']}\n\n")
            
            # Basic Information
            f.write("BASIC INFORMATION\n")
            f.write("-" * 20 + "\n")
            basic = persona['basic_info']
            f.write(f"Account Age: {basic['account_age_years']:.1f} years ({basic['account_age_days']:.0f} days)\n")
            f.write(f"Total Posts: {basic['total_posts']}\n")
            f.write(f"Total Comments: {basic['total_comments']}\n")
            f.write(f"Engagement Style: {basic['engagement_style']}\n\n")
            
            # Activity Patterns
            f.write("ACTIVITY PATTERNS\n")
            f.write("-" * 20 + "\n")
            activity = persona['activity_patterns']
            f.write(f"Peak Activity Hours: {', '.join([f'{h[0]}:00 ({h[1]} posts)' for h in activity['peak_hours'][:3]])}\n")
            f.write(f"Top Subreddits: {', '.join([f'{s[0]} ({s[1]})' for s in activity['top_subreddits'][:5]])}\n")
            f.write(f"Average Post Score: {activity['avg_post_score']:.1f}\n")
            f.write(f"Average Comment Score: {activity['avg_comment_score']:.1f}\n\n")
            
            # Demographics
            f.write("DEMOGRAPHICS\n")
            f.write("-" * 20 + "\n")
            demographics = persona['demographics']
            
            if 'likely_age_group' in demographics:
                f.write(f"Likely Age Group: {demographics['likely_age_group'].title()}\n")
                self._write_citations(f, persona['citations'], f"age_{demographics['likely_age_group']}")
            
            if 'likely_gender' in demographics:
                f.write(f"Likely Gender: {demographics['likely_gender'].title()}\n")
                self._write_citations(f, persona['citations'], f"gender_{demographics['likely_gender']}")
            
            if 'possible_locations' in demographics:
                f.write(f"Possible Locations: {', '.join([f'{loc[0]} ({loc[1]})' for loc in demographics['possible_locations'][:3]])}\n")
                self._write_citations(f, persona['citations'], 'location')
            
            f.write("\n")
            
            # Interests
            f.write("INTERESTS\n")
            f.write("-" * 20 + "\n")
            for interest, score in list(persona['interests'].items())[:5]:
                f.write(f"{interest.title()}: {score} mentions\n")
                self._write_citations(f, persona['citations'], f'interest_{interest}')
            f.write("\n")
            
            # Personality Traits
            f.write("PERSONALITY TRAITS\n")
            f.write("-" * 20 + "\n")
            for trait, score in list(persona['personality_traits'].items())[:5]:
                f.write(f"{trait.title()}: {score} indicators\n")
            f.write("\n")
    
    def _write_citations(self, file, all_citations, category):
        """Write citations for a specific category"""
        citations = all_citations.get(category, [])
        if citations:
            file.write("  Citations:\n")
            for i, citation in enumerate(citations[:3], 1):  # Limit to 3 citations
                file.write(f"    {i}. \"{citation['text']}\"\n")
                file.write(f"       Source: {citation['url']}\n")
            if len(citations) > 3:
                file.write(f"    ... and {len(citations) - 3} more\n")
            file.write("\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python reddit_persona.py <reddit_profile_url>")
        print("Example: python reddit_persona.py https://www.reddit.com/user/kojied/")
        sys.exit(1)
    
    profile_url = sys.argv[1]
    
    # Initialize generator
    generator = RedditPersonaGenerator()
    
    # Extract username
    username = generator.extract_username_from_url(profile_url)
    if not username:
        print("Error: Could not extract username from URL")
        sys.exit(1)
    
    print(f"Processing Reddit user: {username}")
    
    # Get account information
    account_info = generator.get_account_info(username)
    if account_info:
        print(f"Account created: {datetime.utcfromtimestamp(account_info.get('created_utc', 0)).strftime('%Y-%m-%d')}")
        print(f"Total karma: {account_info.get('total_karma', 0)}")
    
    # Scrape content with higher limit and better pagination
    posts, comments = generator.scrape_user_content(username, limit=2000)
    
    if not posts and not comments:
        print("Error: No content found for this user")
        sys.exit(1)
    
    print(f"Found {len(posts)} posts and {len(comments)} comments")
    
    # Generate persona
    persona = generator.generate_persona(username, posts, comments, account_info)
    
    # Save to file
    filename = f"{username}_persona.txt"
    generator.save_persona_to_file(persona, filename)
    
    print(f"Persona saved to: {filename}")

if __name__ == "__main__":
    main()