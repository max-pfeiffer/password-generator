# Using an official image is a good practice. Here I use also the smallest
# image available to reduce the amount of security vulnerabilities, the size
# on disk, and the installed libraries count.
# See: https://snyk.io/advisor/docker/python/3.9.15-slim-bullseye
# Pinning the image using the image digest gives very predictive builds,
# because the image digest uniquely and immutably identifies a container image.
FROM python:3.9.15-slim-bullseye@sha256:9ef969a374118f28a61261e2b018a7f9debcc0dc1342481bd8b8693c1457f46d as dependencies-build-stage

WORKDIR /usr/application

COPY ./requirements.txt /usr/application/

# Only install/build the dependencies for the production image. We save build
# time that way, reduce size and security risks.
RUN python -m venv .venv
RUN . /usr/application/.venv/bin/activate && pip install -r requirements.txt

FROM python:3.9.15-slim-bullseye@sha256:9ef969a374118f28a61261e2b018a7f9debcc0dc1342481bd8b8693c1457f46d as production-image
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/usr/application

# Principle of least privilege: create a new user for running the application
RUN groupadd -g 1001 python_application && \
    useradd -r -u 1001 -g python_application python_application

RUN mkdir /usr/application && chown python_application:python_application /usr/application
WORKDIR /usr/application

# Seperate dependencies from the application code. This way we make use of
# Docker build cache. Application code changes don't trigger a dependency
# build.
COPY --chown=python_application:python_application --from=dependencies-build-stage /usr/application/.venv /usr/application/.venv

# Copy application files
COPY --chown=python_application:python_application /app /usr/application/app/
RUN chmod +x app/start_uvicorn.sh

# Document the exposed port which was configured in start_uvicorn.sh
EXPOSE 8000

# Use the unpriveledged user to run the application
USER 1001
CMD ["/usr/application/app/start_uvicorn.sh"]
