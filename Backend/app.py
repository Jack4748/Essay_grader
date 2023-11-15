import asyncio
from flask import request, jsonify,Flask 
import os
from dotenv import load_dotenv
from db import get_db_connection, create_essay_table, create_metrics_table
from service import update_metrics, get_essay_id, write_essay_to_file, save_essay_info_to_db, get_metrics_from_db

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

# Retrieve database credentials from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
connection = get_db_connection(DATABASE_URL)

# Initialize the database
create_essay_table(connection)
create_metrics_table(connection)

#handles the post request
@app.route('/grade', methods=['POST'])
async def submit_essay():
    try:
        data = request.get_json()
        title = data.get('title')
        essay = data.get('essay')
        essay_id = get_essay_id()
        file_path = write_essay_to_file(essay_id,title,essay,app)    
        save_essay_info_to_db(file_path, essay_id)
        await update_metrics(essay_id,file_path)

        return jsonify({'essay_id': essay_id, 'message': 'File saved successfully.'}), 200      
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error saving file.' + str(e)}), 500

# Handles the get request
@app.route('/metrics/<int:essay_id>', methods=['GET'])
def get_metrics(essay_id):
    try:
        result = get_metrics_from_db(essay_id)
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
        return jsonify({'message': 'Error retrieving file directory.' + str(e)}), 50

if __name__ == "__main__":
    asyncio.run(app.run(debug=True))

