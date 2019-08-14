#!/usr/bin/env bash -eu

for name in $(ls); do
    if [[ -d "$name" ]]; then
        cd $name
        if [[ ! -e "graph.mp4" ]] || [[ ! -e "data.csv" ]]; then
            echo $name
        fi
    fi
done
