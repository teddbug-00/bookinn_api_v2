from datetime import datetime
import time
from math import log10, exp, pow, sqrt
from typing import Optional

from src.models.listing import PropertyListing

def calculate_popularity_score(listing: PropertyListing) -> float:
    """
    Calculate a weighted popularity score based on multiple factors:
    - Recent bookmarks (30%): Emphasizes recent user interest
    - Review quality (25%): Combines rating and review count
    - View engagement (20%): Reflects listing visibility/interest
    - Listing freshness (15%): Prioritizes newer listings
    - Booking completion rate (10%): Rewards successful bookings
    
    Returns a normalized score between 0 and 100
    """
    now = datetime.now()

    start = time.time()
    
    # Recent bookmarks score (30%)
    recent_bookmarks = _calculate_recent_bookmarks(listing.bookmarks, now)
    bookmark_score = min(30, log10(max(1, recent_bookmarks)) * 15)
    
    # Review quality score (25%)
    review_score = _calculate_review_score(
        listing.total_reviews,
        listing.average_rating
    )
    
    # View engagement score (20%)
    view_score = _calculate_view_score(
        listing.view_count,
        listing.total_bookmarks,
        days_active=(now - listing.created_at).days
    )
    
    # Freshness score (15%) 
    freshness_score = _calculate_freshness_score(
        created_at=listing.created_at,
        now=now
    )
    
    # Booking completion rate (10%)
    completion_score = _calculate_completion_score(
        total_bookings=getattr(listing, 'total_bookings', 0),
        cancelled_bookings=getattr(listing, 'cancelled_bookings', 0)
    )

    # Combine all scores
    total_score = (
        bookmark_score +
        review_score + 
        view_score +
        freshness_score +
        completion_score
    )

    print(f"Score: {str(round(total_score, 2))}. Calculation took {str((time.time() - start))} s")
    
    return round(total_score, 2)

def _calculate_recent_bookmarks(bookmarks: list, now: datetime) -> int:
    """Calculate weighted sum of bookmarks, with more recent ones counting more"""
    total = 0
    for bookmark in bookmarks:
        days_ago = (now - bookmark.added_on).days
        if days_ago <= 30:  # Last 30 days
            weight = exp(-days_ago/30)  # Exponential decay
            total += weight
    return total

def _calculate_review_score(total_reviews: int, avg_rating: Optional[float]) -> float:
    """
    Calculate review score using Wilson score confidence interval
    This helps balance between rating and number of reviews
    """
    if not total_reviews or avg_rating is None:
        return 0
        
    # Normalize rating to 0-1 scale
    avg = (avg_rating / 5.0)
    
    # Wilson score calculation
    z = 1.96  # 95% confidence
    n = total_reviews
    
    if n == 0:
        return 0
        
    p = avg
    
    # Wilson score formula
    numerator = (p + z*z/(2*n) - z * ((p*(1-p) + z*z/(4*n))/n)**0.5)
    denominator = (1 + z*z/n)
    
    wilson_score = numerator / denominator
    
    # Convert back to 25-point scale
    return min(25, wilson_score * 25)

def _calculate_view_score(views: int, bookmarks: int, days_active: int) -> float:
    """
    Calculate engagement score based on views and bookmarks per day
    Uses logarithmic scaling to handle large numbers
    """
    if days_active < 1:
        days_active = 1
        
    daily_views = views / days_active
    daily_bookmarks = bookmarks / days_active
    
    view_component = log10(max(1, daily_views)) * 8
    bookmark_component = log10(max(1, daily_bookmarks)) * 12
    
    return min(20, view_component + bookmark_component)

def _calculate_freshness_score(created_at: datetime, now: datetime) -> float:
    """
    Calculate freshness score with exponential decay over time
    Newer listings get higher scores
    """
    days_old = (now - created_at).days
    half_life = 90  # Score halves every 90 days
    
    decay = exp(-days_old * log10(2) / half_life)
    return 15 * decay

def _calculate_completion_score(total_bookings: int, cancelled_bookings: int) -> float:
    """
    Calculate score based on booking completion rate
    Rewards listings with high booking completion rates
    """
    if total_bookings == 0:
        return 5  # Neutral score for new listings
        
    completion_rate = (total_bookings - cancelled_bookings) / total_bookings
    return min(10, completion_rate * 10)