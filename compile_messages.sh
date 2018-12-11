#!/bin/sh

sections=( {{ project_name | lower }} )

for section in "${sections[@]}"
do
	cd ${section}
	python ../manage.py compilemessages
	cd ..
done
