# Copr "make_srpm" hook, run as root in a network-enabled chroot:
#   make -f .copr/Makefile srpm outdir=<dir> spec=<path/to/zapfast.spec>
specdir := $(dir $(spec))
work := $(shell mktemp -d)

srpm:
	dnf -y install git rpm-build rpmautospec rpmdevtools
	# the clone belongs to another user; let git and rpmautospec read it
	git config --system --add safe.directory '*'
	rpmautospec process-distgit $(spec) $(work)/zapfast.spec
	cp $(specdir)zapfast-update-public-key.pem $(work)/
	spectool --get-files --directory $(work) $(work)/zapfast.spec
	rpmbuild -bs --define '_sourcedir $(work)' --define '_srcrpmdir $(outdir)' $(work)/zapfast.spec
