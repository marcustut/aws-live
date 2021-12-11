#!/bin/bash

# install dev tools for build
sudo yum groupinstall "Development Tools" -y
sudo yum install openssl-devel libffi-devel -y

# install pyenv
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc

# install python 3.9.9
yes Y | pyenv install 3.9.9

# install pipenv
pip3 install pipenv

# install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
echo 'export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"' >> ~/.bashrc
echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm' >> ~/.bashrc
source ~/.bashrc
nvm install node

# install pnpm
npm install -g pnpm

# clone repo
# git clone https://github.com/marcustut/aws-live.git

# cd into repo
# cd aws-live

# install virtual env (pipenv)
yes Y | pipenv shell

# install dependencies
pipenv install && pipenv install --dev

# copy .env from bucket
aws s3 cp s3://marcuslee-aws-live-env/server.env .env
aws s3 cp s3://marcuslee-aws-live-env/client.env.local web/.env.local

# install web dependencies
cd web && pnpm i && pnpm build

# run prod server
cd .. && pipenv run python app.py

