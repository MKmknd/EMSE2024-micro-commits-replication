#!/bin/sh

echo "clone studied repositories"
rm -rf ./repository
mkdir ./repository

rm -rf ./cregit_repository
mkdir ./cregit_repository

cd prepare_dataset

project_name_list=(
    "apache/camel"
    "apache/hadoop"
    "torvalds/linux"
    "zephyrproject-rtos/zephyr"
)

for p_name in "${project_name_list[@]}" ; do

	git clone https://github.com/${p_name}.git
	sleep 1
done

