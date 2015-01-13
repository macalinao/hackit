# -*- mode: ruby -*-
# vi: set ft=ruby tabstop=2 shiftwidth=2 expandtab:

Vagrant.configure(2) do |config|
  # use Ubuntu 14.04 as our base image
  config.vm.box = "ubuntu/trusty32"
  # run our bootstrap to set up all the packages and config
  config.vm.provision :shell, path: "bootstrap.sh"
  # and forward our port to http://localhost:5151
  config.vm.network "forwarded_port", guest: 5151, host: 5151
end
