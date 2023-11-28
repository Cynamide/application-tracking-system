# /bin/bash
# This setup file assumes you have pip and npm already installed, and that
# you are using this script from an already-cloned repository in the project root directory.

# Quick success/failure color function. Nothing particularly groundbreaking here
# $1 = exit code
# $2 = task attempted
exit_result () {
	if [[ $1 -eq 0 ]]
	then
		echo -e "\033[0;32m$2: Success\033[0m"
	else
		echo -e "\033[0;31m$2: Failure\033[0m"
		exit 1
	fi
}

echo -e "Navigating to frontend directory..."
cd ./frontend || exit
echo -e "Attempting to install NPM packages..."
npm install
exit_result $? "NPM package installation"
virtualenv venv
source venv/bin/activate
echo -e "Verifying pip installation..."
pip -V
exit_result $? "pip installation check"
echo -e "Returning to project root directory"
cd ../ || exit
echo -e "Installing required pip packages from requirements.txt..."
pip install -r ./requirements.txt
exit_result $? "pip package installation"
