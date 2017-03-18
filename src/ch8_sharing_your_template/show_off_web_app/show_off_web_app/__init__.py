import datetime
import pkg_resources
import os
import sys
from pyramid.config import Configurator
# noinspection PyUnresolvedReferences
import show_off_web_app
import show_off_web_app.controllers.home_controller as home
import show_off_web_app.controllers.account_controller as account
import show_off_web_app.controllers.newsletter_controller as news
from show_off_web_app.data.dbsession import DbSessionFactory
from show_off_web_app.email.template_paser import EmailTemplateParser
from show_off_web_app.services.email_service import EmailService
from show_off_web_app.services.log_service import LogService
from show_off_web_app.services.mailinglist_service import MailingListService

dev_mode = False


def main(_, **settings):
    config = Configurator(settings=settings)

    init_logging(config)  # log setup must run first
    init_mode(config)  # mode must go next
    init_includes(config)  # includes must go next
    init_routing(config)  # it's pretty much flexible from here on down
    init_db(config)
    init_mailing_list(config)
    init_smtp_mail(config)
    init_email_templates(config)

    return config.make_wsgi_app()


def init_logging(config):
    settings = config.get_settings()
    log_level = settings.get('log_level')
    log_filename = settings.get('log_filename')

    LogService.global_init(log_level, log_filename)

    log_package_versions()


def init_email_templates(_):
    EmailTemplateParser.global_init()


def init_smtp_mail(config):
    global dev_mode
    unset = 'YOUR_VALUE'

    settings = config.get_settings()
    smtp_username = settings.get('smtp_username')
    smtp_password = settings.get('smtp_password')
    smtp_server = settings.get('smtp_server')
    smtp_port = settings.get('smtp_port')

    local_dev_mode = dev_mode

    if smtp_username == unset:
        log = LogService.get_startup_log()
        log.warn("SMTP server values not set in config file. "
                 "Outbound email will not work.")
        local_dev_mode = True  # turn off email if the system has no server.

    EmailService.global_init(smtp_username, smtp_password, smtp_server, smtp_port, local_dev_mode)


def init_db(_):
    global dev_mode

    top_folder = os.path.dirname(show_off_web_app.__file__)
    rel_file = os.path.join('db', 'show_off_web_app.sqlite')
    if dev_mode:
        rel_file = rel_file.replace('.sqlite', '_dev.sqlite')
    else:
        rel_file = rel_file.replace('.sqlite', '_prod.sqlite')

    db_file = os.path.join(top_folder, rel_file)
    DbSessionFactory.global_init(db_file)


def init_mode(config):
    global dev_mode
    settings = config.get_settings()
    dev_mode = settings.get('mode') == 'dev'
    log = LogService.get_startup_log()
    log.notice('Running in {} mode.'.format('dev' if dev_mode else 'prod'))


def init_mailing_list(config):
    unset = 'ADD_YOUR_API_KEY'

    settings = config.get_settings()
    mailchimp_api = settings.get('mailchimp_api')
    mailchimp_list_id = settings.get('mailchimp_list_id')

    if mailchimp_api == unset:
        log = LogService.get_startup_log()
        log.warn("Mailchimp API values not set in config file. "
                 "Mailing list subscriptions will not work.")

    MailingListService.global_init(mailchimp_api, mailchimp_list_id)


def init_routing(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_handler('root', '/', handler=home.HomeController, action='index')

    add_controller_routes(config, home.HomeController, 'home')
    add_controller_routes(config, account.AccountController, 'account')
    add_controller_routes(config, news.NewsletterController, 'newsletter')

    config.scan()


def add_controller_routes(config, ctrl, prefix):
    config.add_handler(prefix + 'ctrl_index', '/' + prefix, handler=ctrl, action='index')
    config.add_handler(prefix + 'ctrl_index/', '/' + prefix + '/', handler=ctrl, action='index')
    config.add_handler(prefix + 'ctrl', '/' + prefix + '/{action}', handler=ctrl)
    config.add_handler(prefix + 'ctrl/', '/' + prefix + '/{action}/', handler=ctrl)
    config.add_handler(prefix + 'ctrl_id', '/' + prefix + '/{action}/{id}', handler=ctrl)


def init_includes(config):
    config.include('pyramid_chameleon')
    config.include('pyramid_handlers')
    # config.include('rollbar.contrib.pyramid')


def log_package_versions():
    startup_log = LogService.get_startup_log()

    # TODO: UPDATE WITH OUR DEPENDENCIES

    # update from setup.py when changed!
    # This list is the closure of all dependencies,
    # taken from: pip list --format json
    requires = [{"name": "show_off_web_app", "version": "0.0"}, {"name": "appdirs", "version": "1.4.3"},
                {"name": "Chameleon", "version": "3.1"}, {"name": "docopt", "version": "0.4.0"},
                {"name": "html2text", "version": "2016.9.19"}, {"name": "hupper", "version": "0.4.4"},
                {"name": "Logbook", "version": "1.0.0"}, {"name": "mailchimp", "version": "2.0.9"},
                {"name": "mailer", "version": "0.8.1"}, {"name": "Mako", "version": "1.0.6"},
                {"name": "MarkupSafe", "version": "1.0"}, {"name": "packaging", "version": "16.8"},
                {"name": "passlib", "version": "1.7.1"}, {"name": "PasteDeploy", "version": "1.5.2"},
                {"name": "pip", "version": "9.0.1"}, {"name": "Pygments", "version": "2.2.0"},
                {"name": "pyparsing", "version": "2.2.0"}, {"name": "pyramid", "version": "1.8.3"},
                {"name": "pyramid-chameleon", "version": "0.3"}, {"name": "pyramid-debugtoolbar", "version": "3.0.5"},
                {"name": "pyramid-handlers", "version": "0.5"}, {"name": "pyramid-mako", "version": "1.0.2"},
                {"name": "repoze.lru", "version": "0.6"}, {"name": "requests", "version": "2.13.0"},
                {"name": "rollbar", "version": "0.13.11"}, {"name": "setuptools", "version": "34.3.2"},
                {"name": "six", "version": "1.10.0"}, {"name": "SQLAlchemy", "version": "1.1.6"},
                {"name": "translationstring", "version": "1.3"}, {"name": "venusian", "version": "1.0"},
                {"name": "waitress", "version": "1.0.2"}, {"name": "WebOb", "version": "1.7.2"},
                {"name": "zope.deprecation", "version": "4.2.0"}, {"name": "zope.interface", "version": "4.3.3"}]

    requires.sort(key=lambda d: d['name'].lower())
    t0 = datetime.datetime.now()
    startup_log.notice('---------- Python version info ------------------')
    startup_log.notice(sys.version.replace('\n', ' ').replace('  ', ' '))
    startup_log.notice('---------- package version info ------------------')
    for rec in requires:
        try:
            version = pkg_resources.get_distribution(rec['name']).version
            if version:
                startup_log.notice('{} v{}'.format(rec['name'], version))
            else:
                startup_log.notice("WHERE IS IT? {}.".format(rec['name']))
        except Exception as x:
            startup_log.notice('{} UNKNOWN VERSION ({})'.format(rec['name'], x))

    dt = datetime.datetime.now() - t0

    startup_log.notice('Package info gathered in {} sec'.format(dt.total_seconds()))
    startup_log.notice('--------------------------------------------------')
