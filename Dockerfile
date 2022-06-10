# Multi-stage build

# Global build arguments:

# define the installation paths
ARG SOURCE_PATH="/usr/local/src"
ARG OPENSSL_LIB_PATH="/usr/local/ssl"

# liboqs build type variant; maximum portability of image:
ARG LIBOQS_BUILD_DEFINES="-DOQS_DIST_BUILD=ON"

# openssl build defines (https://github.com/open-quantum-safe/openssl#build-options)
ARG OPENSSL_BUILD_DEFINES="-DOQS_DEFAULT_GROUPS=kyber512"

# define the QSC key exchange algorithm
ARG KEM_ALG="kyber512"

# define the QSC signature algorithm used for the certificates
ARG SIG_ALG="dilithium2"

# define IP addresses or Domain Name
ARG BROKER_IP=localhost
ARG PUB_IP=localhost

# First stage: the full build image:

FROM debian:buster AS builder
# FROM ubuntu:20.04 AS builder

# Set timezone
ENV TZ=Asia/Taipei
ENV DEBIAN_FRONTEND=noninteractive

# Copy files from the local storage to a destination in the Docker image
WORKDIR /
RUN mkdir test
ADD kem_list.txt /test
RUN chmod 777 /test/* && sed -i 's/\r//' /test/*

ARG SOURCE_PATH
ARG OPENSSL_LIB_PATH
ARG LIBOQS_BUILD_DEFINES
ARG OPENSSL_BUILD_DEFINES
ARG KEM_ALG

# Update image and install all prerequisites
# RUN apt-get update && apt-get install build-essential vim cmake gcc libtool libssl-dev make ninja-build git doxygen \
#         libcjson1 libcjson-dev uthash-dev libcunit1-dev libsqlite3-dev xsltproc docbook-xsl -y && apt-get clean

RUN apt-get update && apt-get install -y build-essential vim cmake gcc libtool libssl-dev make ninja-build git 

RUN apt-get install -y doxygen libcjson1 libcjson-dev uthash-dev libcunit1-dev libsqlite3-dev xsltproc docbook-xsl

# Get the fork of OQS-OpenSSL_1_1_1-stable
WORKDIR $SOURCE_PATH
RUN git clone --depth 1 --branch OQS-OpenSSL_1_1_1-stable https://github.com/open-quantum-safe/openssl.git OQS-OpenSSL

# Get and build liboqs, then install it into a subdirectory inside the OQS-OpenSSL folder
RUN git clone --depth 1 --branch main https://github.com/open-quantum-safe/liboqs.git liboqs && \
    cd liboqs && mkdir build && cd build && \
    cmake -GNinja $LIBOQS_BUILD_DEFINES -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=$SOURCE_PATH/OQS-OpenSSL/oqs .. && \
    ninja && ninja install && echo "liboqs installed successfully" || exit 1

# Build and install OQS-OpenSSL_1_1_1-stable
WORKDIR $SOURCE_PATH/OQS-OpenSSL
## OS type: x86_64, aarch64
# RUN ./Configure shared linux-x86_64 -lm --prefix=$OPENSSL_LIB_PATH/ \
#         --openssldir=$OPENSSL_LIB_PATH/ $OPENSSL_BUILD_DEFINES
RUN ./Configure shared no-asm linux-aarch64 -lm --prefix=$OPENSSL_LIB_PATH/ \
        --openssldir=$OPENSSL_LIB_PATH/ $OPENSSL_BUILD_DEFINES

# Let Mosquitto Client to support KEM algorithm
RUN CP=`grep "\/\* $KEM_ALG \*\/" /test/kem_list.txt | awk '{print $1}'` && \
    sed -i '/static const uint16_t eccurves_default/a\    '$CP'                      \/\* '$KEM_ALG' \*\/' ssl/t1_lib.c && \
    make -j$(nproc) && make install && echo "OQS-OpenSSL installed successfully" || exit 1

# Build and install Mosquitto
WORKDIR $SOURCE_PATH
RUN git clone -b master https://github.com/eclipse/mosquitto.git mosquitto && cd mosquitto && \
    make -j$(nproc) && make install && echo "Mosquitto installed successfully" || exit 1


# Second stage: Only create minimal image:

FROM debian:buster
# FROM ubuntu:20.04

ARG OPENSSL_LIB_PATH
ARG SIG_ALG
ENV SIG_ALG=${SIG_ALG}
ARG BROKER_IP
ENV BROKER_IP=34.215.240.96
ARG PUB_IP
ENV PUB_IP=60.250.153.181

## ------ Original Setting ------
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-rpi.gpio \
    libtiff5-dev \ 
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libfreetype6-dev \ 
    liblcms2-dev \ 
    libwebp-dev \
    python3-setuptools \
    iputils-ping
#--no-install-recommends

RUN pip3 install --no-binary Pillow requests
RUN pip3 install Adafruit_SSD1306 pyserial
RUN pip3 install Pillow

# Set the TLS_DEFAULT_GROUPS environment variable to permit selection of QSC KEMs(https://github.com/open-quantum-safe/openssl#build-options)
ENV TLS_DEFAULT_GROUPS="kyber512"

# Only keep the necessary library contents in the final image
# OQS-OpenSSL
COPY --from=builder $OPENSSL_LIB_PATH  $OPENSSL_LIB_PATH
# Mosquitto
COPY --from=builder /usr/local/lib  /usr/local/lib
COPY --from=builder /usr/local/bin  /usr/local/bin
COPY --from=builder /usr/local/sbin  /usr/local/sbin
COPY --from=builder /usr/lib/arm-linux-gnueabihf/libcjson.so.1 /usr/lib/arm-linux-gnueabihf

# Dynamically link to mosquitto
RUN ln -s /usr/local/lib/libmosquitto.so.1 /usr/lib/libmosquitto.so.1 && ldconfig

# Dynamically link to OQS-OpenSSL library
ENV LD_LIBRARY_PATH=$OPENSSL_LIB_PATH/lib

# Set path 
ENV PATH="/usr/local/bin:/usr/local/sbin:$OPENSSL_LIB_PATH/bin:$PATH"

# MQTTS port 
EXPOSE 8883

RUN mkdir /home/MAPS6_MVP
RUN mkdir /mnt/SD
RUN mkdir /mnt/USB

COPY . /home/MAPS6_MVP/
COPY NotoSans-Medium.ttf /home/

WORKDIR /home/MAPS6_MVP

CMD python3 PI_test.py

STOPSIGNAL SIGTERM