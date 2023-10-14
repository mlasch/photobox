#/usr/bin/env bash

SCRIPT_NAME=$(basename "$0")
DIR_NAME=$(dirname "$0")
HELP_MSG="Usage: $SCRIPT_NAME <OPTIONS>...
Mock gphoto2 command with the following options
  --delete-all-files
  --trigger-capture
  --get-all-files
  -R
"

function usage() {
  echo $HELP_MSG
  exit $1
}

function delete_all_files() {
  echo "Delete all"
}

function trigger_capture() {
  echo "Trigger"
  sleep 2
}

function get_all_files() {
  echo "Get files"
  cp $DIR_NAME/../distfiles/demo.jpg $(pwd)/IMG_1234.jpg
}

if ! PARSED_OPTS=$(getopt -o R -l folder: -l delete-all-files -l trigger-capture -l get-all-files --name $SCRIPT_NAME -- "$@"); then
  usage 1
fi

eval set -- "$PARSED_OPTS"

while true; do
  case "$1" in
    --folder)
      FOLDER=$2
      shift 2
      ;;
    --delete-all-files)
      delete_all_files
      shift 1
      ;;
    --trigger-capture)
      trigger_capture
      shift 1
      ;;
    --get-all-files)
      get_all_files
      shift 1
      ;;
    -R)
      shift 1
      ;;
    --)
      shift
      break;
      ;;
    *)
      echo "Error: args parsing failed"
      exit 1
      ;;
  esac
done
