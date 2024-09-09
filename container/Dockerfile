ARG VARIANT=3
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp


   ARG VARIANT="16"
   FROM mcr.microsoft.com/devcontainers/javascript-node:1-${VARIANT}
   
   RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
       && apt-get -y install --no-install-recommends bundler
   
   # [Optional] Uncomment if you want to install an additional version
   #  of node using nvm
   # ARG EXTRA_NODE_VERSION=18
   # RUN su node -c "source /usr/local/share/nvm/nvm.sh \
   #    && nvm install ${EXTRA_NODE_VERSION}"
   
   COPY ./script-in-your-repo.sh /tmp/scripts/script-in-codespace.sh
   RUN apt-get update && bash /tmp/scripts/script-in-codespace.sh
   
