
from robophery.base import ModuleManager


def test_manager_fixture(robophery):

    assert issubclass(robophery.__class__, ModuleManager)


def test_manager_config(robophery):

    assert isinstance(robophery._config, dict)
