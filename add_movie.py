import tornado.web
import json
from con import Database  
class AddMovieHandler(tornado.web.RequestHandler, Database):
    movie_table = Database.db['movies']

    async def post(self):
        code = 1000
        status = False
        result = []
        message = ''

        try:
            # Parse the request body as JSON
            try:
                self.request.arguments = json.loads(self.request.body.decode())
            except Exception as e:
                code = 1001
                message = "Invalid JSON"
                raise Exception

            # Extract movie details from request
            title = self.request.arguments.get('title')
            genre = self.request.arguments.get('genre')
            duration = self.request.arguments.get('duration')
            release_date = self.request.arguments.get('release_date')
            director = self.request.arguments.get('director')
            showtimes = self.request.arguments.get('showtimes')

            movie_data = {
                'title': title,
                'genre': genre,
                'duration': duration,
                'release_date': release_date,
                'director': director,
                'showtimes': showtimes,          
            }
            movie_result = await self.movie_table.insert_one(movie_data)

            if movie_result.inserted_id:
                code = 2000
                status = True
                message = "Movie added successfully"
                result.append({
                    'movieId': str(movie_result.inserted_id)
                })
            else:
                code = 1006
                message = "Failed to add movie"
                raise Exception

        except Exception as e:
            code = 1003
            if not len(message):
                message = 'Internal error'
                print(e)
                raise Exception

        response = {
            'code': code,
            'message': message,
            'status': status,
        }

        try:
            if len(result):
                response['result'] = result
            self.write(response)
            self.finish()
        except Exception as e:
            message = 'There is some issue'
            code = 1004
            raise Exception
