#!/bin/bash

dir=$(dirname $0)
mkdir -p RPMS

for host in $@
do echo Building RPM on $host
	echo
	echo
	ssh $host mkdir -p rpmbuild/SOURCES rpmbuild/SPECS
	rsync -av --delete --exclude=\*.rpm ${dir:?}/lobm ${dir:?}/lobm.yaml ${dir:?}/README.md ${dir:?}/LICENSE $host:rpmbuild/SOURCES
	rsync -av --delete --exclude=\*.rpm ${dir:?}/lobm.spec $host:rpmbuild/SPECS
	ssh $host rpmbuild -ba rpmbuild/SPECS/lobm.spec
    rsync -av $host:rpmbuild/SRPMS/ RPMS/
    rsync -av $host:rpmbuild/RPMS/ RPMS/
done
