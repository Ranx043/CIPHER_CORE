# 💬 NEURONA: SENTIMENT ANALYSIS
## CIPHER_CORE :: Social & News Intelligence

> **Código Neuronal**: `C50004`
> **Dominio**: Social Media, News Analysis, Fear & Greed
> **Estado**: `ACTIVA`
> **Última Evolución**: 2025-01-XX

---

## 🧬 IDENTIDAD DE LA NEURONA

```
╔══════════════════════════════════════════════════════════════╗
║  CIPHER SENTIMENT - The Pulse of the Market                  ║
║  "Markets are driven by fear and greed - measure both"       ║
╠══════════════════════════════════════════════════════════════╣
║  Especialización: Social signals, news analysis, sentiment   ║
║  Conexiones: ML Trading, Market Data, On-Chain Analytics     ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 📱 SOCIAL MEDIA ANALYSIS

### Twitter/X Sentiment Analyzer

```python
"""
CIPHER Social Media Sentiment Analysis
Real-time sentiment from Twitter, Reddit, Discord, Telegram
"""

import asyncio
import aiohttp
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import re
import numpy as np
from textblob import TextBlob
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch

@dataclass
class SocialPost:
    """Social media post/tweet"""
    id: str
    platform: str
    timestamp: datetime
    author: str
    author_followers: int
    content: str
    likes: int
    reposts: int
    replies: int
    mentions: List[str]
    hashtags: List[str]
    cashtags: List[str]  # $BTC, $ETH, etc.
    urls: List[str]
    sentiment_score: float = 0.0
    engagement_score: float = 0.0

@dataclass
class SentimentResult:
    """Aggregated sentiment result"""
    symbol: str
    timestamp: datetime
    sentiment_score: float  # -1 to 1
    sentiment_label: str  # 'bullish', 'bearish', 'neutral'
    volume: int  # Number of posts
    engagement: float  # Total engagement
    influential_posts: List[SocialPost]
    top_keywords: List[Tuple[str, int]]
    trend: str  # 'increasing', 'decreasing', 'stable'

