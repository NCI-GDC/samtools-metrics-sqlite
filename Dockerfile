ARG REGISTRY=docker.osdc.io/ncigdc
ARG BASE_CONTAINER_VERSION=latest

FROM ${REGISTRY}/python3.9-builder:${BASE_CONTAINER_VERSION} as builder

COPY ./ /samtools_metrics_sqlite

WORKDIR /samtools_metrics_sqlite

RUN pip install tox && tox -e build

FROM ${REGISTRY}/python3.9:${BASE_CONTAINER_VERSION}

LABEL org.opencontainers.image.title="samtools_metrics_sqlite" \
      org.opencontainers.image.description="samtools-metrics-sqlite" \
      org.opencontainers.image.source="https://github.com/NCI-GDC/samtools-metrics-sqlite" \
      org.opencontainers.image.vendor="NCI GDC"

COPY --from=builder /samtools_metrics_sqlite/dist/*.whl /samtools_metrics_sqlite/
COPY requirements.txt /samtools_metrics_sqlite/

WORKDIR /samtools_metrics_sqlite

RUN pip install --no-deps -r requirements.txt \
	&& pip install --no-deps *.whl \
	&& rm -f *.whl requirements.txt

USER app

ENTRYPOINT ["python", "-m","samtools_metrics_sqlite"]

# CMD ["--help"]
