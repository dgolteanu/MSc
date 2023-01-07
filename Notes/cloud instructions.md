---
output:
  pdf_document: default
  html_document: default
---
## For those who have never used a terminal or command line interface
A few basics: there is no mouse input, only keyboard navigation, spaces have meaning when writing and executing (running) commands (programs).  
Mac users need only to open the "Terminal" app, for windows users please download "MobaXTerm" https://mobaxterm.mobatek.net/download.html  
For first time users I'd recommend MobaXTerm and associated windows instructions **even for Mac** as it makes file transfers to and from servers easier.

You will need some basic concepts of filesystem structure and commands for navigation, the best beginner resource I've found
is listed here, please carefully read from the beginning up to "Miscellaneous", if you get to the "Intermediate" section you've gone too far :) 
https://dev.to/awwsmm/101-bash-commands-and-tips-for-beginners-to-experts-30je#toc  

The concept of a file path and filesystem directory structure are very important to understand for using the CLI.

### Tab key is used to autocomplete, this is strongly recommended to fill in paths and filenames. Before you finish typing out each part of a file path (before each /) hit tab once to autocomplete, it will try to autocomplete based on the letters already typed, if in your current location (directory) multiple files or directories match the partially typed input it will list all matches, you should continue typing until your desired file or directory name until it's the only option and will autocomplete. Note: directories will complete with a / at the end while files will not, if you want to see all files/directories without typing anything just hit tab twice.

# Step 1: generate a SSH (secure shell) key pair
SSH keys are a pair of private-public cryptographic keys used to identify yourself online instead of passwords, they're required to connect to the cloud server where you will be running mldsp from the command line interface (CLI). Keys are specific to you/the compter used to generate them, do not share/send your private key, only use it with ssh related commands.

## Follow the instructions  
* For Mac & Linux users: https://docs.alliancecan.ca/wiki/Using_SSH_keys_in_Linux 
    * Follow **ONLY Step 1: Creating a key pair **
    * You must set a password for your keys, do not leave blank
    * Admin will have to do Step 2 onwards (installing public key)
    * **Send the admin your PUBLIC key ONLY (the one with .pub )**
* For Windows users: https://docs.alliancecan.ca/wiki/Generating_SSH_keys_in_Windows
    * Please use MobaXTerm not PUTTY
    * Follow **ONLY Section 1: Creating a key pair**
    * You must set a password for your keys, do not leave blank
    * Between step 3 & 4, please copy and send the admin this version of your public key: ![](/Users/dolteanu/local_documents/Coding/MSc_github/Notes/mobaXterm_public_key_fig.png)
    * Use the buttons to save the pulic and private keys in the same folder (actually on your computer, NOT onedrive, google drive, iCloud etc.)
    * For step 5 under Section 1 make sure you only have .pub extension, and not .ppk autofilled for your public key file


# Step 2: Find your IP address and send it to the admin
## Go to this site: https://nordvpn.com/what-is-my-ip/ 
Your home IP address will most likely change every few days/weeks (dynamic IP, provided by your internet company), if you get a similar error after previously successfully connecting to the server:
``` dolteanu@199.241.167.26: Permission denied (publickey)``` It's likely your internet company changed your IP address. Every time you connect to a new internet connection your IP will be unique and will need to be sent to the admin, campus IP addresses are relatively stable.

# Step 3 Log into the server (finally)
## Windows users
Follow instructions:[ https://docs.alliancecan.ca/wiki/Connecting_with_MobaXTerm#Using_a_Key_Pair](https://docs.alliancecan.ca/wiki/Connecting_with_MobaXTerm#Using_a_Key_Pair)

For remote host field put: **199.241.167.26**

Do select 'specify username' for windows users we'll fill in your uwo user ID

For Mac users following along with MobaXTerm to make your life easier we'll want to use the same username as your mac, this can be found by opening Terminal; hitting enter (a few times) you will see copies of a command prompt appear, this includes your computer name separated by ':', current location (e.g. '%' or '/' or 'Desktop'), and username followed by \$ after which you can start typing commands which are run by hitting the enter key.

Example from my mac `Hotcakes:~ dolteanu$` in this case my username is dolteanu. 

Do select the use private key box, and select the private key file from where you saved it in Step 2  


After hitting OK, you'll be taken back to the main window with a terminal taking up most of the MobaXterm window. It should prompt you to enter your ssh key password, note when you type the password the command prompt will remain blank this is a security feature, you must trust the password is being typed and hit enter after to connect to the server.  


If you've sucessfully conected, you'll see a welcome message appear and at the last line, the command prompt header has changed to `username@lab-members:~$ ` with your username. You are now in the server!  
To exit the server run the `exit` command

## Mac/Linux users
Run these commands from your terminal:  
`cd ~/.ssh`  
`ssh -i ~/.ssh/my_private_key username@199.241.167.26` change the private key name from 'my_private_key' to your key's actual name, remember if it's not tab autocompleting, you're probably not in the location (directory) you think you're in, or that file/directory doesn't exists (at least where you're looking).  

You'll know the command is sucessful when it asks for your ssh key password, note when you type the password the command prompt will remain blank this is a security feature, you must trust the password is being typed and hit enter after to connect to the server.  
If you've sucessfully conected, you'll see a welcome message appear and at the last line the command prompt header changed to `username@lab-members:~$ ` with your username. You are now in the server your terminal app is not showing you your local mac but rather only the server!  
To exit the server run the `exit` command, your terminal is back to showing you your local mac.

# Step 4 upload your data 
For MLDSP CLI you will need the same format as the website, except not zipped. 1 parent folder (directory) with 1 file named `metadata.csv` this should have 2 columns with no headers. First the sample names matching the fasta headers (everything after the '>' in the first line of each sample within your fasta). Second column is the unique class label to use for classification. Neither columns can have spaces or special characters.  
In the parent directory the fasta file(s) should be inside a folder (directory) named 'fastas'. The parent folder containing all the aforementioned is what you will upload to the server. Note: all samples present in your fasta must be present in the metadata.csv (inverse not true, those non-existent samples listed in your metadata will simply be ignored). 

## MAC/linux
On your local machine, not server (remember what your terminal is showing/whether you're logged into the server) navigate to the directory containing your data folder, it does not need to be zipped.  

Run the following command changing the private key name and username to yours. The path/data_folder should be changed to whatever your data directory location/name is for you.  
`scp -i ~/.ssh/my_private_key -r path/data_folder/ username@199.241.167.26:~` This will send the data directory to your home directory on the server, you cannot close the terminal/computer until the transfer is done

## Windows
Left side menu in MobaXTerm shows your current files & directories in your home directory on the server, use the menu buttons to upload/download from your computer to the server

# Step 5 Running MLDSP CLI
**Mac users make sure you've logged back into the server after doing your data transfer**  

Detailed steps and command line arguments are described in the MLDSP Readme.md, briefly the command to run MLDSP:
`MLDSP parent_directory/fastas/ parent_directory/metadata.csv -r Desired_run_name -k k_value` where the parent_directory will need to be replaced with the path to your data folder, also replace the desired run name (no spaces) and provide a number for  the cgr k value.

Once the program is running you cannot close the terminal window or your computer until you see it says DONE, mldsp will generate a Results directory with a folder of your run name containing results. The `Training_Run_{Run name}.log` contains the main results with Images folder hosting a cgr image (with 1 cgr per class), MoDMap, and confusion matrices (1 per classifier).