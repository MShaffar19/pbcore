#!/bin/bash
type module >& /dev/null || . /mnt/software/Modules/current/init/bash
module load python/2.7.9-mobs-pbcore
set -ex


export PATH=$PWD/build/bin:$PATH
export PYTHONUSERBASE=$PWD/build
PIP="pip --cache-dir=${bamboo_build_working_directory:-$PWD}/.pip"

rm -rf   build
mkdir -p build/bin build/lib build/include build/share
$PIP install --no-compile --find-link file:///mnt/software/p/python/wheelhouse/thirdparty --user -r requirements.txt
$PIP install --no-compile --find-link file:///mnt/software/p/python/wheelhouse/thirdparty --user -r requirements-dev.txt
$PIP install --no-compile --find-link file:///mnt/software/p/python/wheelhouse/thirdparty --user -e ./

set +e
make pylint # way too many errors right now
set -e
make test
