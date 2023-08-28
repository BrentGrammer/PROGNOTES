# GIT

Good site with quick cheatsheet info: http://rogerdudler.github.io/git-guide/

good book pro git book by Scott Chacon

great youtube channel with git tutorial by David Mahler: https://www.youtube.com/watch?v=uR6G2v_WsRA

-Used for version control and to save and store snapshots of versions of code.  
-Code can be uploaded (pushed) to repositories like GitHub where other developers can access and work on it.

INSTALLING:

http://git-scm.com/download/
download the installer, comes with gitbash (use this) which is a command line tool (can be used over the standard command line in windows, similar to linux).

Note: you can use git on either the windows command line or with gitbash command line tool (recommended), it works in both.

To start GitBash, right click anywhere in a folder or desktop and select GitBash here option in the context menu. This makes that location the local repository.

Notes from meetup:

Fork: Creates a repository in your github account and links it to the forked repository.

Clone: copy on your local machine

$ git diff - shows what has changed

---

Undoing a change:

-git log to get hashes of commits with their messages.

$ git reset [hash for commit - see your msg to identify] - to revert changes from a point in history

---

COMMANDS:

Main Commands:

$ git init -

starts a local repository and creates a folder for it on your computer. creates a .git folder which is hidden by default (usually don't need to go into this folder)

$ git add <file> - adds files to a staging area of the index, and makes them ready for a commit.

$ git status - used to see what you have in the staging area which is ready for commit.

$ git commit - takes everything that's in the staging area index and sends it to the local repository (i.e. on your computer).

$ git push - takes the local repository and pushes it to a remote repository (like github).

$ git pull - pull the latest file/version from the remote repository (github).

$ git clone - pulls an entire project (all files, not just the latest) or module from the remote repository to your local repository.

$ touch [filename] (ex: touch index.html) <--- this creates a file.

---

OTHER COMMANDS:

GIT IGNORE <---USED IF YOU DON'T WANT SOMETHING INCLUDED (even if you use add ., it will skip and ignore these files -- usually log.txt log files, for example.).

-Create a .gitignore file with the command $ touch .gitignore
-in the .gitignore file, simply type the name of the file(s) you want to ignore (i.e. log.txt, etc.) --git will then exclude these files from future commands.

Note: you can also ignore entire directories/folders (use the forward slash, and then type the name of the folder: /dirName)
Ex: in .gitignore file, type: /directoryName (/jsfolder) etc.

-can also ignore entire types of files with _.fileExt (ex: _.txt <---this ignores all txt files).

IGNORING FOLDERS/FILES:

/images
That will ignore any file OR directory named images in the same directory as the gitignore file you are using.

If you want to specify that it should only match the images directory then add the trailing slash:

/images/

---

Misc Commands:

$ clear <---clears the content of the window to clean it up.

---

======================================================================

TO USE:

Note: Start your project or work from the local repository and don't edit on gitHub - do all editing locally to keep histories from not synching.

1. Initialize the current working folder as a repository:
   $ git init --this initializes the current folder. A .git folder is created in the directory (it is hidden by default)

2. set up your username and email:
   $ git config --global user.name 'Firstname Lastname' <--insert your name here

$ git config --global user.email 'email@email.com' <--your email

3. Add the file(s) to your local repository (staging area):
   $ git add [filename] <---Ex: git add index.html

-To check what file(s) are in the staging area, use $ git status command.

-If you want to remove a file from the staging area: $ git rm --cached [filename] <----Ex: git rm --cached index.html (this removes index.html from the staging area.
also: git reset filename.txt
Will remove a file named filename.txt from the current index, the "about to be committed" area, without changing anything else.
To undo git add . use git reset (no dot).

-To add files of the same type: use _. ($ git add --cached _.html)

-To add everything to the staging area: use . ($ git add --cached .)

Note: if a file is modified and saved after being put in the staging area, it will be removed and you will be notified that it has been modified - you then need to re add it to the staging area.

4. COMMIT the file(s):
   $ git commit  
   or
   $ git commit -m 'comment goes here' <---this is faster and better

SHORTCUT TO STAGE AND COMMIT THE FILE(S):
$ git commit -a -m 'comment goes here'

// \*\*\*the -a flag can be used as a shortcut so you can skip git add . if the files you're trying to add are only modified and not new!

also can be combined to be $ git commit -am 'message'

**_This opens up the VIM editor by default. You need to press 'i' on the keyboard to enter insert mode to be able to type!_**
Type your comment ('initial commit' for ex.), then press ESCAPE to get out of insert mode, then type in :wq and ENTER to quit.

If VIM doesn't pop up then write your message and save and quit the editor.

-All files will be removed from the staging area and repository after being committed.

\*\*\*SHORTER WAY TO COMMIT:
$ git commit -m 'comment goes here' <---use the -m option and add the comment afterwords in quote marks -- this skips the editing step with the editor.

or

$ git commit -am 'message'

// this is using the -a and -m flag together to skip git add

---

GITHUB -- CREATE A REMOTE REPOSITORY:

1. CREATE A REMOTE REPOSITORY:

go to github and login, then select the + menu on the top right and create a new repository.
-after creation, for the project you should add a README.md file to describe the application (the extension stands for 'mark down' - and formats it a certain way).  
-the instructions are for steps to take in the command line initially (you may already have done some of them if you have a local repository set up).

Skip to the git remote add origin (as instructed on the repository webpage):
git
$ git remote add origin https://github.com/BrentGrammer/sample.git instruction and copy and paste that into the command line in gitBash.

2. PUSH THE FILES TO THE REMOTE REPOSITORY IN GITBASH:

input: $ git push -u origin master (as instructed on the remote repository webpage) <---this pushes the project to the master branch on the remote repository (it will ask you to log in to github first).

Create a README.md with $ touch README.md in GitBash (look up the syntax of markdown online for the formatting here: https://guides.github.com/features/mastering-markdown/).  
re
-Add the new file (in this case readme.md) to the staging area and commit it to the local repository.

-Send the commit to the remite repository:
$ git push

Note: use $ git remote command to test if there is a remote repository connected (it will return 'origin' in the command prompt).

---

TO CLONE OR DOWNLOAD THE PROJECT FROM GITHUB:

-Go to the top right on the app page in github and click Clone or Download button. You get a link.

-copy the link location, and in GitBash use the clone command:
$ git clone [paste the link here]

ex: $ git clone https://github.com/BrentGrammer/sample.git

-a new folder is created and all of the contents of the project are downloaded to it.

---

IF CHANGES ARE MADE BY OTHER PEOPLE IN THE PROJECT:

-use $ git pull command to update the project files with changes made in the remote repository.
Ex: $ git pull

---

BRANCHES:

Used when you are assigned a specific task in a project working with other people (i.e. your job is to design a login function for the application).  
Your work is stored on a separate branch from the Master branch.

To Create a Branch:

$ git branch [nameOfBranch] (i.e. $ git branch login). Note: this just creates the branch and does not change to it.

To switch to the created branch:
$ git checkout [nameOfBranch] <--Ex: $ git checkout login (switches to the login branch)

NOTE: All changes made to files in the branch are only visible and applicable inside that branch. If you switch to another branch (i.e. master, etc.) the files are not visible and changes made are not applied.

To add the changes in a branch to the master branch (i.e. once the project and functionality is complete), use merge command:

$ git merge [nameOfBranch] <---i.e. $ git merge login

The files and changes in the branch will now be visible and applied to the master branch files.

Delete A Branch:

$ git branch -d branchName

---

BRANCHING AND MERGING:

https://www.youtube.com/watch?v=FyAAIHHClqI

Terms:
Branch: pointer that points to a particular commit
Head: symbolic pointer points to which branch is currently checked out.
Checked out: means "selected" or "active"
Checkout: "select to work on"

Alias command: you can create custom commands to shorten frequently used commands:
synatx: $alias [cmd name] [""]
ex: $alias graph="git log --all --decorate --oneline --graph"
$ graph

//this will create a command $ graph which will run the $git log command it's assigned to.

---

commands you can use:
format: $git mainCommand (optional parameters)

CHECK WHICH BRANCH IS CHECKED OUT (you're on)
$git log --all --decorate --oneline --graph
or
$git status

CREATE NEW BRANCH:
$git branch (name)
Ex: $git branch loginstuff (created a branch named 'loginstuff'.

LIST OF BRANCHES:
$git branch (shows all branches and which the head is pointing to in green)

CHECKOUT TO A DIFFERENT BRANCH:
$git checkout [branchName]
//this moves the head pointer to the specified branch

Shortcut command for creating a branch:

$git checkout -b [branchName]
//this breaks down the two cmd process of $git branch [name] and then $git checkout [name] to one command.

---

MERGING:

--

Fast-Forward Merging:

Can be used when there is a direct path to the master (master is the first direct parent branch)
The master branch is moved to the checked out branch

for this example: SDN = [the name of the branch]
s1 = [a file being edited]

Commands:

$git checkout master //move head to master branch;

$git diff master..SDN //shows differences and what will change with merge;

$git merge SDN //from the master branch merge the new branch;

$cat s1 //shows changes made to file 's1' from the merge;

$graph (this is an alias cmd-see above) //checks that the HEAD is pointed to the master and the merged branch (the master and SDN branch point to the same commit)

--

Now that the merge is complete, the branch can be deleted if desired:

Check it branches are merged:
$git branch --merged //shows what branches are merged;

$git branch -d SDN //deletes the branch named SDN

---

3 WAY MERGE:

-Used when there is not a direct path to the master branch from the merging branch (the last commit of the master branch was not the commit that the branch was originally created from and copied.)

commands:

$git status //confirms you are on master branch

$git merge auth //you can accept default comment or make one with /m ''

---merge completed now----

$git status //check the merge - it should say "merge made by the 'recursive strategy'"

$graph //check the head pointer

--Delete the branch--

$git branch --merged //check if it's safe to delete

$git branch -d auth //deletes the branch named auth that has been merged with master

---

Dealing with Merge Conflicts:

-Occurs when the same lines in the same files were changed in two branches that are being merged.

Note: when merging branches to the master, if there is a difference in a line of code in two different commits on different branches being merged to the master, then the line of code with a change will be merged into the master over the line of code with no change.

\*\*\*If there is a change on both commits being merged to master on the same line of code, then git doesn't know which change to use.

commands:

to abort the merge:
$git merge --abort

to continue with the merge:

$git merge dev //tries to merge the branch with conflicting commits

$git status //check to show that git modified conflicting file for analysis

---

To resolve conflict:

$vi [fileName] //edits the file to see where the conflicts are -- this looks like this

<<<<<< HEAD //indicates head is pointing->lineofcode1
lineofcode1
=========== //this separates the two branches
lineofcode2

> > > > > > dev //indicates what brach lineofcode2 is in

You can now choose which version you want and then delete the ===== and HEAD and branch markers.

---

Now, add the modified file to the staging area:
$git add [modifiededitedfile]

$git status //shows that there are no conflicts and the edited file is in the staging area

(Note: at this stage you are still in the merging process. when changes are committed, git will complete the merge commit as well)

$git commit -m 'commenthere'

You can now delete the merged branch
$git branch -d [branchName]

---

Dealing with Detached Head State:

Detached Head -when the head is pointing to a specific commit and not a branch.

To resolve:
$git checkout master //takes the head and points it to the master branch so the head is not detached.

---

Errors from not having a CLEAN STATE:

Clean State: clean working tree and staging area (there are no modified files in the staging area and no staging files that are not committed)

When you don't have a clean state, you can be blocked from changing branches or complicate merging.

To get a clean State:

$git stash
//this command saves the changes made in files without staging/committing them and stores that info as a stash point and makes a clean state, so you can then go to another branch etc.

$git stash list //shows list of saved stash points on the branch

$git stash list -p //with this option you can see the edits in each stash point

$git stash apply //this applies the most recent stash point and puts the modified files back into the work tree for staging and commit

Once you are done with the stash point, you need to pop or remove it from the storage list of stashpoints:

$git stash pop //applies the stash point and removes it from list

To apply a specific stash from the list use:
$git stash apply [label] //ex: stash@{1}

$git diff //shows the file to confirm changes from stashpoint save were saved and there.

---

$git stash save "commenthere" //this adds a comment to a stashpoint for easier referencing in the list

---

TO GET A PREVIOUS VERSION OF A FILE FROM THE LAST COMMIT:

$ git checkout HEAD [filename] --this pulls the last commit version of the file to your local repository.

=========================

From 4-4 Meetup Denver Modern Web

iTerm2 is good terminal for using git on mac

GitCop - designed by knowledgeable guy at the meetup - helps with workflow and especially good with rebase commands.

git.config - can have global and local copies. a global copy can overwrite local

-removing from the staging area:
$ git reset (this removes it from the staging area)

-remove a committed file:
$ git reset --soft

$ git rm --

committed file/messages in the .git file if you need to recover

-Add all files (that aren't new) with commit message and commit in one command:
$ git commit -am "message"

-Use git add[specific file or dir] and not git add . (why?)

-Abort staged files
$ git checkout

-History of commits etc.
$ git log

-reverse a commit
$ git log (to see history of what to remove)
$ git revert [commit log key]

-Shows history of actions if a merge / checkout goes bad or gets confusing:
$ git reflog

Deletes branch:
$ git branch -D [branch code/name]

---

Ineractive rebase - revert or edit history

$ git rebase -i [range where to go back to HEAD~back x pages]
Ex: $ git rebase -i HEAD~3
// go back 3 pages in the history

-takes you to a point in time before a commit

use $ git status for a list of options and commands to use to alter version history

$ git rebase --continue (finish the rebase history change)

To abort a rebase if you get confused in the history:
$ git rebase --abort

command

rerere - repeats resolve merge - can be used with merge conflicts - look this up.

---

UNDO rm -r:

$ git reset --hard HEAD

see https://stackoverflow.com/questions/2125710/how-to-revert-a-git-rm-r

---

Working with others:

-Never use rebase -i with the official history with a team

-Make a branch

-Keep up to date with the latest modifications: pull regularly

---

Cherry Pick -
copies history of branch with a single partner, but not with the entire team on the official branch.

$ git blame

// used on a line of code you are not sure about it tells you who wrote it, who added it and why

-Go back a number of pages in history to review work done:
$ git shortlog HEAD~100
// goes back 100 pages/steps

---

GitCop - created by attendee - used well with rebase - keeps team members up to date

---

good commit messages 'fixing...' 'adding...' 'updating...' -try to stick to consistent format and indicate what was done and where - maybe with ticket number (canalsobe in body)

Bisect: (takes a range of history based on a condition that returns true or false) - can be used to find out when a specific action was taken in the history

=======================================================

DEBUGGING:

Error: warning: LF will be replaced by CRLF.

See this article: https://stackoverflow.com/questions/5834014/lf-will-be-replaced-by-crlf-in-git-what-is-that-and-is-it-important?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

-When working on cross platform collaborations (i.e. with linux/windows/macos etc.), this will come up because Linux and Mac register a new line in the code with a LF (Linefeed), and Windows registers it as CRLF (Carriage Return/Linefeed). To ignore this error you can use a git config command in the CLI:

If you�re on a Windows machine, set it to true � this converts LF endings into CRLF when you check out code:

$ git config --global core.autocrlf true

If you�re on a Linux or Mac system that uses LF line endings:

$ git config --global core.autocrlf input

// This setup should leave you with CRLF endings in Windows checkouts, but LF endings on Mac and Linux systems and in the repository.

If you�re a Windows programmer doing a Windows-only project, then you can turn off this functionality, recording the carriage returns in the repository by setting the config value to false:

$ git config --global core.autocrlf false

---

Misc commands:

See newest change to file:
$cat [fileName]

==========================

SSH (Secure Shell)

-Establish secure way of communicating between your computer and github

\*\*\*Never give out or reveal your private id_rsa ssh key file

DOCS: https://help.github.com/articles/connecting-to-github-with-ssh/

1. Check if you have SSH keys on your machine (check in the user directory (shortcut is '~') for .ssh dir using the ls -a (to show all hidden files) flag:

$ $ ls -a ~/.ssh

-If you get an error or nothing showing, then you need to install ssh keys, otherwise you can use the keys you have.

2. Create SSH Keys:

DOCS: https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/
and: https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#platform-windows

-2 files (Private file you keep on your computer (id_rsa), and a Public file (id_rsa.pub) you give to third parties like GitHub, etc.)

Command to generate key:

$ ssh-keygen -t rsa -b 4096 -C "youremail@gmail.com"

// -t specified type of key to create, rsa is the type of key, -b flag is set to number of bits (bigger is better-4096 recommended by most services), -C is the comment flag used to provide your email address for GitHub-it's associated with the key pair).

3. Go through options after running command:

-Stick with default name for key (id_rsa): just hit ENTER
-Passphrase: hit ENTER if you don't want a passphrase
-Confirm passphrase - hit ENTER again if no passphrase set.

// key is now created and you should be able to see it with the command: $ ls -a ~/.ssh

- id_rsa (private file), id_rsa.pub (public file to give out)

\*\*Protect the id_rsa private file and never give it out or allow access.

4. Use SSH-AGENT to tell third party sites which ssh key to use:

-Check if ssh-agent is running or start it up with this command in gitbash:

$ eval "$(ssh-agent -s)"

//this will return an id for ssh-agent to show it is running.

5. Add the New SSH Key:

-use ssh-add and provide the path to the private key file (id_rsa) in the user directory/.ssh/private file name:

$ ssh-add ~/.ssh/id_rsa

// key has been added and you can send the public key to third parties now.

6. Send Public Key to Third Parties (GitHub):

DOCS: https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/#platform-windows

-copy and paste the code from the docs to get file contents copied to clipboard using gitbash:

$ clip < ~/.ssh/id_rsa.pub

7. Get the copied SSH Key file contents to GitHub:

-Go to profile page->Settings->SSH and GPG Keys (right side menu)-> click on New SSH Key button.

-Screen asks for Title (this is something to help you remember which computer your working on that has the SSH key)

-In the Key Text Area box, paste (CTRL-V) what was copied to the clipboard with gitbash from the ssh key file. (the contents should start with 'ssh-rsa' and end with your email address provided.

\*\*\*Make sure there is no extra space in the pasted content - remove extra lines or white space at end, etc. if present.

-Click Add Key

8. Test your SSH Key connection with github:

-use the following command to test the SSH key created in github:

$ ssh -T git@github.com

-You will be asked if you want to connect to the source - type 'yes' and hit ENTER

-Message will confirm successful authentication if everything worked.

9. Use the SSH in conjunction with a repository on GitHub to access:

-Go to the newly created repository page link from the github home page.

-from the Quick Setup bar at the top, click on the SSH option next to HTTP. copy this code to the clipboard.

-In gitbash terminal, run the following command to let git know where the external repository is that should hold code files in project:

Use git remote add + origin (default name for main external repository) + [line copied from SSH tab on github repository page]

Ex:
$ git remote add origin git@github.com:BrentGrammer/react-practice-expense-app.git

-check if this worked by running:

$ git remote
// origin should be displayed

$ git remote -v
// urls for remote repository should be displayed

10. Finally, push the code to the associated repository set up with the SSH key:

-use git push with the -u flag which will establish an association - this only needs to be done once initially.
-add the flags for the remote repo name and the branch to push to (i.e. origin is the name, and the branch is master, for ex.).

$ git push -u origin master

===================

FORKING A REMOTE REPOSITORY:

Go to the repository and click the fork button in the top right corner.

CLONE THE FORKED REPOSITORY:

git clone [url to forked repository]

// navigate to the forked repository (this is the copy of the original repository residing in your GitHub account) and look on the right-hand side of the web page. You should see an area that is labeled �HTTPS clone URL�. Simple copy the URL there, and then use it with git clone

---

example of upstream: https://stackoverflow.com/questions/9257533/what-is-the-difference-between-origin-and-upstream-on-github

ADD REMOTE ORIGIN FOR ORIGINAL REPOSITORY FOR PULL REQUESTS:

-add a Git remote that points back to the original repository, like this:

git remote add upstream [original repository link you forked from: ex = https://github.com/openvswitch/openvswitch.github.io.git]

---

CREATE BRANCH WORKFLOW:

Create and checkout a feature branch.
Make changes to the files.
Commit your changes to the branch.

1. create abd checkout to a branch:
   git checkout -b <new branch name>

2. pushing changes to the branch:
   git push origin new-feature

---

AFTER PULL REQUEST ACCEPTED:

First, you should update your local clone by using git pull upstream master. This pulls the changes from the original repository�s (indicated by upstream) master branch (indicated by master in that command) to your local cloned repository.

Delete feature branch once changes merged:
git branch -d <branch name>

Then you can update the master branch in your forked repository:
git push origin master

And push the deletion of the feature branch to your GitHub repository:
git push --delete origin <branch name>

---

KEEPING FORK IN SYNC WITH ORIGINAL REPOSITORY:

To keep your fork in sync with the original repository, use these commands:

git pull upstream master
git push origin master

// This pulls the changes from the original repository (the one pointed to by the upstream Git remote) and pushes them to your forked repository (the one pointed to by the origin remote).

---

STASHING CHANGES:
-used when switching branches before committing or staging any file changes so yo can come back to them later.

DOCS: https://git-scm.com/book/en/v1/Git-Tools-Stashing

$ git stash
// save changes to come back to without committing

$ git stash list
// show stashes

$ git stash apply
// re apply most recent saved changes when back on branch

$ git stash apply [name of stash]
// reapply changes from an older stash

---

CLONING A SINGLE BRANCH FOM REMOTE REPO INTO YOURS:

git clone -b <branchname> --single-branch <remote git url>

DELETING BRANCH BOTH REMOTE AND LOCAL:

$ git push --delete upstream <branch_name>
$ git branch -d <branch_name>

---

SYNCING WITH FORKED MASTER:

$ git fetch upstream
$ git merge upstream/master
$ git push origin master

---

Syncing a local branch with a remote branch:

$ git fetch

# This updates 'remote' portion of local repo.

$ git reset --hard origin/<your-working-branch>

# this will sync your local copy with remote content, discarding any committed

# or uncommitted changes.

---

RESTORE OLD VERSION FROM PREVIOUS COMMIT:

$ git reset --hard 0ad5a7a6 <----this is the commit id

// erases commit history after the specified commit and reverts all code to that commit.

-You could also create a branch to hold the current version and revert after that to be safe.

i.e. $ git checkout -b old-project-state 0ad5a7a6

========

ACCEPT ALL INCOMING CHANGES FROM PULL:

$ git checkout --theirs .
$ git add .

REJECT ALL INCOMING CHANGES AND USE CURRENT CHANGE FOR MERGE:

git checkout --ours .
git add .

or, don't use the . and specify the file(s) in place of the dot that you want to checkout. less "drastic" & exactly what you want to do, presumably.

https://stackoverflow.com/questions/10697463/resolve-git-merge-conflicts-in-favor-of-their-changes-during-a-pull

---

UNDOING CHANGES AND REVERTING TO A PREVIOUS OR LATEST COMMIT:

1. UNDO local file changes but NOT REMOVE your last commit

git reset --hard

2. UNDO local file changes AND REMOVE your last commit

git reset --hard HEAD^

3. KEEP local file changes and REMOVE ONLY your last commit

git reset --soft HEAD^

---

Temp switch to old commit and save:

$ git checkout <commitIdNumber>

$ git checkout -b old-state <commitIdNumber>

---

FIXING GITIGNORE NOT RECOGNIZING CHANGES:

https://stackoverflow.com/questions/11451535/gitignore-is-not-working

on Windows:
$ git rm . -r --cached .
$ git add .
then commit and push

---

Could Not Resolve Host error:

Clear the proxy in git config:

git config --global --unset http.proxy

https version:

git config --global --unset https.proxy

---

BASIC MERGE WORKFLOW:

$ git checkout -b newBranch
$ git commit -a -m 'newBranch work complete'
$ git checkout master
$ git merge newBranch

---

Import a file from another branch:

$ git checkout <other-branch> -- src/react/pages/NotFoundPage.js

---

RESET ORIGIN URL:

git remote set-url origin new.git.url/here

---

MULITPLE SSH KEYS:

See: https://coderwall.com/p/7smjkq/multiple-ssh-keys-for-different-accounts-on-github-or-gitlab

To add to Keychain:

$ ssh-add -K [path/to/private SSH key]
