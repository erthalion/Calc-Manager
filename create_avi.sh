#!/bin/bash
mencoder $1 -mf fps=25 -o $2 -ovc lavc -lavcopts vcodec=mpeg4
