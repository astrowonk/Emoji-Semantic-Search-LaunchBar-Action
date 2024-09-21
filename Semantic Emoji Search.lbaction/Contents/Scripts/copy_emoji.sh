#!/bin/bash

mycommand="/usr/bin/osascript -e 'tell app \"LaunchBar\" to paste in frontmost application \"$1\"'"

eval $mycommand
