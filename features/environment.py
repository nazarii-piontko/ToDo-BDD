from behave.log_capture import capture
from infrastucture.testing_context import TestingContext


@capture
def before_scenario(context, scenario):
    context.context = TestingContext()
    context.context.start()


@capture
def after_scenario(context, scenario):
    context.context.stop()
