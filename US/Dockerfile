FROM python:3.5

RUN apt-get update \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN groupadd -g 799 liondon && \
    useradd -r -u 999 -g liondon liondon

# Set up a working folder and install the pre-reqs
WORKDIR /app

RUN pip install Flask \
  && pip install requests

USER liondon

COPY --chown=liondon:liondon . .

CMD [ "python", "./user.py" ]

