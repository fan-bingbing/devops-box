Vagrant.configure(2) do |config|
	config.disksize.size = '50GB'
	config.vm.define "devops-box" do |devbox|
		devbox.vm.box = "ubuntu/bionic64"
    		devbox.vm.network "private_network", ip: "192.168.56.120"
				devbox.vm.network "forwarded_port", guest: 8000, host: 8000
				# devbox.vm.network "forwarded_port", guest: 8888, host: 8888
				# devbox.vm.network "forwarded_port", guest: 1000, host: 1000
				# devbox.vm.network "forwarded_port", guest: 7681, host: 7681
				# run jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser

				devbox.vm.synced_folder ".", "/vagrant", :mount_options => ['dmode=755', 'fmode=755']
      	devbox.vm.provision "shell", path: "scripts/install.sh"
    		devbox.vm.provider "virtualbox" do |v|
    		  v.memory = 4096
    		  v.cpus = 2
    		end
	end
end
