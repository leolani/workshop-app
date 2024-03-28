import logging.config
import os
import time

from cltl.combot.infra.config.k8config import K8LocalConfigurationContainer
from cltl.combot.infra.di_container import singleton
from cltl.combot.infra.event.memory import SynchronousEventBusContainer
from cltl.combot.infra.event_log import LogWriter
from cltl.combot.infra.resource.threaded import ThreadedResourceContainer
from cltl_service.combot.event_log.service import EventLogService
from emissor.representation.util import serializer as emissor_serializer
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from cltl.template.dummy_demo import DummyDemoProcessor
from cltl_service.template.service import TemplateService

logging.config.fileConfig(os.environ.get('CLTL_LOGGING_CONFIG', default='config/logging.config'),
                          disable_existing_loggers=False)
logger = logging.getLogger(__name__)


APP_NAME="Template App"


class InfraContainer(SynchronousEventBusContainer, K8LocalConfigurationContainer, ThreadedResourceContainer):
    def start(self):
        pass

    def stop(self):
        pass


class TemplateContainer(InfraContainer):
    logger.info("Initialized ApplicationContainer")

    @property
    @singleton
    def processor(self):
        config = self.config_manager.get_config("cltl.template")

        return DummyDemoProcessor(config.get("phrase"))

    @property
    @singleton
    def template_service(self):
        return TemplateService.from_config(self.processor, self.event_bus, self.resource_manager, self.config_manager)



class ApplicationContainer(TemplateContainer):
    @property
    @singleton
    def log_writer(self):
        config = self.config_manager.get_config("cltl.event_log")

        return LogWriter(config.get("log_dir"), serializer)

    @property
    @singleton
    def event_log_service(self):
        return EventLogService.from_config(self.log_writer, self.event_bus, self.config_manager)

    def start(self):
        logger.info("Start EventLog")
        super().start()
        self.event_log_service.start()

    def stop(self):
        try:
            logger.info("Stop EventLog")
            self.event_log_service.stop()
        finally:
            super().stop()


def serializer(obj):
    try:
        return emissor_serializer(obj)
    except Exception:
        try:
            return vars(obj)
        except Exception:
            return str(obj)


def main():
    ApplicationContainer.load_configuration()
    logger.info("Initialized Application")
    application = ApplicationContainer()

    with application as started_app:
        # ADD IF INTENTIONS ARE USED
        # intention_topic = started_app.config_manager.get_config("cltl.bdi").get("topic_intention")
        # started_app.event_bus.publish(intention_topic, Event.for_payload(IntentionEvent([Intention("init", None)])))

        routes = {
            '/template': started_app.template_service.app,
            ## YOUR ENDPOINTS HERE
        }
        # ADD for backend
        # if started_app.server:
        #     routes['/host'] = started_app.server.app

        web_app = DispatcherMiddleware(Flask(APP_NAME), routes)

        run_simple('0.0.0.0', 8000, web_app, threaded=True, use_reloader=False, use_debugger=False, use_evalex=True)

        # intention_topic = started_app.config_manager.get_config("cltl.bdi").get("topic_intention")
        # started_app.event_bus.publish(intention_topic, Event.for_payload(IntentionEvent([Intention("terminate", None)])))
        time.sleep(1)


if __name__ == '__main__':
    main()

