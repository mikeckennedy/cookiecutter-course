import pyramid_handlers
from show_off_web_app.controllers.base_controller import BaseController
from show_off_web_app.services.mailinglist_service import MailingListService


class NewsletterController(BaseController):
    # POST /newsletter/add_subscriber
    @pyramid_handlers.action(request_method='POST')
    def add_subscriber(self):
        email = self.merged_dicts.get('email')

        if MailingListService.add_subscriber(email):
            self.redirect('/newsletter/subscribed')

        self.redirect('/newsletter/failed')

    @pyramid_handlers.action(renderer='templates/newsletter/subscribed.pt')
    def subscribed(self):
        return {}

    @pyramid_handlers.action(renderer='templates/newsletter/failed.pt')
    def failed(self):
        error = None
        if not MailingListService.get_is_initialized():
            error = 'Your mailing list service is not initialized (keys missing in *.ini files)'

        return {
            'error': error
        }
