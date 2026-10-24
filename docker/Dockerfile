FROM ros:jazzy-ros-base AS runtime

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ="UTC"
ARG USERNAME=trickfire
ARG USER_UID=1000
ARG USER_GID=1000

# --------------------------------------------------------------------------------------------
# apt sandbox: on some Docker Desktop / kernel combos the unprivileged `_apt` user cannot verify
# repository signatures ("At least one invalid signature was encountered"). Builds run as root
# anyway, so disable the privilege drop.
# --------------------------------------------------------------------------------------------
RUN echo 'APT::Sandbox::User "root";' > /etc/apt/apt.conf.d/10-no-sandbox

# --------------------------------------------------------------------------------------------
# Locale + timezone
# --------------------------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install --no-install-recommends -y locales tzdata && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8

RUN ln -snf "/usr/share/zoneinfo/${TZ}" /etc/localtime && \
    echo "${TZ}" > /etc/timezone

# --------------------------------------------------------------------------------------------
# Build + test toolchain, driven by deps.txt. Editing it invalidates this layer.
# --------------------------------------------------------------------------------------------
COPY docker/deps.txt /tmp/deps.txt

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        $(tr -d '\r' < /tmp/deps.txt | grep -vE '^[[:space:]]*(#|$)') \
        sudo \
        git \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------------------------------
# User. The base image ships an `ubuntu` user at uid 1000; replace it so bind-mounted files
# are owned by the host user on Linux (override with --build-arg USER_UID=...).
# --------------------------------------------------------------------------------------------
RUN (userdel -r ubuntu 2>/dev/null || true) && \
    groupadd --gid "${USER_GID}" "${USERNAME}" && \
    useradd --uid "${USER_UID}" --gid "${USER_GID}" --shell /bin/bash --create-home --no-log-init "${USERNAME}" && \
    usermod -aG video "${USERNAME}" && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/user && \
    chmod 0440 /etc/sudoers.d/user

COPY docker/container.bashrc /home/${USERNAME}/.bashrc
RUN sed -i 's/\r$//' /home/${USERNAME}/.bashrc && chown ${USERNAME}:${USER_GID} /home/${USERNAME}/.bashrc

USER ${USERNAME}
WORKDIR /home/${USERNAME}/cpp-workshop

# --------------------------------------------------------------------------------------------
# DEV - adds editor/formatting tooling on top of runtime (devcontainer)
# --------------------------------------------------------------------------------------------
FROM runtime AS dev

USER root

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        clangd \
        clang-format \
        gdb \
        shellcheck \
        shfmt \
        python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --break-system-packages ruff

USER ${USERNAME}
