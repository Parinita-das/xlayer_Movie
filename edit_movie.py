from bson import ObjectId
import tornado.web
import json
from con import Database 

class EditMovieHandler(tornado.web.RequestHandler):
    async def post(self):
        code = 1000
        status = False
        message = ''

        try:
            # Extract title and updated data from request body
            request_data = json.loads(self.request.body)
            movie_title = request_data.get('title')
            updated_data = request_data.get('updated_data', {})

            movie_table = Database.db['movies']

            movie = await movie_table.find_one({'title': movie_title})

            if movie:
                # Update the movie document with the updated_data
                updated_movie = {**movie, **updated_data}  
                update_result = await movie_table.replace_one({'title': movie_title}, updated_movie)

                if update_result.modified_count > 0:
                    code = 2000
                    status = True
                    message = "Movie updated successfully"
                else:
                    code = 1007
                    message = "Update operation failed"
                    raise Exception
            else:
                code = 1007
                message = "Movie not found"

        except Exception as e:
            code = 1003
            message = 'Internal error'
            print(e)

        response = {
            'code': code,
            'message': message,
            'status': status,
        }

        self.write(response)
        self.finish()