class CryptoSentimentAnalyzer:
    """
    Analyze crypto sentiment from social media
    """

    def __init__(self, use_transformer: bool = True):
        self.use_transformer = use_transformer

        # Load FinBERT for financial sentiment
        if use_transformer:
            self.tokenizer = AutoTokenizer.from_pretrained(
                "ProsusAI/finbert"
            )
            self.model = AutoModelForSequenceClassification.from_pretrained(
                "ProsusAI/finbert"
            )
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer
            )

        # Crypto-specific lexicon
        self.bullish_words = {
            'moon', 'bullish', 'pump', 'buy', 'long', 'breakout',
            'accumulate', 'hodl', 'diamond hands', 'to the moon',
            'ath', 'all time high', 'dip', 'buy the dip', 'undervalued',
            'gem', 'alpha', 'bullrun', 'rally', 'green', 'gains',
            'rip', 'send it', 'wagmi', 'gm', 'lfg'
        }

        self.bearish_words = {
            'crash', 'bearish', 'dump', 'sell', 'short', 'breakdown',
            'distribute', 'paper hands', 'rug', 'scam', 'overvalued',
            'correction', 'bubble', 'top', 'red', 'loss', 'ngmi',
            'rekt', 'liquidated', 'capitulation', 'fear', 'fud',
            'dead', 'worthless', 'ponzi'
        }

        # Cashtag mappings
        self.cashtag_to_symbol = {
            '$btc': 'BTC', '$bitcoin': 'BTC',
            '$eth': 'ETH', '$ethereum': 'ETH',
            '$sol': 'SOL', '$solana': 'SOL',
            '$bnb': 'BNB', '$avax': 'AVAX',
            '$matic': 'MATIC', '$dot': 'DOT',
            '$atom': 'ATOM', '$link': 'LINK',
            '$uni': 'UNI', '$aave': 'AAVE',
        }

        self.post_history: Dict[str, List[SocialPost]] = defaultdict(list)

    def analyze_text(self, text: str) -> Dict:
        """Analyze sentiment of a single text"""

        # Clean text
        clean_text = self._clean_text(text)

        # Multiple analysis methods
        results = {}

        # 1. Transformer-based (FinBERT)
        if self.use_transformer:
            try:
                transformer_result = self.sentiment_pipeline(clean_text[:512])[0]
                label_map = {'positive': 1, 'negative': -1, 'neutral': 0}
                results['transformer_score'] = label_map.get(transformer_result['label'], 0)
                results['transformer_confidence'] = transformer_result['score']
            except Exception:
                results['transformer_score'] = 0
                results['transformer_confidence'] = 0

        # 2. TextBlob sentiment
        blob = TextBlob(clean_text)
        results['textblob_polarity'] = blob.sentiment.polarity
        results['textblob_subjectivity'] = blob.sentiment.subjectivity

        # 3. Crypto-specific lexicon
        text_lower = text.lower()
        bullish_count = sum(1 for word in self.bullish_words if word in text_lower)
        bearish_count = sum(1 for word in self.bearish_words if word in text_lower)

        if bullish_count + bearish_count > 0:
            results['lexicon_score'] = (bullish_count - bearish_count) / (bullish_count + bearish_count)
        else:
            results['lexicon_score'] = 0

        # Combined score (weighted average)
        weights = {'transformer': 0.5, 'textblob': 0.2, 'lexicon': 0.3}

        if self.use_transformer:
            combined = (
                results.get('transformer_score', 0) * weights['transformer'] +
                results['textblob_polarity'] * weights['textblob'] +
                results['lexicon_score'] * weights['lexicon']
            )
        else:
            combined = (
                results['textblob_polarity'] * 0.4 +
                results['lexicon_score'] * 0.6
            )

        results['combined_score'] = np.clip(combined, -1, 1)

        # Sentiment label
        if results['combined_score'] > 0.15:
            results['label'] = 'bullish'
        elif results['combined_score'] < -0.15:
            results['label'] = 'bearish'
        else:
            results['label'] = 'neutral'

        return results

    def _clean_text(self, text: str) -> str:
        """Clean social media text"""

        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)

        # Remove mentions (keep for analysis but remove for sentiment)
        text = re.sub(r'@\w+', '', text)

        # Keep cashtags for now
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def extract_entities(self, text: str) -> Dict:
        """Extract mentions, hashtags, cashtags"""

        mentions = re.findall(r'@(\w+)', text)
        hashtags = re.findall(r'#(\w+)', text.lower())
        cashtags = re.findall(r'\$([a-zA-Z]+)', text.lower())

        # Map cashtags to symbols
        symbols = []
        for tag in cashtags:
            full_tag = f'${tag}'
            if full_tag in self.cashtag_to_symbol:
                symbols.append(self.cashtag_to_symbol[full_tag])
            else:
                symbols.append(tag.upper())

        return {
            'mentions': mentions,
            'hashtags': hashtags,
            'cashtags': cashtags,
            'symbols': list(set(symbols))
        }

    def analyze_post(self, post: SocialPost) -> SocialPost:
        """Analyze a single social media post"""

        # Get sentiment
        sentiment = self.analyze_text(post.content)
        post.sentiment_score = sentiment['combined_score']

        # Calculate engagement score (normalized)
        post.engagement_score = np.log1p(
            post.likes +
            post.reposts * 2 +
            post.replies * 1.5
        )

        # Weight by follower count
        post.engagement_score *= np.log1p(post.author_followers) / 10

        # Store in history
        for symbol in post.cashtags:
            self.post_history[symbol.upper()].append(post)

        return post

    def get_aggregated_sentiment(
        self,
        symbol: str,
        hours: int = 24
    ) -> Optional[SentimentResult]:
        """Get aggregated sentiment for a symbol"""

        cutoff = datetime.utcnow() - timedelta(hours=hours)
        posts = [
            p for p in self.post_history.get(symbol.upper(), [])
            if p.timestamp > cutoff
        ]

        if not posts:
            return None

        # Weighted sentiment (by engagement)
        total_weight = sum(p.engagement_score for p in posts)
        if total_weight > 0:
            weighted_sentiment = sum(
                p.sentiment_score * p.engagement_score
                for p in posts
            ) / total_weight
        else:
            weighted_sentiment = np.mean([p.sentiment_score for p in posts])

        # Determine label
        if weighted_sentiment > 0.15:
            label = 'bullish'
        elif weighted_sentiment < -0.15:
            label = 'bearish'
        else:
            label = 'neutral'

        # Total engagement
        total_engagement = sum(
            p.likes + p.reposts + p.replies for p in posts
        )

        # Top influential posts
        influential = sorted(
            posts, key=lambda p: p.engagement_score, reverse=True
        )[:5]

        # Extract keywords
        all_text = ' '.join(p.content for p in posts)
        word_freq = defaultdict(int)
        for word in all_text.lower().split():
            if len(word) > 3 and word not in {'http', 'https', 'the', 'and', 'for'}:
                word_freq[word] += 1

        top_keywords = sorted(
            word_freq.items(), key=lambda x: x[1], reverse=True
        )[:10]

        # Trend analysis
        if len(posts) > 10:
            recent = posts[-len(posts)//3:]
            older = posts[:len(posts)//3]
            recent_sentiment = np.mean([p.sentiment_score for p in recent])
            older_sentiment = np.mean([p.sentiment_score for p in older])

            if recent_sentiment > older_sentiment + 0.1:
                trend = 'increasing'
            elif recent_sentiment < older_sentiment - 0.1:
                trend = 'decreasing'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'

        return SentimentResult(
            symbol=symbol.upper(),
            timestamp=datetime.utcnow(),
            sentiment_score=weighted_sentiment,
            sentiment_label=label,
            volume=len(posts),
            engagement=total_engagement,
            influential_posts=influential,
            top_keywords=top_keywords,
            trend=trend
        )


class RedditSentimentCollector:
    """
    Collect and analyze Reddit sentiment
    """

    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.access_token = None

        self.crypto_subreddits = [
            'cryptocurrency', 'bitcoin', 'ethereum', 'CryptoMarkets',
            'defi', 'altcoin', 'solana', 'cardano', 'Polkadot'
        ]

    async def get_access_token(self):
        """Get Reddit OAuth token"""

        async with aiohttp.ClientSession() as session:
            auth = aiohttp.BasicAuth(self.client_id, self.client_secret)
            data = {
                'grant_type': 'client_credentials'
            }
            headers = {'User-Agent': self.user_agent}

            async with session.post(
                'https://www.reddit.com/api/v1/access_token',
                auth=auth,
                data=data,
                headers=headers
            ) as resp:
                result = await resp.json()
                self.access_token = result['access_token']

    async def fetch_subreddit_posts(
        self,
        subreddit: str,
        limit: int = 100,
        timeframe: str = 'day'
    ) -> List[Dict]:
        """Fetch posts from a subreddit"""

        if not self.access_token:
            await self.get_access_token()

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'User-Agent': self.user_agent
        }

        posts = []

        async with aiohttp.ClientSession() as session:
            url = f'https://oauth.reddit.com/r/{subreddit}/top'
            params = {'limit': limit, 't': timeframe}

            async with session.get(url, headers=headers, params=params) as resp:
                data = await resp.json()

                for post_data in data.get('data', {}).get('children', []):
                    post = post_data['data']
                    posts.append({
                        'id': post['id'],
                        'title': post['title'],
                        'selftext': post.get('selftext', ''),
                        'score': post['score'],
                        'num_comments': post['num_comments'],
                        'created_utc': post['created_utc'],
                        'author': post['author'],
                        'subreddit': subreddit
                    })

        return posts

    async def analyze_subreddit(
        self,
        subreddit: str,
        analyzer: CryptoSentimentAnalyzer
    ) -> Dict:
        """Analyze sentiment of a subreddit"""

        posts = await self.fetch_subreddit_posts(subreddit)

        sentiments = []
        symbol_mentions = defaultdict(int)

        for post in posts:
            full_text = f"{post['title']} {post['selftext']}"

            # Analyze sentiment
            sentiment = analyzer.analyze_text(full_text)
            sentiments.append({
                'score': sentiment['combined_score'],
                'engagement': post['score'] + post['num_comments'],
                'post': post
            })

            # Extract symbols
            entities = analyzer.extract_entities(full_text)
            for symbol in entities['symbols']:
                symbol_mentions[symbol] += 1

        # Aggregate
        if sentiments:
            avg_sentiment = np.mean([s['score'] for s in sentiments])
            weighted_sentiment = sum(
                s['score'] * s['engagement'] for s in sentiments
            ) / sum(s['engagement'] for s in sentiments)
        else:
            avg_sentiment = 0
            weighted_sentiment = 0

        return {
            'subreddit': subreddit,
            'post_count': len(posts),
            'avg_sentiment': avg_sentiment,
            'weighted_sentiment': weighted_sentiment,
            'symbol_mentions': dict(symbol_mentions),
            'top_posts': sorted(sentiments, key=lambda x: x['engagement'], reverse=True)[:5]
        }
```

---

## 📰 NEWS ANALYSIS

### Crypto News Analyzer

```python
"""
CIPHER News Sentiment Analysis
Analyze crypto news for market signals
"""

import asyncio
import aiohttp
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import feedparser
from bs4 import BeautifulSoup
import re

@dataclass
class NewsArticle:
    """News article"""
    id: str
    source: str
    title: str
    content: str
    url: str
    published: datetime
    symbols: List[str]
    sentiment_score: float = 0.0
    importance: str = 'normal'  # 'breaking', 'important', 'normal'

class CryptoNewsCollector:
    """
    Collect news from multiple crypto news sources
    """

    def __init__(self):
        self.rss_feeds = {
            'cointelegraph': 'https://cointelegraph.com/rss',
            'coindesk': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
            'decrypt': 'https://decrypt.co/feed',
            'bitcoinmagazine': 'https://bitcoinmagazine.com/feed',
            'theblock': 'https://www.theblock.co/rss.xml',
        }

        self.breaking_keywords = [
            'breaking', 'just in', 'urgent', 'flash',
            'sec', 'regulation', 'hack', 'exploit',
            'bitcoin etf', 'approval', 'ban', 'lawsuit'
        ]

        self.important_keywords = [
            'fed', 'interest rate', 'cpi', 'inflation',
            'earnings', 'partnership', 'acquisition',
            'launch', 'update', 'upgrade', 'hard fork'
        ]

    async def fetch_rss_feed(
        self,
        source: str,
        url: str
    ) -> List[NewsArticle]:
        """Fetch articles from RSS feed"""

        articles = []

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    content = await resp.text()

            feed = feedparser.parse(content)

            for entry in feed.entries[:50]:  # Last 50 articles
                # Parse publish date
                if hasattr(entry, 'published_parsed'):
                    published = datetime(*entry.published_parsed[:6])
                else:
                    published = datetime.utcnow()

                # Extract content
                content = entry.get('summary', '')
                if hasattr(entry, 'content'):
                    content = entry.content[0].get('value', content)

                # Clean HTML
                content = BeautifulSoup(content, 'html.parser').get_text()

                # Determine importance
                title_lower = entry.title.lower()
                if any(kw in title_lower for kw in self.breaking_keywords):
                    importance = 'breaking'
                elif any(kw in title_lower for kw in self.important_keywords):
                    importance = 'important'
                else:
                    importance = 'normal'

                articles.append(NewsArticle(
                    id=entry.get('id', entry.link),
                    source=source,
                    title=entry.title,
                    content=content[:2000],  # Limit content length
                    url=entry.link,
                    published=published,
                    symbols=[],
                    importance=importance
                ))

        except Exception as e:
            print(f"Error fetching {source}: {e}")

        return articles

    async def fetch_all_feeds(self) -> List[NewsArticle]:
        """Fetch from all configured RSS feeds"""

        tasks = [
            self.fetch_rss_feed(source, url)
            for source, url in self.rss_feeds.items()
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_articles = []
        for result in results:
            if isinstance(result, list):
                all_articles.extend(result)

        # Sort by publish date
        all_articles.sort(key=lambda x: x.published, reverse=True)

        return all_articles


class NewsAnalyzer:
    """
    Analyze news articles for trading signals
    """

    def __init__(self, sentiment_analyzer: CryptoSentimentAnalyzer):
        self.sentiment_analyzer = sentiment_analyzer
        self.article_history: List[NewsArticle] = []

    def analyze_article(self, article: NewsArticle) -> NewsArticle:
        """Analyze a single news article"""

        # Combine title and content for analysis
        full_text = f"{article.title}. {article.content}"

        # Get sentiment
        sentiment = self.sentiment_analyzer.analyze_text(full_text)
        article.sentiment_score = sentiment['combined_score']

        # Extract symbols
        entities = self.sentiment_analyzer.extract_entities(full_text)
        article.symbols = entities['symbols']

        self.article_history.append(article)

        return article

    def get_news_sentiment(
        self,
        symbol: Optional[str] = None,
        hours: int = 24,
        importance: Optional[str] = None
    ) -> Dict:
        """Get aggregated news sentiment"""

        cutoff = datetime.utcnow() - timedelta(hours=hours)

        articles = [
            a for a in self.article_history
            if a.published > cutoff
        ]

        if symbol:
            articles = [a for a in articles if symbol.upper() in a.symbols]

        if importance:
            articles = [a for a in articles if a.importance == importance]

        if not articles:
            return {
                'sentiment': 0,
                'article_count': 0,
                'label': 'neutral'
            }

        # Weight by importance
        importance_weights = {'breaking': 3, 'important': 2, 'normal': 1}

        weighted_sum = sum(
            a.sentiment_score * importance_weights[a.importance]
            for a in articles
        )
        total_weight = sum(importance_weights[a.importance] for a in articles)

        avg_sentiment = weighted_sum / total_weight if total_weight > 0 else 0

        # Count by sentiment
        bullish = sum(1 for a in articles if a.sentiment_score > 0.15)
        bearish = sum(1 for a in articles if a.sentiment_score < -0.15)
        neutral = len(articles) - bullish - bearish

        # Determine overall label
        if avg_sentiment > 0.15:
            label = 'bullish'
        elif avg_sentiment < -0.15:
            label = 'bearish'
        else:
            label = 'neutral'

        return {
            'sentiment': avg_sentiment,
            'article_count': len(articles),
            'bullish_count': bullish,
            'bearish_count': bearish,
            'neutral_count': neutral,
            'label': label,
            'breaking_articles': [a for a in articles if a.importance == 'breaking'],
            'top_articles': sorted(articles, key=lambda x: abs(x.sentiment_score), reverse=True)[:5]
        }
```

---

## 📊 FEAR & GREED INDEX

### Crypto Fear & Greed Calculator

```python
"""
CIPHER Fear & Greed Index
Multi-factor sentiment indicator
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np

@dataclass
class FearGreedComponents:
    """Components of Fear & Greed Index"""
    volatility: float
    momentum: float
    social_sentiment: float
    dominance: float
    trends: float
    trading_volume: float

@dataclass
class FearGreedResult:
    """Fear & Greed Index result"""
    value: int  # 0-100
    label: str  # 'Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed'
    timestamp: datetime
    components: FearGreedComponents
    historical_comparison: str

class CryptoFearGreedIndex:
    """
    Calculate comprehensive Fear & Greed Index
    """

    def __init__(self):
        self.history: List[FearGreedResult] = []

        # Component weights
        self.weights = {
            'volatility': 0.15,
            'momentum': 0.25,
            'social_sentiment': 0.20,
            'dominance': 0.10,
            'trends': 0.15,
            'trading_volume': 0.15
        }

    def calculate(
        self,
        market_data: Dict,
        social_sentiment: float,
        news_sentiment: float
    ) -> FearGreedResult:
        """
        Calculate Fear & Greed Index

        Args:
            market_data: Dict with:
                - btc_price: current BTC price
                - btc_price_30d: BTC price 30 days ago
                - btc_volatility: 30-day volatility
                - btc_volatility_avg: average volatility
                - btc_dominance: BTC market dominance
                - btc_dominance_avg: average dominance
                - total_volume: 24h volume
                - avg_volume: average volume
            social_sentiment: -1 to 1
            news_sentiment: -1 to 1
        """

        components = self._calculate_components(
            market_data, social_sentiment, news_sentiment
        )

        # Weighted average
        weighted_sum = (
            components.volatility * self.weights['volatility'] +
            components.momentum * self.weights['momentum'] +
            components.social_sentiment * self.weights['social_sentiment'] +
            components.dominance * self.weights['dominance'] +
            components.trends * self.weights['trends'] +
            components.trading_volume * self.weights['trading_volume']
        )

        # Convert to 0-100 scale
        value = int(np.clip(weighted_sum, 0, 100))

        # Determine label
        label = self._get_label(value)

        # Historical comparison
        historical_comparison = self._compare_to_history(value)

        result = FearGreedResult(
            value=value,
            label=label,
            timestamp=datetime.utcnow(),
            components=components,
            historical_comparison=historical_comparison
        )

        self.history.append(result)

        return result

    def _calculate_components(
        self,
        market_data: Dict,
        social_sentiment: float,
        news_sentiment: float
    ) -> FearGreedComponents:
        """Calculate individual components"""

        # 1. Volatility (inverted - high volatility = fear)
        vol_ratio = market_data['btc_volatility'] / market_data['btc_volatility_avg']
        volatility_score = 100 - np.clip(vol_ratio * 50, 0, 100)

        # 2. Momentum (price performance)
        price_change = (market_data['btc_price'] - market_data['btc_price_30d']) / market_data['btc_price_30d']
        momentum_score = np.clip((price_change + 0.3) / 0.6 * 100, 0, 100)  # -30% to +30% mapped to 0-100

        # 3. Social Sentiment
        social_score = (social_sentiment + 1) / 2 * 100  # -1 to 1 mapped to 0-100

        # 4. Dominance (high BTC dominance = fear/safety)
        dom_change = market_data['btc_dominance'] - market_data['btc_dominance_avg']
        dominance_score = 50 - dom_change * 5  # Inverted - high dominance means fear

        # 5. Trends (combine news + search trends)
        trends_score = (news_sentiment + 1) / 2 * 100

        # 6. Trading Volume
        vol_ratio = market_data['total_volume'] / market_data['avg_volume']
        volume_score = np.clip(vol_ratio * 50, 0, 100)

        return FearGreedComponents(
            volatility=volatility_score,
            momentum=momentum_score,
            social_sentiment=social_score,
            dominance=dominance_score,
            trends=trends_score,
            trading_volume=volume_score
        )

    def _get_label(self, value: int) -> str:
        """Get label for Fear & Greed value"""

        if value <= 20:
            return 'Extreme Fear'
        elif value <= 40:
            return 'Fear'
        elif value <= 60:
            return 'Neutral'
        elif value <= 80:
            return 'Greed'
        else:
            return 'Extreme Greed'

    def _compare_to_history(self, value: int) -> str:
        """Compare current value to history"""

        if len(self.history) < 30:
            return 'insufficient_history'

        recent_values = [r.value for r in self.history[-30:]]
        avg = np.mean(recent_values)
        std = np.std(recent_values)

        z_score = (value - avg) / std if std > 0 else 0

        if z_score > 2:
            return 'extremely_high_vs_recent'
        elif z_score > 1:
            return 'high_vs_recent'
        elif z_score < -2:
            return 'extremely_low_vs_recent'
        elif z_score < -1:
            return 'low_vs_recent'
        else:
            return 'normal_vs_recent'

    def get_signals(self) -> Dict:
        """Get trading signals from Fear & Greed"""

        if len(self.history) < 2:
            return {'signal': 'neutral', 'strength': 0}

        current = self.history[-1]
        previous = self.history[-2]

        # Contrarian signals
        signals = {}

        # Extreme Fear = potential buying opportunity
        if current.value <= 20:
            signals['contrarian'] = 'strong_buy'
            signals['interpretation'] = 'Extreme fear often marks market bottoms'

        elif current.value <= 30:
            signals['contrarian'] = 'buy'
            signals['interpretation'] = 'Fear may indicate buying opportunity'

        # Extreme Greed = potential selling opportunity
        elif current.value >= 80:
            signals['contrarian'] = 'strong_sell'
            signals['interpretation'] = 'Extreme greed often marks market tops'

        elif current.value >= 70:
            signals['contrarian'] = 'sell'
            signals['interpretation'] = 'Greed may indicate selling opportunity'

        else:
            signals['contrarian'] = 'neutral'
            signals['interpretation'] = 'Market sentiment is balanced'

        # Momentum (change in sentiment)
        change = current.value - previous.value

        if change > 10:
            signals['momentum'] = 'improving'
        elif change < -10:
            signals['momentum'] = 'deteriorating'
        else:
            signals['momentum'] = 'stable'

        # Historical percentile
        if len(self.history) >= 100:
            all_values = [r.value for r in self.history]
            percentile = sum(1 for v in all_values if v < current.value) / len(all_values) * 100
            signals['historical_percentile'] = percentile

        return signals
```

---

## 🐋 WHALE SENTIMENT

### Whale Activity Sentiment

```python
"""
CIPHER Whale Sentiment Analysis
Derive sentiment from whale behavior
"""

from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np

@dataclass
class WhaleTransaction:
    """Large whale transaction"""
    tx_hash: str
    timestamp: datetime
    from_type: str  # 'exchange', 'wallet', 'contract'
    to_type: str
    token: str
    amount: float
    value_usd: float

class WhaleSentimentAnalyzer:
    """
    Analyze whale behavior for sentiment signals
    """

    def __init__(self):
        self.transactions: List[WhaleTransaction] = []

    def add_transaction(self, tx: WhaleTransaction):
        """Add whale transaction"""
        self.transactions.append(tx)

    def analyze(
        self,
        token: str,
        hours: int = 24
    ) -> Dict:
        """Analyze whale sentiment for a token"""

        cutoff = datetime.utcnow() - timedelta(hours=hours)

        txs = [
            t for t in self.transactions
            if t.token == token and t.timestamp > cutoff
        ]

        if not txs:
            return {'sentiment': 'neutral', 'signal_strength': 0}

        # Analyze flows
        exchange_inflow = sum(
            t.value_usd for t in txs
            if t.to_type == 'exchange'
        )

        exchange_outflow = sum(
            t.value_usd for t in txs
            if t.from_type == 'exchange'
        )

        wallet_accumulation = sum(
            t.value_usd for t in txs
            if t.to_type == 'wallet' and t.from_type != 'wallet'
        )

        # Net flow
        net_exchange_flow = exchange_inflow - exchange_outflow

        # Determine sentiment
        total_volume = sum(t.value_usd for t in txs)

        if total_volume == 0:
            return {'sentiment': 'neutral', 'signal_strength': 0}

        flow_ratio = net_exchange_flow / total_volume

        if flow_ratio > 0.3:
            sentiment = 'bearish'
            interpretation = 'Whales moving to exchanges - potential selling'
        elif flow_ratio < -0.3:
            sentiment = 'bullish'
            interpretation = 'Whales withdrawing from exchanges - accumulation'
        else:
            sentiment = 'neutral'
            interpretation = 'Balanced whale activity'

        # Signal strength (0-1)
        signal_strength = min(abs(flow_ratio) * 2, 1)

        # Large transaction analysis
        large_txs = [t for t in txs if t.value_usd > 1_000_000]

        return {
            'sentiment': sentiment,
            'interpretation': interpretation,
            'signal_strength': signal_strength,
            'metrics': {
                'exchange_inflow': exchange_inflow,
                'exchange_outflow': exchange_outflow,
                'net_exchange_flow': net_exchange_flow,
                'wallet_accumulation': wallet_accumulation,
                'total_volume': total_volume,
                'transaction_count': len(txs),
                'large_transaction_count': len(large_txs)
            },
            'largest_transactions': sorted(
                txs, key=lambda x: x.value_usd, reverse=True
            )[:5]
        }
```

---

## 🔗 CONEXIONES NEURONALES

```yaml
conexiones_primarias:
  - neurona: "ML_TRADING"
    tipo: "feature_provider"
    desc: "Sentiment features para modelos ML"

  - neurona: "MARKET_DATA"
    tipo: "data_integration"
    desc: "Combinar con datos de mercado"

  - neurona: "ON_CHAIN_ANALYTICS"
    tipo: "whale_data"
    desc: "Datos on-chain para whale sentiment"

conexiones_secundarias:
  - neurona: "TRADING_STRATEGIES"
    tipo: "signal"
    desc: "Señales de sentimiento para trading"

  - neurona: "PORTFOLIO_ANALYTICS"
    tipo: "risk_input"
    desc: "Sentimiento como factor de riesgo"
```

---

## 📊 MÉTRICAS DE LA NEURONA

```yaml
metricas_salud:
  - nombre: "Source Coverage"
    valor: 10+
    umbral_minimo: 5

  - nombre: "Post Volume/Hour"
    valor: 1000+
    umbral_alerta: 100

  - nombre: "Sentiment Accuracy"
    valor: 75%+
    umbral_alerta: 60%

  - nombre: "News Latency"
    valor: "<5min"
    umbral_alerta: "15min"
```

---

## 🔄 CHANGELOG

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2025-01-XX | Creación inicial - Twitter/Reddit analysis |
| 1.1.0 | 2025-01-XX | News sentiment, Fear & Greed Index |
| 1.2.0 | 2025-01-XX | Whale sentiment, FinBERT integration |

---

> **CIPHER**: "El mercado es una máquina de votación emocional - lee las emociones."
