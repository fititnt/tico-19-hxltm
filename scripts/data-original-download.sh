#!/bin/sh
# ==============================================================================
#
#          FILE:  data-original-download.sh
#
#         USAGE:  ./scripts/data-original-download.sh
#
#   DESCRIPTION:  Downloads https://github.com/tico-19/tico-19.github.io/ to
#                 tmp/original-git
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v1.0
#       CREATED:  2021-11-11 15:25 UTC started
# ==============================================================================

set -e

TMP_DIR="tmp"
DATA_DIR="data"
DATA_ORIGINAL_DIR="data/original"
DATA_ORIGINAL_GIT_DIR="tmp/original-git"

if [ ! -d "$TMP_DIR" ]; then
    mkdir "$TMP_DIR"
fi

# wget https://github.com/tico-19/tico-19.github.io/archive/refs/heads/master.zip

# if [ ! -f ${TMP_DIR}/tico-19.github.io.zip ]; then
#   curl -L "https://github.com/tico-19/tico-19.github.io/archive/refs/heads/master.zip" \
#     --output "${TMP_DIR}/tico-19.github.io.zip"
# fi

if [ ! -d "$DATA_ORIGINAL_GIT_DIR" ]; then
    git clone --depth 1 https://github.com/tico-19/tico-19.github.io "$DATA_ORIGINAL_GIT_DIR"
else
    echo "Already cloned. Skipping..."
fi
# unzip "${TMP_DIR}/tico-19.github.io.zip" -d "$TMP_DIR"

