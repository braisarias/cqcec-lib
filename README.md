CQCEC
===========

#### Notes.
The only supported router is the Hitron model.

#### Requeriments.
You must to have python-setuptools and nmap packages installed on your team. Try running sudo `apt-get install nmap python-setuptools` if you are running a Debian based operative system or sudo `yum install nmap python-setuptools` if you are running a Fedora operating system.

#### Installation.

 + Download the repository using Git (`git clone https://github.com/braisarias/fdr-ipwhois.git`) or [direct download](https://github.com/braisarias/fdr-ipwhois/archive/master.zip).
 + Go to the repository directory.
 + Execute the setup script (`sudo python setup.py install`).
 + If everything goes fine you should be able to excute the `cqcec` command.

#### Configuration.
A configuration file named **cqcec_config.cfg** has been placed in the etc directory. You should change this file variables in order to be able to run the program correctly.

You can get a Google Safe Browsing API key visiting this [link](https://developers.google.com/safe-browsing/key_signup).

#### Running.
In order to run the web interface you should execute a web server.

    cd web
    python -m CGIHTTPServer

Now you should access to the web interface at http://localhost:8000.
