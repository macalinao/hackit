# README #

*Hackit* - Reddit for Facebook Groups.

Pull requests appreciated!

##Setup

Setup is provided via [Vagrant](https://vagrantup.com), which deals with all dependencies and setup issues.

### Running with Vagrant

To start Hackit with Vagrant:

- Install Vagrant
- Clone the repo
- Run, in a terminal:
```bash
	vagrant up
	vagrant ssh
	python /vagrant/web.py
```

### Running without Vagrant

Please check out the [`bootstrap.sh`](bootstrap.sh) file, as that contains all the setup needed for installing dependencies for Hackit.
