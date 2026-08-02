from http.client import HTTPException, HTTPException

from fastapi import APIRouter, Depends , Query
from sqlmodel import Session, func, select, update, update
from database import get_session
from model import Review, ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.get("/", response_model=ReviewRead)
def get_reviews(session: Session = Depends(get_session),
                    movie_name: str = Query(None, description="Filter by movie name"),
                    skip: int = Query(0 , ge=0),
                    limit: int = Query(5 , ge=0, le=100)
                ):
    """Get all reviews Paginated"""
    query = select(Review)
    if movie_name:
        query = query.where(Review.movie_name == movie_name)
    reviews = session.exec(query.offset(skip).limit(limit)).all()
    return reviews

@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, session: Session = Depends(get_session)):
    """Create a new review"""
    db_review = Review(
        movie_name=review.movie_name,
        reviewer_name=review.reviewer_name,
        rating=review.rating,
        comment=review.comment
    )
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

@router.get("/{review_id}", response_model=ReviewRead)
def get_review(review_id: int, session: Session = Depends(get_session)):
    """Get a review by ID"""
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=ReviewRead)
def update_review(review_id: int, review_update: ReviewUpdate, session: Session = Depends(get_session)):
    """Update a review by ID"""
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review

@router.delete("/{review_id}", response_model=ReviewRead)
def delete_review(review_id: int, session: Session = Depends(get_session)):
    """Delete a review by ID"""
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    session.delete(review)
    session.commit()
    return review

@router.get("/avg-rating/{movie_name}", response_model=float)
def get_avg_rating(movie_name: str, session: Session = Depends(get_session)):
    """Get the average rating for a movie"""
    result  = session.exec(
        select(func.avg(Review.rating) , func.count(Review.rating)).where(Review.movie_name == movie_name)
    ).first()
    avg_rating, total_reviews = result
    if total_reviews == 0:
        raise HTTPException(status_code=404, detail="No reviews found for this movie")
    return {
        "movie_name": movie_name,
        "average_rating": round(avg_rating, 2),
        "total_reviews": total_reviews
    }
