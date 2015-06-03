
#########################
# Configurations        #
#########################

scriptDirectory = "vagrantScripts/"     # Location of all configuration scripts for the VMs
                                        # Name them after the hostname

boilerplateScript = "boilerplate.sh"    # This script is run on each machine BEFORE the specialized configuration script

nodes = [                               # Each machine has it's own line. Hostname and ip are required, all other fields are optional
  { :hostname => 'db',          :ip => '192.168.5.100', :forwardedPorts => [ 27017 ] },
  { :hostname => 'actor',       :ip => '192.168.5.101', :shared => "src/actor" },
  { :hostname => 'scraper1',    :ip => '192.168.5.102', :shared => "src/scraper" },
]

box = "ubuntu/trusty64"                 # The base box. This includes the OS and some updates

#########################
#  Build the machines   #
#########################
Vagrant.configure("2") do |config|      # Configure Vagrant using version 2 of the configuration object
  nodes.each do |node|                          # For each loop setting each object in nodes to node
    config.vm.define node[:hostname] do |nodeconfig|    # This scopes the configuration variable for each of the machines
      # Set the box, hostname, and ip address
      nodeconfig.vm.box = box
      nodeconfig.vm.hostname = node[:hostname] + ".box"
      nodeconfig.vm.network :private_network, ip: node[:ip]
      
      # This is run on every machine
      nodeconfig.vm.provision "shell", path: scriptDirectory + boilerplateScript
      
      # If a machine-specific configuration script exists ([hostname].sh), run it
      if File.exists?(scriptDirectory + node[:hostname] + '.sh')
        nodeconfig.vm.provision "shell", path: scriptDirectory + node[:hostname] + '.sh'
      end

      # Forward all necesary ports. All port forwarding is on the same port.
      if node[:forwardedPorts]
        node[:forwardedPorts].each do |port|
          nodeconfig.vm.network "forwarded_port", guest: port, host: port
        end
      end

      # Set the shared folder
      if node[:shared]
        nodeconfig.vm.synced_folder ".", "/vagrant", disabled: true		# Disable the default
        nodeconfig.vm.synced_folder node[:shared], "/vagrant"
      end

      # Set up the virtual machine's capabilities
      memory = node[:ram] ? node[:ram] : 256;
      nodeconfig.vm.provider :virtualbox do |vb|
        vb.customize [
          "modifyvm", :id,
          "--cpuexecutioncap", "50",
          "--memory", memory.to_s,
          "--cpus", 1,
        ]
      end
    end
  end
end

#########################
# Done		        #
#########################
