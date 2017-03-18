import logbook
import mailchimp


class MailingListService:
    mailchimp_api = None
    mailchimp_list_id = None
    __log = logbook.Logger('Mailing List Service')

    @staticmethod
    def global_init(api_key, list_id):
        MailingListService.mailchimp_api = api_key
        MailingListService.mailchimp_list_id = list_id

    @staticmethod
    def add_subscriber(email):
        if not MailingListService.get_is_initialized():
            MailingListService.__log.warn("CANNOT USE MAILCHIMP API. KEYS NOT SET")
            MailingListService.__log.warn("Set your API keys in development.ini / production.ini")
            return False

        # noinspection PyBroadException
        try:
            api = mailchimp.Mailchimp(apikey=MailingListService.mailchimp_api)
        except IndexError:
            MailingListService.__log.warn("Cannot initialize mailchimp, bad key?")
            return False
        except:
            MailingListService.__log.warn("Unexpected error initializing mailchimp via API key?")
            return False

        if not email or not email.strip():
            return False

        try:
            api.lists.subscribe(
                MailingListService.mailchimp_list_id,
                {'email': email.strip().lower()},
                double_optin=False,
                update_existing=True,
                replace_interests=False)
            MailingListService.__log.notice("Successfully added {} to the mailchimp list.".format(email))
            return True
        except Exception as x:
            MailingListService.__log.error("Error during mailing list signup: {}".format(x))
            return False

    @staticmethod
    def get_is_initialized():
        return MailingListService.mailchimp_api != 'ADD_YOUR_API_KEY' and \
               MailingListService.mailchimp_list_id != 'ADD_YOUR_LIST_ID'
