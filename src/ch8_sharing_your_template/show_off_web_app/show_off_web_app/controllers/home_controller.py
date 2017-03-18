import pyramid_handlers
from show_off_web_app.controllers.base_controller import BaseController
from show_off_web_app.infrastructure.supressor import suppress


class HomeController(BaseController):
    alternate_mode = False

    @pyramid_handlers.action(renderer='templates/home/index.pt')
    def index(self):
        return {'value': 'HOME'}

    @pyramid_handlers.action(renderer='templates/home/about.pt')
    def about(self):
        return {'value': 'ABOUT'}

    @pyramid_handlers.action(renderer='templates/home/bookus.pt')
    def bookus(self):
        return {}

    @pyramid_handlers.action(renderer='templates/home/contact.pt')
    def contact(self):
        return {'value': 'CONTACT'}

    @pyramid_handlers.action(renderer='templates/home/not_implemented.pt')
    def not_implemented(self):
        return {}

    @pyramid_handlers.action(renderer='templates/home/image_credits.pt')
    def image_credits(self):
        return {}

    @suppress()
    def dont_expose_as_web_action(self):
        print("Called dont_expose_as_web_action, what happened?")

    def alternate_row_style(self):
        alt = self.alternate_mode
        self.alternate_mode = not self.alternate_mode

        if alt:
            return "alternate"
        else:
            return ""


