# Linux OS Baseline Maker

This tool will create a new YUM repository using the latest packages up to a certain date.  The source packages are read from a local filesystem.  The new repository is constructed using symbolic links to the original RPMs - i.e. the RPMs are not copied into the repository - just referenced.  This saves considerable space over using other methods like `reposync`.  

A baseline is basically a set of defined packages released up to a certain date.  The baseline is served out as a YUM repository so can be used to upgrade a fleet of systems, thus ensuring they are all at the same patch level rather than random levels depending on when they were updated.  For instance, depending on site policy, a baseline can be created every six or 12 months.  A separate repository can similarly be created which has only the required security updates.  It can be continually updated and applied to systems as required.

It is written in Perl, but requires the `createrepo` script (which is written in Python).

## Approach
Packages are sorted according to their version numbers, not their file modification date.  This is because, in some instances, multiple versions of the same package are released at the same and sometimes the original file modification dates are not reliable.

## Install

Download the script from [here](https://github.com/Q-Technologies/lobm).

Install the script wherever you prefer, but it will look in the following locations for it's config file (in this order):
  
* `/etc/lobm`
* `../etc`  (relative to the script)
* `.`

The config file must be named: `lobm.yaml`

Alternatively, use the SPEC file to create an RPM and then install the RPM.

## Prelimary Tasks

### Software Packages
You need to have already downloaded the linux distrubution's RPMs into a local directory.  The following methods have been tested:

* SLES using SMT (Subscription Management Tool)
* openSUSE and CentOS using rsync from a mirror
* copying all the files from ISO for SLES, openSUSE and CentOS
* using reposync for RHEL

### Setup The Main Configuration File
Create the `lobm.yaml` file in one of the locations specified in the install section.  The included sample file can be used as a starting point.  Key things defined in the config file are:

* location where the new baseline repository will be created
* where to create the repositories
* how aggressively to use the CPU
* the URL prefix where the repository will be served from

The key variables:

* `baseline_dir` - the place on disk for new repositories
* `http_served_from` - effectively the DocumentRoot
* `http_server_name` - the server name the repository can be reached at
* `http_server_proto` - the protocol the repository can be reached over
* `createrepo_cmd` - path to createrepo script
* `workers` - number of workers to use for the createrepo (if not specified then workers will equal cpu threads)


Here is an example:

```yaml
baseline_dir: "/software/repos/baselines/"
http_served_from: "/software"
http_server_name: "install.example.com"
http_server_proto: "http"
createrepo_cmd: "/usr/bin/createrepo"
workers: 2
```

### Setup Each Baseline Configuration File
The baseline configuration files are in YAML format annd can be stored anywhere.  A good place to put them is in `/etc/lobm/baselines`.

The key variables:

* `name` - the baseline name.  This will be visible in the URL and will be the repository name
* `description` - a more verbose description of the baseline
* `target` - the platform/os to target, e.g. centos, rhel, redhat, suse, sles
* `os_release` - only applicable to Red Hat.  This ensures a certain redhat-release-server package is chosen to match the required OS release level
* `versions` - the number of versions of each package to put into the repository.  One is the default if omitted.
* `rpm_dirs` - an array of associative arrays specifying where to find the source packages.  
  * `dir` - the path to the packages (it will be used recursively)
  * `date` - only find packages up to this date
* `exclude` - an array of packages to exclude.  All other packages found will be included
* `include` - an array of packages to include.  Any package not specified in the include will be excluded regardless of the `exclude` array contents

Here is an example:

```yaml
name: baseline_name
description: A more verbose description
target: platform
os_release: 6.5
versions: 1 # number of versions of each package to put in new repository
rpm_dirs:
  -
    dir: /path/to/first/dir/of/RPMs
    date: YYYY-MM-DD  # Date to select RPMs up to
  -
    dir: /path/to/second/dir/of/RPMs
    date: YYYY-MM-DD  # Date to select RPMs up to
include:
  - excluded_package_1  # excludes all others ('exclude' is effectively ignored)
exclude:
  - excluded_package_1
  - excluded_package_2
```


## Usage

### Invocation

```bash
lobm -c /path/to/baseline_definition.yaml
```

### Options

* `-h` a simple help message
* `-v` display messages describing what is happening
* `-r` force running as root (should not be necessary normally)
* `-c` full path to the baseline definiton file 

### Baseline Definiton File
The baseline configuration file needs to be in YAML format with the following fields:

```yaml
name: baseline_name
rpm_dirs:
  -
    dir: /path/to/first/dir/of/RPMs
    date: YYYY-MM-DD  # Date to select RPMs up to
  -
    dir: /path/to/second/dir/of/RPMs
    date: YYYY-MM-DD  # Date to select RPMs up to
```




## TODO

* Only builds x64 repos at this stage
* Only uses the file modification date to determine cutoff, it could use the RPM build date instead
* Better validation of inputs from the YAML files is required