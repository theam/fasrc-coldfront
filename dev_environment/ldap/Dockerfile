FROM --platform=linux/amd64 osixia/openldap:1.5.0 AS stage-amd64

FROM --platform=linux/arm64/v8 osixia/openldap:1.5.0 AS stage-arm64

ARG TARGETARCH

FROM stage-${TARGETARCH} AS final
USER root
COPY . /build
RUN chown -R root:root /build
RUN chmod 777 /build/install.sh
RUN /build/install.sh && rm -rf /build
