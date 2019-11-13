## Instructions on installing on Ubuntu 18/19

1. Update all packages (apt update)
2. Allow ports for the HTTP and HTTPS
3. Install Docker 

    sudo apt install docker.io docker-compose

4. Login in your docker hub account. Trillo will provide permission to download  software

    sudo docker login

5. Create a folder /opt/trillo and git clone following repository
		

	    sudo mkdir /opt
    	sudo bash
    	cd /opt
    	git clone https://github.com/opentrillo/install-centos.git trillo
    	cd trillo

6. Add VM's IP address to your DNS A record by giving a name. 
7. Login in your DNS hosting provider and create a new DNS A record.  Run the following command to make sure the record is alive. Verify that the IP address matches the output of the following command. 
	
    dig  <A-record-name>.yourdomain

8. Once the domain is confirmed then with a valid email address,   execute the following command in the same folder. If everything goes fine then the runtime server will be up.

    ./trillort install-cert --domain tmsdesign.trillo.io --email info@trillo.io

9. If you are running then runtime on the Google Cloud,  then you can capture output logs in the Stackdriver. First, install the logging agent on the VM using the URL “https://cloud.google.com/logging/docs/agent/installation” and then add the following metadata on the computer engine. Add a Custom metadata item with the key user-data and the value

    write_files:
      - path: /etc/docker/daemon.json
        content: '{"log-driver":"gcplogs"}'
    
    runcmd:
      - systemctl restart docker

Reference: https://cloud.google.com/community/tutorials/docker-gcplogs-driver

Finally, provision the new runtime URL on the AppBuilder and test with a deployment.  the deployment is successful then you have successfully created a new runtime server.  




