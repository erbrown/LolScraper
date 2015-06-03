

# Configurations for each machine
scriptDirectory = "vagrantScripts/"
boilerplateScript = "boilerplate.sh"
nodes = [
  { :hostname => 'db',          :ip => '192.168.5.100', :forwardedPorts => [ 27017 ] },
  { :hostname => 'actor',       :ip => '192.168.5.101' },
  { :hostname => 'scraper1',    :ip => '192.168.5.102' },
]

# The box for each machine
box = "ubuntu/trusty64"

#  Build the machines
Vagrant.configure("2") do |config|
  nodes.each do |node|
    config.vm.define node[:hostname] do |nodeconfig|
      nodeconfig.vm.box = box
      nodeconfig.vm.hostname = node[:hostname] + ".box"
      nodeconfig.vm.network :private_network, ip: node[:ip]
      nodeconfig.vm.provision "shell", path: scriptDirectory + boilerplateScript
      nodeconfig.vm.provision "shell", path: scriptDirectory + node[:hostname] + '.sh'

      if node[:forwardedPorts]
        node[:forwardedPorts].each do |port|
          nodeconfig.vm.network "forwarded_port", guest: port, host: port
        end
      end

      memory = node[:ram] ? node[:ram] : 256;
      nodeconfig.vm.provider :virtualbox do |vb|
        vb.customize [
          "modifyvm", :id,
          "--cpuexecutioncap", "50",
          "--memory", memory.to_s,
        ]
      end
    end
  end
end
