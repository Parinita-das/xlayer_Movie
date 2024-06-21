import tornado.ioloop
import tornado.web

from admin.add_city import AddCityHandler
from admin.add_movie import AddMovieHandler
from authorization.admin_login import AdLoginHandler
from user.booking import BookingHandler
from admin.del_city import DeleteCityHandler
from admin.del_movie import DeleteMovieHandler
from admin.edit_movie import EditMovieHandler
from user.get_seats import BookedSeatsHandler
from user.select_city import CityDropdownHandler
from authorization.signup import UserHandler
from user.search_movie import SearchHandlerByTitle
from authorization.user_login import LoginHandler

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
        (r"/add_movie", AddMovieHandler),
        (r"/del_movie", DeleteMovieHandler),
        (r"/edit_movie", EditMovieHandler),
        (r"/search_movie", SearchHandlerByTitle),
        (r"/add_city", AddCityHandler),
        (r"/del_city", DeleteCityHandler),
        (r"/select_city", CityDropdownHandler),
        (r"/booking", BookingHandler),
        (r"/get_seats", BookedSeatsHandler),

      


    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    print("Server is running on http://localhost:8080")
    tornado.ioloop.IOLoop.current().start()