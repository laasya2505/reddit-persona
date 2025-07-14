# Reddit User Persona Generator

A Python script that analyzes Reddit user profiles and generates comprehensive user personas based on their posts, comments, and activity patterns. The tool provides detailed insights into user demographics, interests, personality traits, and behavior patterns with proper citations for each finding.

## 🎯 Project Overview

This tool scrapes a Reddit user's public profile and creates a detailed persona report that includes:

- **Basic Information**: Account age, post/comment counts, engagement style
- **Activity Patterns**: Peak activity hours, favorite subreddits, engagement metrics
- **Demographics**: Age group, gender, and location inference
- **Interests**: Gaming, tech, fitness, food, travel, entertainment, education, finance
- **Personality Traits**: Helpful, humorous, analytical, creative, social indicators
- **Citations**: Direct quotes and sources for every characteristic identified

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Output Format](#output-format)
- [Technical Details](#technical-details)
- [Limitations](#limitations)
- [Privacy and Ethics](#privacy-and-ethics)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- Internet connection for Reddit API access

### Step 1: Clone or Download

```bash
git clone <your-repository-url>
cd reddit-persona
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests beautifulsoup4 textstat
```

### Step 3: Verify Installation

```bash
python reddit_persona.py --help
```

## 💻 Usage

### Basic Usage

```bash
python reddit_persona.py <reddit_profile_url>
```

### Examples

```bash
# Example 1: Generate persona for user 'kojied'
python reddit_persona.py https://www.reddit.com/user/kojied/

# Example 2: Generate persona for user 'amyaurora'
python reddit_persona.py https://www.reddit.com/user/amyaurora/
```

### Expected Output

The script will:
1. Extract username from the provided URL
2. Fetch account information (creation date, karma, etc.)
3. Scrape up to 2000 posts and comments with pagination
4. Analyze content for patterns and characteristics
5. Generate a comprehensive persona report
6. Save results to `{username}_persona.txt`

## ✨ Features

### Data Collection
- **Comprehensive Scraping**: Collects up to 2000 posts and comments
- **Pagination Support**: Handles Reddit's API pagination automatically
- **Account Information**: Fetches official account metadata
- **Rate Limiting**: Respects Reddit's servers with appropriate delays

### Analysis Capabilities
- **Demographic Inference**: Age group, gender, and location analysis
- **Interest Detection**: 8 major interest categories with keyword matching
- **Personality Analysis**: 5 personality traits based on language patterns
- **Activity Patterns**: Peak hours, favorite subreddits, engagement metrics
- **Citation System**: Every finding backed by actual posts/comments

### Output Features
- **Structured Reports**: Well-organized text files with clear sections
- **Citation Tracking**: Direct quotes and URLs for verification
- **Quantitative Metrics**: Numerical scores for interests and traits
- **Time Analysis**: Account age in both years and days

## 📊 Output Format

The generated persona report includes the following sections:

### 1. Basic Information
```
Account Age: 12.3 years (4,502 days)
Total Posts: 494
Total Comments: 11,847
Engagement Style: Commenter
```

### 2. Activity Patterns
```
Peak Activity Hours: 15:00 (22 posts), 17:00 (21 posts)
Top Subreddits: witchcraft (250), elderwitches (125)
Average Post Score: 82.9
Average Comment Score: 3.8
```

### 3. Demographics
```
Likely Age Group: Middle
Likely Gender: Female
Possible Locations: Portland (15), Seattle (8)
```

### 4. Interests (Ranked by Frequency)
```
Gaming: 45 mentions
Tech: 32 mentions
Finance: 28 mentions
```

### 5. Personality Traits
```
Helpful: 44 indicators
Creative: 38 indicators
Analytical: 10 indicators
```

### 6. Citations
Each characteristic includes supporting evidence:
```
Citations:
  1. "I work in tech and love programming in Python..."
     Source: https://reddit.com/r/programming/comments/xyz123/
  2. "My gaming setup includes a custom PC..."
     Source: https://reddit.com/r/gaming/comments/abc456/
```

## 🔧 Technical Details

### API Endpoints Used
- `https://www.reddit.com/user/{username}/about/.json` - Account information
- `https://www.reddit.com/user/{username}/submitted/.json` - User posts
- `https://www.reddit.com/user/{username}/comments/.json` - User comments

### Analysis Methods

#### Demographic Inference
- **Age Groups**: Uses keyword matching for life stage indicators
  - Young: college, student, homework, dorm
  - Middle: work, career, mortgage, kids, marriage
  - Older: retirement, grandkids, medicare
- **Gender**: Analyzes relationship references and pronouns
- **Location**: Regex patterns for geographical mentions

#### Interest Categories
- **Gaming**: game, gaming, steam, console, pc, xbox, playstation
- **Tech**: programming, code, software, developer, python
- **Fitness**: gym, workout, exercise, running, lifting
- **Food**: cooking, recipe, restaurant, chef, kitchen
- **Travel**: travel, trip, vacation, flight, hotel
- **Entertainment**: movie, tv, netflix, music, band
- **Education**: university, college, degree, study
- **Finance**: money, investment, stock, crypto, bitcoin

#### Personality Traits
- **Helpful**: help, advice, recommend, suggest, guide
- **Humorous**: lol, funny, joke, hilarious
- **Analytical**: analyze, data, statistics, research
- **Creative**: art, design, creative, original
- **Social**: friend, community, social, group

### Data Processing
- **Text Preprocessing**: Case normalization, content cleaning
- **Pattern Matching**: Regex and keyword-based analysis
- **Frequency Analysis**: Counting mentions and occurrences
- **Citation Tracking**: Maintaining source references

## ⚠️ Limitations

### Technical Limitations

#### 1. Data Access Constraints
- **Public Content Only**: Can only analyze publicly visible posts and comments
- **API Rate Limits**: Reddit's API has built-in rate limiting
- **Content Limits**: Maximum 2000 posts/comments per scraping session
- **No Real-time Data**: Analysis based on historical content only

#### 2. Scraping Limitations
- **Deleted Content**: Cannot access deleted or removed posts
- **Private Profiles**: Cannot analyze private or suspended accounts
- **Shadowbanned Content**: May miss shadowbanned posts
- **API Changes**: Reddit API changes may affect functionality

#### 3. Analysis Accuracy
- **Inference-Based**: Demographics are inferred, not factual
- **Context Limitations**: May miss sarcasm, irony, or context
- **Keyword Dependency**: Analysis relies on keyword matching
- **Bias Potential**: May reflect algorithmic biases in keyword selection

### Analytical Limitations

#### 1. Demographic Inference
- **Age Groups**: Broad categories, not specific ages
- **Gender**: Binary classification, may miss non-binary identities
- **Location**: Based on mentions, not current residence
- **Accuracy**: No ground truth validation available

#### 2. Interest Detection
- **Surface-Level**: Based on keyword frequency, not depth
- **Context-Agnostic**: May misclassify ironic or quoted content
- **Limited Categories**: Only 8 predefined interest areas
- **Threshold Issues**: May miss interests with low mention frequency

#### 3. Personality Analysis
- **Simplified Model**: Basic trait detection, not comprehensive
- **Language-Dependent**: Works best with English content
- **Temporal Bias**: May reflect recent activity more than historical
- **No Validation**: Not validated against psychological assessments

### Data Quality Issues

#### 1. Sampling Bias
- **Recency Bias**: Recent posts may be overrepresented
- **Subreddit Bias**: Analysis skewed toward active subreddits
- **Volume Bias**: Heavy posters may appear more prominent
- **Temporal Bias**: Analysis reflects posting period, not lifetime

#### 2. Content Quality
- **Spam Detection**: No filtering for spam or bot content
- **Multiple Accounts**: Cannot detect if user has multiple accounts
- **Shared Accounts**: Cannot identify shared account usage
- **Content Authenticity**: No verification of content truthfulness

#### 3. Classification Errors
- **False Positives**: May incorrectly identify characteristics
- **False Negatives**: May miss actual characteristics
- **Ambiguous Content**: Difficulty with ambiguous or unclear posts
- **Contextual Misunderstanding**: May misinterpret context-dependent content

## 🔒 Privacy and Ethics

### Privacy Considerations
- **Public Data Only**: Only analyzes publicly available content
- **No Personal Information**: Does not collect email, IP, or private data
- **User Consent**: Operates on assumption of public posting consent
- **Data Retention**: Does not store user data beyond analysis session

### Ethical Usage
- **Research Purpose**: Intended for academic and research use
- **No Harassment**: Should not be used to harass or target users
- **Respect Privacy**: Respect user privacy even with public data
- **Responsible Disclosure**: Use findings responsibly and ethically

### Legal Compliance
- **Terms of Service**: Complies with Reddit's Terms of Service
- **Fair Use**: Analysis falls under fair use for research purposes
- **No Commercial Use**: Not intended for commercial profiling
- **Data Protection**: Follows general data protection principles

## 🛠️ Troubleshooting

### Common Issues

#### 1. Installation Problems
```bash
# If pip install fails
pip install --upgrade pip
pip install -r requirements.txt

# For permission issues
pip install --user -r requirements.txt
```

#### 2. Network Errors
- **Solution**: Check internet connection
- **Rate Limiting**: Wait a few minutes if getting 429 errors
- **Firewall**: Ensure Reddit is not blocked by firewall

#### 3. No Content Found
- **Private Profile**: User may have private profile
- **Deleted Account**: Account may be deleted or suspended
- **New Account**: Very new accounts may have minimal content

#### 4. Incorrect Analysis
- **Limited Data**: More posts/comments generally improve accuracy
- **Language Issues**: Works best with English content
- **Context**: Results are inference-based, not factual

### Error Messages

#### `AttributeError: 'RedditPersonaGenerator' object has no attribute 'extract_username_from_url'`
- **Cause**: Missing method definition
- **Solution**: Ensure you're using the latest version of the script

#### `HTTP 429 Too Many Requests`
- **Cause**: Rate limiting by Reddit
- **Solution**: Wait and retry, or reduce scraping frequency

#### `No content found for this user`
- **Cause**: User has no public posts/comments or account issues
- **Solution**: Try a different user or check account status

## 📈 Performance Expectations

### Execution Time
- **Small Profiles** (< 100 posts): 30-60 seconds
- **Medium Profiles** (100-1000 posts): 2-5 minutes
- **Large Profiles** (1000+ posts): 5-15 minutes

### Resource Usage
- **Memory**: 50-200 MB depending on content volume
- **Network**: 1-10 MB data transfer
- **CPU**: Moderate during text analysis phase

### Accuracy Expectations
- **High Confidence**: Activity patterns, subreddit preferences
- **Medium Confidence**: Interest categories, personality traits
- **Low Confidence**: Demographics, location inference

## 🤝 Contributing

### Bug Reports
- Use GitHub Issues for bug reports
- Include full error messages and stack traces
- Provide example usernames (if public) that cause issues

### Feature Requests
- Suggest new analysis categories
- Propose accuracy improvements
- Request additional output formats

### Code Contributions
- Follow PEP 8 style guidelines
- Add unit tests for new features
- Update documentation for changes

## 📄 License

This project is intended for educational and research purposes. Please use responsibly and in accordance with Reddit's Terms of Service.

## 🙏 Acknowledgments

- Reddit for providing public API access
- Open source Python libraries used in this project
- The research community for persona analysis methodologies
