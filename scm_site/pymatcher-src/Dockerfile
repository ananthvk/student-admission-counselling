FROM python:3.12-alpine as builder

# Install required build tools
RUN apk add --no-cache build-base python3-dev meson cython

WORKDIR /app
COPY pymatcher-src ./
RUN pip wheel . -w /app/wheels
CMD ["echo", "Wheel built"]