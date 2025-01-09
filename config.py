from dynaconf import Dynaconf
import atexit
import logging
import logging.config
import logging.handlers

# `settings_files` = Load these files in the order.
# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
class Config(object):

    def __init__(self) -> None:

        self.settings = Dynaconf(
            envvar_prefix = "Voter-Reg",
            settings_files = ['settings.toml', '.secrets.toml'],
            environments = True,
            load_dotenv = True,
            env = "development",
            env_switcher = "Voter-Reg_ENV"
        )

    def setup_logging(self) -> None:

        logging.config.dictConfig(self.settings.logging)
        
        queue_handler = logging.getHandlerByName("queue")
        if queue_handler is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)
