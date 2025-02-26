FROM ubccr/hpcts:slurm-2023.07
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY base.config /build/base.config
COPY install.sh /build/install.sh
COPY slurm.conf /etc/slurm/slurm.conf
COPY submit_jobs.sh /usr/local/bin/submit_jobs.sh
COPY example_job.sbatch /usr/local/bin/example_job.sbatch
RUN /build/install.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["frontend"]
