import tornado.ioloop
import tornado.web
from add_movie import AddMovieHandler
from admin_login import AdLoginHandler
from del_movie import DeleteMovieHandler
from edit_movie import EditMovieHandlercl
from signup import UserHandler
from search_movie import SearchHandlerByTitle
from user_home import HomeHandler
from user_login import LoginHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        response = {
            'message': 'Hello, world!'
        }
        self.write(response)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/users", UserHandler),
        (r"/login", LoginHandler),
        (r"/admin_login", AdLoginHandler),
        (r"/user_home", HomeHandler),
        (r"/add_movie", AddMovieHandler),
        (r"/del_movie", DeleteMovieHandler),
        (r"/edit_movie", EditMovieHandler),
        (r"/search_movie", SearchHandlerByTitle),

    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    print("Server is running on http://localhost:8080")
    tornado.ioloop.IOLoop.current().start()