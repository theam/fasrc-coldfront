# syntax=docker/dockerfile:experimental

# to build for a development environment, run the following command:
# docker build --build-arg build_env=dev -t coldfront --ssh default . --network=host
FROM python:3.10-bookworm

ARG build_env=production
ENV BUILD_ENV=$build_env

LABEL org.opencontainers.image.source=https://github.com/fasrc/coldfront
LABEL org.opencontainers.image.description="fasrc coldfront application"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && apt-get install -y libreadline8 gosu vim\
     redis redis-server openssl\
    && apt-get install -y libsasl2-dev libldap2-dev libssl-dev \
    && apt-get install -y sssd sssd-tools supervisor \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir ~/.ssh && echo "Host git*\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config

WORKDIR /usr/src/app
COPY requirements.txt ./

### slurmenv-specific config ###
RUN groupadd -r munge
RUN useradd -r -u 998 -g munge -s /sbin/nologin -d /var/run/munge munge

COPY ./slurm_build /build
RUN /build/install.sh && rm -rf /build
COPY ./slurm_build/slurm.conf /etc/slurm/slurm.conf
COPY --chown=slurm:slurm ./slurm_build/slurmdbd.conf /etc/slurm/slurmdbd.conf
RUN chmod 600 /etc/slurm/slurmdbd.conf
# COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY ./slurm_build/pmlogger-supremm.config /etc/pcp/pmlogger/pmlogger-supremm.config
COPY ./slurm_build/slurm-prolog.sh /usr/local/bin/slurm-prolog.sh
COPY ./slurm_build/slurm-epilog.sh /usr/local/bin/slurm-epilog.sh
COPY ./slurm_build/submit_jobs.sh /usr/local/bin/submit_jobs.sh
COPY ./slurm_build/example_job.sbatch /usr/local/bin/example_job.sbatch
### end of slurmenv-specific config ###

ARG IPYTHON_STARTUP=/root/.ipython/profile_default/startup
RUN mkdir -p ${IPYTHON_STARTUP}
COPY etc/ipython_init.py ${IPYTHON_STARTUP}


RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN if [ "${BUILD_ENV}" = "dev" ]; then pip install django-redis django-debug-toolbar; fi

RUN pip install django-prometheus gunicorn mozilla_django_oidc

ENV PYTHONPATH /usr/src/app:/usr/src/app/ifxreport:/usr/src/app/ifxbilling:/usr/src/app/fiine.client:/usr/src/app/ifxurls:/usr/src/app/nanites.client:/usr/src/app/ifxuser:/usr/src/app/ifxmail.client:/usr/src/app/ifxec

RUN mkdir -p /usr/src/app/media/reports

EXPOSE 80
EXPOSE 25

CMD ["/bin/bash", "./container_startup.sh"]
