FROM python:3-alpine AS base

RUN apk add --no-cache tini
RUN addgroup -S app && adduser -S -G app app
USER app
RUN mkdir /home/app/workdir
WORKDIR /home/app/workdir

COPY --chown=app:app requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt
ENV FLASK_APP app.server
CMD [ "python", "-m", "flask", "run", "--host", "0.0.0.0", "--no-debugger" ]

FROM base
COPY --chown=app:app . .
ENTRYPOINT ["/sbin/tini", "--"]
CMD [ "/home/app/.local/bin/waitress-serve", "--port", "5000", "--call", "app.server:create_app" ]
