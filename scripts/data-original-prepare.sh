#!/bin/sh
# ==============================================================================
#
#          FILE:  data-original-prepare.sh
#
#         USAGE:  ./scripts/data-original-prepare.sh
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - POSIX Shell or better
#                 - rsync
#                 - miller
#                   - See <https://github.com/johnkerl/miller>
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v1.0
#       CREATED:  2021-11-11 16:63 UTC started
# ==============================================================================
set -e

# PWD_NOW=$(pwd)
# TMP_DIR="tmp"
# DATA_DIR="data"
DATA_ORIGINAL_DIR="data/original"
DATA_ORIGINAL_GIT_DIR="tmp/original-git"

set -x
rsync --archive --verbose "${DATA_ORIGINAL_GIT_DIR}/data/" "$DATA_ORIGINAL_DIR/"
# set +x


#### terminology/facebook ______________________________________________________
### Copy
find "$DATA_ORIGINAL_DIR/terminologies/" -name 'f_*' -type f -exec cp "{}" "$DATA_ORIGINAL_DIR/terminology/facebook"  \;

## ls
ls "${DATA_ORIGINAL_DIR}"/terminology/facebook/

### Rename
# data/original/terminology/facebook/f_en-pt_XX.csv -> data/original/terminology/facebook/f-en-pt-XX.csv
for i in "${DATA_ORIGINAL_DIR}"/terminology/facebook/f_en-*; do
  mv "$i" "$(echo "$i" | sed "s/_/-/g")";
done

ls "${DATA_ORIGINAL_DIR}"/terminology/facebook/

# data/original/terminology/facebook/f-en-pt-XX.csv -> data/original/terminology/facebook/en_pt-XX.csv
for i in "${DATA_ORIGINAL_DIR}"/terminology/facebook/f-en-*; do
  mv "$i" "$(echo "$i" | sed "s/f-en-/en_/g")";
done

# data/original/terminology/facebook/en_pt-XX.csv-> data/original/terminology/facebook/en_pt.csv
for i in "${DATA_ORIGINAL_DIR}"/terminology/facebook/*-XX.csv; do
#   echo "$i" "$(echo "$i" | sed "s/-XX.csv/.csv/")";
  mv "$i" "$(echo "$i" | sed "s/-XX.csv/.csv/")";
done

# exit 1

## ls
ls "${DATA_ORIGINAL_DIR}"/terminology/facebook/

# echo "TODO: normalize _XX"

#### terminology/google ______________________________________________________

#### terminology/google ______________________________________________________
### Copy
find "$DATA_ORIGINAL_DIR/terminologies/" -name 'g_*' -type f -exec cp "{}" "$DATA_ORIGINAL_DIR/terminology/google"  \;

## ls
ls "${DATA_ORIGINAL_DIR}"/terminology/google/

### Rename

for i in "${DATA_ORIGINAL_DIR}"/terminology/google/g_*; do
#   echo "$i" "$(echo "$i" | sed "s/f_//")";
  mv "$i" "$(echo "$i" | sed "s/g_//")";
done

## ls
ls "${DATA_ORIGINAL_DIR}"/terminology/google/


#### validate __________________________________________________________________

# mlr --icsv check data/original/terminology/google/*.csv
# mlr --icsv check data/original/terminology/facebook/*.csv