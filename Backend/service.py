import random,asyncio
import os
from db import get_db_connection
from dotenv import load_dotenv

load_dotenv()

# Retrieve database credentials from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
connection = get_db_connection(DATABASE_URL)

# Dummy function that generates the example metrics and delays for 10 sec
async def dummy_ml_function(essay_id, file_path):
    example_metrics = {
        'focus_and_development': round(random.uniform(0.0, 10.0), 2),
        'content_development': round(random.uniform(0.0, 10.0), 2),
        'organisation': round(random.uniform(0.0, 10.0), 2),
        'language_use': round(random.uniform(0.0, 10.0), 2),
        'Holistic_Score': round(random.uniform(0.0, 10.0), 2)
    }
    await asyncio.sleep(10)
    return example_metrics

# Generate a unique filename using the essay_id
def get_essay_id():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT essay_id FROM essay_db ORDER BY essay_id DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                essay_id = result[0] + 1 
            else:
                essay_id = 1
        return essay_id
    except Exception as e:
        raise e

# Writes the contents to the file
def write_essay_to_file(essay_id,title,essay,app):
    UPLOAD_FOLDER = 'assets'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    try:
        file_name = f"essay{essay_id}.txt"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)  
        with open(file_path, 'w+') as file:
            file.write(title + " \n\n " + essay)
        return file_path
    except Exception as e:
        raise e

# Stores directory in the database
def save_essay_info_to_db(file_path,essay_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO essay_db (directory,essay_id) VALUES (%s,%s)", (file_path,essay_id))
            connection.commit()
    except Exception as e:
        raise e

# Updates the metrics to the database
async def update_metrics(essay_id, file_path):
    metrics  =  await dummy_ml_function(essay_id,file_path)
    try:
        with connection.cursor() as cursor:
            insert_query = """
                    INSERT INTO metrics_db (
                        essay_id, 
                        focus_and_development, 
                        content_development, 
                        organisation,
                        language_use, 
                        Holistic_Score)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
            cursor.execute(insert_query, (
                    essay_id,
                    metrics.get('focus_and_development'),
                    metrics.get('content_development'),
                    metrics.get('organisation'),
                    metrics.get('language_use'),
                    metrics.get('Holistic_Score')
                ))
            connection.commit()
    except Exception as e:
        raise e

# Retrieves the metrics from the database
def get_metrics_from_db(essay_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM metrics_db WHERE essay_id = %s", (essay_id,))
            result = cursor.fetchone()
        return result
    except Exception as e:
        raise e

