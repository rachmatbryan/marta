MARTA

# Automatic Text to 3D Animations System

## Quick Installation:

- First you're going to want to get a Compute Canada account. If you are unable to set up this account, you will need access to a powerful graphics card, and even with a card you may not be able to run the system as it runs with ___________________ memory...

- Go to this website to learn more about The Digital Research Alliance of Canada and whether or not you're eligible to make an account: `https://alliancecan.ca/en`

- Keep in mind you will need to use the Cedar branch.

- Once you've been given access to this resource, you're going to need to sign in using this command: `[name@server ~]$ ssh -Y userid@cluster_name` except that you should place your user id in the userid slot and the `cedar` as the cluster name.

- Once you've given your password you should be in your compute canada account. From here you'll want to create a virtual environment using this command:  `python -m venv name_of_your_environment_here`

- You should now be able to activate your environment by typing in this command: `source name_of_environment/bin/activate`

- NOTE: If you ever want to leave your virtual environment simply type `deactivate`

- Next you'll want to run the requirements.txt file to install the needed dependencies for the project. This can be done with this command: `pip install -r requirements.txt`. Keep in mind that for this to work, you will need to be cd'd into the correct folder. Note: it will take a while for the requirements page to install.

- Once the requirements page has installed, try running the nlpmain.py file with  `python nlpmain.py` if there are any missing packages install them with pip and try rerunning.







# MAYBE WE SHOULD ADD THIS SECTION IN LATER?

## Step By Step Installation Guide:

### Step One: Set up an account with Compute Canada (now called: Digital Research Alliance of Canada)

- If you are unable to set up this account, you will need access to a powerful graphics card, and even with a card you may not be able to run the system as it runs with ___________________ memory...

- Go to this website to learn more about The Digital Research Alliance of Canada and whether or not you're eligible to make an account: `https://alliancecan.ca/en`

- Keep in mind you will need to use the Cedar branch

### Step Two: Log into your account on Compute Canada, and begin loading the proper modules.

- In order to log into compute canada in your terminal or VSCode, you should use this repository made by pashazgit: `https://github.com/pashazgit/ComputeCanada-Wiki`

- Once you're onto your compute canada within your terminal you should create a virtual environment as described by pashazgit's repo. When in said environment the first thing you want to do is check your python version by typing: `python --version` in your terminal. It is likely that your environment will have the most recent version of python, but for our code to work we need to use python 3.9.6. In order to change your python version simply type `module load python/3.9.6`. You should get no response in the terminal, but if you type `module list` you should see all of your currently loaded modules as well as python 3.9.6. If you get errors after typing the module load command, then you should try `module spider python/3.9.6` and follow the instructions in lays out.

- Next, download `spacy` using these commands:

    a. `pip install -U pip setuptools wheel`

    b. `pip install -U spacy`

    c. `python -m spacy download en_core_web_sm`

- Next, 
