# House-keeping cron job

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root@localhost

# REMOVE THE : BEFORE THE /usr/bin COMMAND TO ACTUALLY RUN THE JOB!
# Also adapt the arguments to the task at hand.
# Or simply remove this file.

# m h   dom mon dow   user        command
7 0     *   *   *     {{ cookiecutter.pypi_package }}      . /etc/default/{{ cookiecutter.pypi_package }} && : /usr/bin/{{ cookiecutter.pypi_package }} maintenance >/var/log/{{ cookiecutter.pypi_package }}/cron.log 2>&1
