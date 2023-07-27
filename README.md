MARTA

# Automatic Text to 3D Animations System

## Quick Installation:

- First you're going to want to get an account with The Digital Research Alliance of Canada. If you are unable to set up this account, you will need access to a powerful graphics card such as an nvidia v100 gpu 32gb, or access to some similar company that can provide the RAM resources that are needed to generate all of the assets.

- Go to this website to learn more about The Digital Research Alliance of Canada and whether or not you're eligible to make an account: `https://alliancecan.ca/en`

- Once you have obtained an account, you will need to use the Cedar branch.

- Once you've been given access to this resource, you're going to need to sign in using this command: `[name@server ~]$ ssh -Y userid@cluster_name` except that you should place your user id in the userid slot and the `cedar` as the cluster name.

- Once you've given your password you should be in your compute canada account. From here you'll want to create a virtual environment using this command:  `python -m venv name_of_your_environment_here`

- You should now be able to activate your environment by typing in this command: `source name_of_environment/bin/activate`

- NOTE: If you ever want to leave your virtual environment simply type `deactivate`

- Next you'll want to run the requirements.txt file to install the needed dependencies for the project. This can be done with this command: `pip install -r requirements.txt`. Keep in mind that for this to work, you will need to cd into the correct folder. Note: it will take a while for the requirements page to install.
- Note: If you are getting errors after installing the requirement.txt page, you are goimg to have to install dependencies one by one. This can be accomplished by running the program and adding the dependencies that it says are missing in the errors. If you run `python nlpmain.py` and get module errors, this means that you are still missing some dependencies.

- Once the requirements page has installed, try running the nlpmain.py file with  `python nlpmain.py` if there are any missing packages install them with pip and try rerunning.
