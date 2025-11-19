from fastapi import FastAPI, HTTPException

app = FastAPI()

text_posts = {
    1: {
        "title": "When Data Engineers Debug",
        "content": "Step 1: Check logs\nStep 2: Blame Kafka\nStep 3: Restart everything\nStep 4: It magically works\n#DataEngineering #FunnyTech"
    },
    2: {
        "title": "ETL in Real Life",
        "content": "Extract emotions, Transform into motivation, Load into career.\n#ETL #DataLife"
    },
    3: {
        "title": "Data Engineer’s Horoscope",
        "content": "You will face missing values today. Don’t worry — a little cleaning will clear your path.\n#DataHumor #Analytics"
    },
    4: {
        "title": "SQL Love Story",
        "content": "SELECT * FROM life WHERE happiness = TRUE;\nResult: 0 rows returned.\n#SQL #DeveloperHumor"
    },
    5: {
        "title": "Data Pipeline Therapy",
        "content": "‘Tell me where it hurts,’ said the Data Engineer.\n‘Everywhere,’ whispered the DAG.\n#Airflow #ETL #TechJokes"
    },
    6: {
        "title": "When AI Fails",
        "content": "People blame data engineers.\nWhen AI succeeds? Nobody remembers us.\n#AI #DataEngineeringTruth"
    },
    7: {
        "title": "Data Engineer’s Workout Plan",
        "content": "Lifting tables. Dropping indexes. Running queries.\n#SQL #DataFitness"
    },
    8: {
        "title": "Streaming Mindset",
        "content": "Batch people plan. Streamers adapt.\n#Kafka #DataStreaming #Mindset"
    },
    9: {
        "title": "Null Values Everywhere",
        "content": "My data has more missing values than my sleep schedule.\n#DataQuality #FunnyData"
    },
    10: {
        "title": "Career Advice",
        "content": "Learn data. The world runs on it.\nEven your memes are powered by recommendation algorithms.\n#DataCareer #Inspiration"
    }
}

@app.get("/posts")
def get_all_posts():
    return text_posts

@app.get(f"/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")

    return text_posts.get(id)
