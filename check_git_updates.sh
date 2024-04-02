#!/bin/bash

# Set the branch you want to track (e.g., master)
BRANCH="master"

# Set the name of your remote repository (e.g., origin)
REMOTE="ipsum"

# Fetch updates from the remote repository
git fetch $REMOTE

# Get the status of the branch
STATUS=$(git status -uno)

# Check if your local branch is ahead, behind, or has diverged
echo $STATUS

# Check if there are new commits
if [[ $STATUS == *"Your branch is behind"* ]]; then
  # Get the current timestamp
  TIMESTAMP=$(date +%Y%m%d%H%M%S)
  
  # Get the list of changed files
  CHANGED_FILES=$(git diff --name-only $REMOTE/$BRANCH)

  # Loop through each changed file
  for FILE in $CHANGED_FILES
  do
    # Copy the changed file to a new file with the timestamp in its name in the same directory
    cp $FILE "${FILE%.*}_$TIMESTAMP.${FILE##*.}"
  done
fi



#chmod +x check_git_updates.sh