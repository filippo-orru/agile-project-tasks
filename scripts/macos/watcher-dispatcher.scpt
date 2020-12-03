#!/bin/osascript
on run argv
    set dir to quoted form of (first item of argv)
    tell app "Terminal" to do script "cd " & dir & "; bash scripts/macos/index-watcher.sh & bash scripts/macos/add_task-watcher.sh & bash scripts/macos/print-watcher.sh"
end run
