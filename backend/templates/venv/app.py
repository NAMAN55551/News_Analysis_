from flask import Flask, render_template, jsonify, request
import json
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

def load_news_data():
    """Load processed news data from JSON file"""
    try:
        with open("all_news_processed.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("all_news_processed.json not found!")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON file!")
        return {}

def search_articles(data, query, category_filter=None):
    """Search articles based on query and optional category filter"""
    if not query and not category_filter:
        return data
    
    results = {}
    query_lower = query.lower() if query else ""
    
    for category, articles in data.items():
        # Apply category filter if specified
        if category_filter and category_filter != "All" and category.lower() != category_filter.lower():
            continue
            
        filtered_articles = []
        
        for article in articles:
            # Search in multiple fields
            search_fields = [
                article.get("title", ""),
                article.get("description", ""),
                article.get("content", ""),
                article.get("preprocessed_text", ""),
                category
            ]
            
            # Check if query matches any field
            if not query_lower:
                # If no query, include all articles (category filter already applied)
                filtered_articles.append(article)
            else:
                for field in search_fields:
                    if field and query_lower in field.lower():
                        filtered_articles.append(article)
                        break
        
        if filtered_articles:
            results[category] = filtered_articles
    
    return results

@app.route("/")
def index():
    """Serve the main page with all news data"""
    data = load_news_data()
    return render_template("index.html", news=data)

@app.route("/api/news")
def api_news():
    """Get all news articles"""
    data = load_news_data()
    return jsonify(data)

@app.route("/api/search")
def api_search():
    """Search news articles with query and optional category filter"""
    query = request.args.get('q', '')
    category_filter = request.args.get('category', None)
    
    data = load_news_data()
    results = search_articles(data, query, category_filter)
    
    return jsonify({
        "query": query,
        "category_filter": category_filter,
        "results": results,
        "total_articles": sum(len(articles) for articles in results.values())
    })

@app.route("/api/categories")
def api_categories():
    """Get all available categories"""
    data = load_news_data()
    categories = list(data.keys())
    return jsonify({"categories": categories})

@app.route("/api/stats")
def api_stats():
    """Get statistics about the news data"""
    data = load_news_data()
    stats = {}
    
    total_articles = 0
    sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    
    for category, articles in data.items():
        category_stats = {
            "total": len(articles),
            "sentiments": {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
        }
        
        for article in articles:
            total_articles += 1
            sentiment = article.get("sentiment", "NEUTRAL")
            category_stats["sentiments"][sentiment] = category_stats["sentiments"].get(sentiment, 0) + 1
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        stats[category] = category_stats
    
    return jsonify({
        "total_articles": total_articles,
        "categories": stats,
        "overall_sentiment": sentiment_counts
    })

@app.route("/api/article/<int:article_id>")
def api_article(article_id):
    """Get a specific article by ID (simplified - using index in category)"""
    data = load_news_data()
    
    # This is a simplified approach - in a real app, you'd have proper article IDs
    for category, articles in data.items():
        if article_id < len(articles):
            return jsonify(articles[article_id])
    
    return jsonify({"error": "Article not found"}), 404

if __name__ == "__main__":
    print("Starting Flask News API server...")
    print("Available endpoints:")
    print("- GET /api/news - Get all news articles")
    print("- GET /api/search?q=query&category=filter - Search articles")
    print("- GET /api/categories - Get all categories")
    print("- GET /api/stats - Get news statistics")
    print("- GET /api/article/<id> - Get specific article")
    
    app.run(debug=True, host='0.0.0.0', port=5000)