from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from pydantic.fields import _FIELD_ARG_NAMES
from app.schemas import PostCreate, PostResponse, UserCreate, UserRead, UserUpdate
from app.db import Post, create_db_end_tables, get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile
from app.users import auth_backend, current_active_user, fastapi_users

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_end_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )
        print(upload_result)
        if upload_result.response_metadata.http_status_code == 200:
            post = Post(
                user_id = user.id,
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name,
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()    
 

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    user_dict = {u.id: u.email for u in users}
    
    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
                "is_owner": post.user_id == user.id,
                "email": user_dict.get(post.user_id, "Unknown")
            }
        )
    return {"posts": posts_data}

@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="You don't have permission to delete this post")
        
        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))        


# without DB connection

# text_posts = {
#     1: {
#         "title": "When Data Engineers Debug",
#         "content": "Step 1: Check logs\nStep 2: Blame Kafka\nStep 3: Restart everything\nStep 4: It magically works\n#DataEngineering #FunnyTech"
#     },
#     2: {
#         "title": "ETL in Real Life",
#         "content": "Extract emotions, Transform into motivation, Load into career.\n#ETL #DataLife"
#     },
#     3: {
#         "title": "Data Engineer’s Horoscope",
#         "content": "You will face missing values today. Don’t worry — a little cleaning will clear your path.\n#DataHumor #Analytics"
#     },
#     4: {
#         "title": "SQL Love Story",
#         "content": "SELECT * FROM life WHERE happiness = TRUE;\nResult: 0 rows returned.\n#SQL #DeveloperHumor"
#     },
#     5: {
#         "title": "Data Pipeline Therapy",
#         "content": "‘Tell me where it hurts,’ said the Data Engineer.\n‘Everywhere,’ whispered the DAG.\n#Airflow #ETL #TechJokes"
#     },
#     6: {
#         "title": "When AI Fails",
#         "content": "People blame data engineers.\nWhen AI succeeds? Nobody remembers us.\n#AI #DataEngineeringTruth"
#     },
#     7: {
#         "title": "Data Engineer’s Workout Plan",
#         "content": "Lifting tables. Dropping indexes. Running queries.\n#SQL #DataFitness"
#     },
#     8: {
#         "title": "Streaming Mindset",
#         "content": "Batch people plan. Streamers adapt.\n#Kafka #DataStreaming #Mindset"
#     },
#     9: {
#         "title": "Null Values Everywhere",
#         "content": "My data has more missing values than my sleep schedule.\n#DataQuality #FunnyData"
#     },
#     10: {
#         "title": "Career Advice",
#         "content": "Learn data. The world runs on it.\nEven your memes are powered by recommendation algorithms.\n#DataCareer #Inspiration"
#     }
# }

# @app.get("/posts")
# def get_all_posts(limit: int = None):
#     if limit:
#         return list(text_posts.values())[:limit]
#     return text_posts    

# @app.get(f"/posts/{id}")
# def get_post(id: int) -> PostResponse:
#     if id not in text_posts:
#         raise HTTPException(status_code=404, detail="Post not found")

#     return text_posts.get(id)

# @app.post("/posts")
# def create_post(post: PostCreate) -> PostResponse:
#     new_post = {"title": post.title, "content": post.content}
#     text_posts[max(text_posts.keys()) + 1] = new_post
#     return new_post