from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from db import get_db_connection, create_essay_table, create_metrics_table
import random,asyncio

app = Flask(__name__)

# Create the 'uploads' folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load environment variables from the .env file
load_dotenv()

# Retrieve database credentials from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
connection = get_db_connection(DATABASE_URL)

# Initialize the database
create_essay_table(connection)
create_metrics_table(connection)


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
                        organisation, language_use, 
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
        


#handles the post request
@app.route('/grade', methods=['POST'])
async def submit_essay():
    try:
        data = request.get_json()
        title = data.get('title')
        essay = data.get('essay')
        # Generate a unique filename using the essay_id
        with connection.cursor() as cursor:
            cursor.execute("SELECT essay_id FROM essay_db ORDER BY essay_id DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                essay_id = result[0] + 1 
            else:
                essay_id = 1
        
        filename = f"essay{essay_id}.txt"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
        
        # Save the essay to a file
        with open(file_path, 'w+') as file:
            file.write(title + " \n\n " + essay)

        # Store the directory in the database
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO essay_db (directory,essay_id) VALUES (%s,%s)", (file_path,essay_id))
            connection.commit()
            
        
        await update_metrics(essay_id,file_path)
        return jsonify({'essay_id': essay_id, 'message': 'File saved successfully.'}), 200
        
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error saving file.' + str(e)}), 500

# Handles the get request
@app.route('/metrics', methods=['GET'])
def get_essay():
    try:
        data = request.get_json()
        essay_id = data.get('essay_id')

        # Retrieve the directory from the database based on essay_id
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM metrics_db WHERE essay_id = %s", (essay_id,))
            result = cursor.fetchone()

        if result:
            result = {
                'essay_id': result[0],
                'focus_and_development': result[1],
                'content_development': result[2],
                'organisation': result[3],
                'language_use': result[4],
                'Holistic_Score': result[5]
            }
            return jsonify({'metrics': result}), 200
        else:
            return jsonify({'message': 'File not found for the given essay_id.'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error retrieving file directory.' + str(e)}), 500


if __name__ == '__main__':
    asyncio.run(app.run(debug=True))
