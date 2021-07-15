#!/bin/bash

textx generate model/*.item --overwrite --target python --output-path src-gen/python || exit 1

