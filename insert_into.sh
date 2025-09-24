#!/bin/bash

# Usage: ./merge-into.sh target-branch-name

# Check if target branch is provided
if [ -z "$1" ]; then
  echo "❌ Error: No target branch specified."
  echo "Usage: $0 <target-branch>"
  exit 1
fi

TARGET_BRANCH=$1

# Get current branch name
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo "🔍 Current branch: $CURRENT_BRANCH"
echo "📌 Target branch: $TARGET_BRANCH"

# Stash any uncommitted changes
echo "🧺 Stashing changes..."
git stash -q --keep-index

# Switch to target branch
echo "🔄 Checking out $TARGET_BRANCH..."
git checkout $TARGET_BRANCH

# Pull latest changes
echo "📥 Pulling latest changes from remote..."
git pull origin $TARGET_BRANCH

# Merge current branch into target
echo "🔗 Merging $CURRENT_BRANCH into $TARGET_BRANCH..."
git merge $CURRENT_BRANCH

# Push changes
echo "🚀 Pushing merged changes to remote..."
git push origin $TARGET_BRANCH

# Switch back to original branch
echo "↩️ Switching back to $CURRENT_BRANCH..."
git checkout $CURRENT_BRANCH

# Apply stashed changes
echo "📦 Restoring stashed changes..."
git stash pop -q

echo "✅ Merge complete!"
