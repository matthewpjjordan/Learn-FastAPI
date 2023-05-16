from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, oauth2, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
):
    posts = db.query(models.Post).limit(limit).offset(skip).all()
    return posts


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,  # sets status code for successful requests
    response_model=schemas.Post,
)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    new_post = models.Post(
        user_id=current_user.id,
        # unpacks dict into corresponding Post attributes
        **post.dict(),
    )
    db.add(new_post)
    db.commit()
    # refresh contents of instance from db e.g. includes defaults created in db
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found.",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist.",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorised to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist.",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorised to perform requested action",
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
