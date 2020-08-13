#!/bin/sh

var=$(identify ~/Desktop/Projects/PyGame/resource/frames/* | grep -v 16x16 | grep -Ev 'coin|weapon' | awk '{printf ("%5s\n", $1)}')

echo "$var" | while read -r line;
do
	cp "$line" "$HOME"/Desktop/TestConvert;
done
