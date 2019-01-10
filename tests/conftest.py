import logging
import uuid

import pytest

import hlbox
from hlbox import config as hlbox_config, sandboxes
from hlbox.utils import get_docker_client


def pytest_addoption(parser):
    parser.addoption('--docker-url', action='store', default=None,
                     help="Use this url to connect to a Docker backend server")


@pytest.fixture(scope='session')
def docker_url(request):
    return request.config.getoption('docker_url')


@pytest.fixture(scope='session')
def docker_client(docker_url):
    return get_docker_client(base_url=docker_url)


@pytest.fixture(scope='session')
def docker_image():
    return 'python:3.6.5-alpine'


@pytest.fixture(scope='session')
def profile(docker_image):
    return hlbox.Profile('python', docker_image,
                           command='python3 -c \'print("profile stdout")\'')


@pytest.fixture(scope='session')
def profile_read_only(docker_image):
    return hlbox.Profile('python_read_only', docker_image,
                           command='python3 -c \'print("profile stdout")\'',
                           read_only=True)


@pytest.fixture(scope='session')
def profile_unknown_image():
    return hlbox.Profile('unknown_image', 'unknown_image:tag',
                           command='unknown')


@pytest.fixture(scope='session', autouse=True)
def configure(profile, profile_read_only, profile_unknown_image, docker_url):
    hlbox.configure(profiles=[profile, profile_read_only,
                                profile_unknown_image],
                      docker_url=docker_url)
    # Standard logging to console
    console = logging.StreamHandler()
    logging.getLogger().addHandler(console)


@pytest.fixture(autouse=True)
def configure_pytest_logging(caplog):
    caplog.set_level(logging.INFO)


@pytest.fixture(scope='session', autouse=True)
def isolate_and_cleanup_test_containers(docker_client):
    sandboxes._SANDBOX_NAME_PREFIX = 'hlbox-test-'
    yield
    test_containers = docker_client.containers.list(
        filters={'name': 'hlbox-test'}, all=True)
    for container in test_containers:
        container.remove(v=True, force=True)


@pytest.fixture(scope='session')
def test_utils(docker_client, docker_image):
    class TestUtils(object):
        def create_test_container(self, **kwargs):
            kwargs.update(name='hlbox-test-' + str(uuid.uuid4()),
                          stdin_open=kwargs.get('stdin_open', True))
            return docker_client.containers.create(docker_image, **kwargs)

    return TestUtils()


# noinspection PyUnresolvedReferences
class ConfigWrapper:
    def __init__(self):
        self.__dict__['_orig_attrs'] = {}

    def __setattr__(self, attr, value):
        # Do not override the original value if already saved
        if attr not in self._orig_attrs:
            self._orig_attrs[attr] = getattr(hlbox_config, attr)
        setattr(hlbox_config, attr, value)

    def restore(self):
        for attr, value in self._orig_attrs.items():
            setattr(hlbox_config, attr, value)


@pytest.fixture
def config():
    """A fixture to override the config attributes which restores changes after
    the test run."""

    wrapper = ConfigWrapper()
    yield wrapper
    wrapper.restore()
