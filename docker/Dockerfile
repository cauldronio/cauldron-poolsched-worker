# The container produced with this file contains all GrimoireLab libraries and executables.
# It is configured for getting tasks from a database and running them
# Build this container from the root of the repository

FROM cauldronio/grimoirelab:0.2.63-py3.8

ENV CODE_WORKER /code

USER root

RUN apt-get update && apt-get install -y default-libmysqlclient-dev

# Add code from src folder
ADD . ${CODE_WORKER}
WORKDIR ${CODE_WORKER}
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Install requirements
RUN pip install -q -r requirements.txt

RUN mkdir -p /job_logs
RUN mkdir -p /spdx_files
RUN mkdir -p /git_repositories
RUN mkdir -p /static_files
RUN chown grimoirelab /job_logs
RUN chown grimoirelab /spdx_files
RUN chown grimoirelab /git_repositories
RUN chown grimoirelab /static_files

VOLUME ["/job_logs"]
VOLUME ["/spdx_files"]
VOLUME ["/git_repositories"]
VOLUME ["/static_files"]

USER grimoirelab

ENTRYPOINT ["/entrypoint.sh"]
