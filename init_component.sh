#!/bin/bash


# Parse command-line options
name=""
remote=""
namespace="cltl"
no_app=false

usage() {
  echo "Usage: $0 [OPTIONS]"
  echo "Options:"
  echo "  -n, --name <name>       Name of the component"
  echo "  -r, --remote <remote>   Remote repository URL"
  echo "  -s, --namespace <namespace>"
  echo "                          Namespace to use for packages, 'cltl' by default (optional) "
  echo "  -a, --no-app            Remove app specific code (py-app/) (optional)"
  echo ""
  echo "Example:"
  echo ""
  echo "$0 --name mycomponent --remote 'https://github.com/me/mycomponent' --namespace myproject"
  echo ""
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--name) shift; name="$1" ;;
    -r|--remote) shift; remote="$1" ;;
    -s|--namespace) shift; namespace="$1" ;;
    -a|--no-app) no_app=true ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      ;;
  esac
  shift
done

# Validate if required options are provided
if [ -z "$name" ] || [ -z "$remote" ]; then
  usage=
  exit 1
fi


echo "Init repository for component $name in namespace $namespace with remote repository $remote"


# Remove app specific code
if [ "$no_app" = true ]; then
  rm -rf py-app
fi


# Adjust namespace for modules
if [ "$namespace" != "cltl" ]; then
  git mv src/cltl "src/$namespace"
  git mv src/cltl_service "src/${namespace}_service"
fi


# Setup setup.py
sed -i '.bak' "s|https://github.com/leolani/cltl-template|$remote|g" setup.py
sed -i '.bak' "s/cltl[.]template/$namespace.$name/g" setup.py
sed -i '.bak' "s/cltl\([^.]*\)[.][*]/$namespace\1.*/g" setup.py
sed -i '.bak'  "s/template/$name/g" setup.py
rm setup.py.bak


# Setup README
echo "# $name" > README.md


# Setup git
git remote remove origin
git remote add origin $remote

if ! git ls-remote "$remote" &> /dev/null; then
  echo "Remote repository $remote not found on on GitHub"
  exit 1
fi

if git ls-remote "$remote" | grep -q "refs/heads"; then
  echo "Remote repository $remote is not empty:"
  git ls-remote
  exit 1
fi


git add .
git status


echo "Commit and push your changes with"
echo ""
echo "git push --set-upstream origin main"



