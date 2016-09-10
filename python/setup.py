from distutils.core import setup
setup(
    name='raspi_server',
    version='0.0',
    packages=['raspi_server', 'raspi_server.slack_plugins', 'raspi_server.tasks'],
    scripts=['bin/run_raspi_server.py']
    )
