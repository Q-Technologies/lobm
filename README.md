# Linux OS Baseline Maker

This tool will create a new YUM repository using the latest packages up to a certain date.  The source packages are read from a local filesystem.

It is written in Perl, but requires the `createrepo` script (which is written in Python).

## Install

Download the script from here:

Install the script wherever you prefer, but it will look in the following locations for it's config file (in this order):
* ../etc
* /etc
* .

The config file must be named: `lobm.yaml`

Alternatively, use the SPEC file to create an RPM and then install the RPM.

## Prelimary tasks

### Software packages
You need to have already downloaded the linux distrubution's RPMs into a local directory.  The following methods have been tested:
* SLES using SMT (Subscription Management Tool)
* openSUSE and CentOS using rsync from a mirror
* copying all the files from ISO for SLES, openSUSE and CentOS

### Setup the config file
Create the `lobm.yaml` file in one of the locations specified in the install section.  The included sample file can be used as a starting point.  Key things defined in the config file are:
* location of baseline definition files
* where to create the repositories
* how aggressively to use the CPU
* the URL prefix where the repository will be served from

## Usage

