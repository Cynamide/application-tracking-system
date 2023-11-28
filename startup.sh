#! /bin/bash
# This setup file assumes you have pip and npm already installed, and that
# you are using this script from an already-cloned repository in the project root directory.

# Quick success/failure color function. Nothing particularly groundbreaking here
# $1 = exit code
# $2 = task attempted
exit_result () {
	if [[ $1 -eq 0 ]]
	then
		echo -e "\033[0;32m$2: Started\033[0m"
	else
		echo -e "\033[0;31m$2: Failure\033[0m"
		exit 1
	fi
}
echo -e "Navigating to backend..."
cd ./backend || exit
echo -e "Attempting to start backend..."
flask run &
exit_result $? "Backend boot"

echo -e "Navigating to frontend..."
cd ../frontend || exit
echo -e "Attempting to start frontend..."
yarn start &
echo -e "(Frontend takes some time to load, please be patient...)"
exit_result $? "Frontend boot"


