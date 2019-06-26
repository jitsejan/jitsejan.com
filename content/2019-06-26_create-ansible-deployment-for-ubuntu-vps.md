Title: Creating an Ansible playbook to provision my Ubuntu VPS
Date: 2019-06-26 20:16
Modified: 2019-06-26 20:16
Category: posts
Tags: DevOps, Ansible, data engineer, VPS, Ubuntu, Spark, Jupyter
Slug: creating-ansible-deployment-for-ubuntu-vps
Authors: Jitse-Jan
Summary: My first experiment with Ansible to automate the provisioning of my server.

# Provisioning my VPS with Ansible
## Objective
Clean installation on Ubuntu 18.04 with the following requirements:

- Create user account for myself from the root account
- Install basic applications (`curl`, `java`, etc)
- Install [Jupyter](https://jupyter.org/) notebooks
- Install [Spark](https://spark.apache.org/)
- Install [nginx](https://www.nginx.com/)

## Introduction
The goal is to provision my VPS at SSDNodes with all the tools I need to develop Spark and Python code in Jupyter notebooks. While in previous installations I have been using both [Docker](https://github.com/jitsejan/notebooks) and [Kubernetes](https://github.com/jitsejan/kubernetes-vps) to make it easy to spin up the Spark notebooks, it would still require me to install Docker, Kubernetes and all relevant software after manually creating the user account and doing all the *boring* work. Plus, installation of Kubernetes is **always** a challenge and a lengthy process. Since I don't need any containerization now, I would expect that a clean installation without Docker and Kubernetes should be more than enough to get my development environment up and running. 

At work I have introduced [Terraform](https://www.terraform.io) to deploy our data platform on [AWS](https://aws.amazon.com) (and a few resources on [Azure](https://azure.microsoft.com)). While Terraform works great for setting up the services for all our data pipelines, APIs and machine learning models, I wanted to understand more about [Ansible](https://www.ansible.com/) to see if it would be useful too. In short, Terraform should be used for setting up resources and services and Ansible should be used to provision single (or multiple) instances. For example, you would create an EC2 instance automatically with Terraform and install all relevant applications on the EC2 machine with Ansible. 

<img src="https://getvectorlogo.com/wp-content/uploads/2019/01/red-hat-ansible-vector-logo.png" />

> **WHY ANSIBLE?**  
> Working in IT, you're likely doing the same tasks over and over. What if you could solve problems once and then automate your solutions going forward? Ansible is here to help.  

## Preparation
Installation of Ansible on Mac (and Linux) is easy with [Brew](https://brew.sh).

``` bash
$ brew install ansible
```

After installation we can verify if Ansible is available by checking the version. In my case I have installed version **2.8.1**. 

```bash
$ ansible --version
ansible 2.8.1
  config file = /Users/jitsejan/.ansible.cfg
  configured module search path = ['/Users/jitsejan/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/Cellar/ansible/2.8.1_1/libexec/lib/python3.7/site-packages/ansible
  executable location = /usr/local/bin/ansible
  python version = 3.7.3 (default, Jun 19 2019, 07:38:49) [Clang 10.0.1 (clang-1001.0.46.4)]
```

Finally, you need to make sure the machine you want to provision is defined in the Ansible configuration `/etc/ansible/hosts`.

```ini
[ssdnodes]
development.jitsejan.com
```

To make it easier to connect to the host, it is smart to create a key pair on the local computer and copy it to the host. This way you do not need to provide login details when you run the Ansible tool. Create the keypair with `ssh-keygen`:

```bash
$ ssh-keygen -t rsa -b 4096
```

Copy the key to the host to be deployed. It will ask you to provide the password for the root, but it will be the only time we need the password.

```bash
$ ssh-copy-id root@development.jitsejan.com
```

And that is all there is to it to get started with Ansible.

## Structure
The directory of the repository at the time of writing looks like the following. Please note that this _might_ not be the best structure, but it gave me a good head-start to work with the file structure, local and global variables and templating.

```bash
├── README.md
├── provision_vps.yaml
└── roles
    ├── base
    │   ├── tasks
    │   │   └── main.yml
    │   └── vars
    │       └── main.yml
    ├── common
    │   └── tasks
    │       └── main.yml
    ├── jupyter
    │   ├── defaults
    │   │   └── main.yml
    │   ├── files
    │   │   ├── custom.css
    │   │   └── requirements.txt
    │   ├── tasks
    │   │   └── main.yml
    │   ├── templates
    │   │   ├── etc
    │   │   │   └── systemd
    │   │   │       └── system
    │   │   │           └── jupyter.service
    │   │   └── jupyterhub_config.py.j2
    │   └── vars
    │       └── main.yml
    ├── nginx
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── nginx.conf.j2
    └── spark
        ├── tasks
        │   └── main.yml
        └── vars
            └── main.yml
```

## Breakdown
### Playbook
The core of an Ansible deployment is a playbook (or multiple). The playbook contains all the different items that should be deployed. In Ansible these items are divided by *roles*, each role can relate to a tool, a service, a user or anything else that makes sense to group together. In my repository I have called the playbook `provision_vps.yaml'. The file is small, since I have used multiple roles to be loaded when running the playbook. 

The first part of the file contains the host and the user you want to run the deployment with. I have only specified one host, since I only have one VPS to deploy. 

```yaml
- hosts: ssdnodes
  remote_user: root
```

For each host, we can define *global* variables by defining them in the playbook under `vars`. This makes the variables available in all the different roles. If the variable is only to be used within a role, it is smarter to define it at the role level. In my case I want to deploy a Jupyter notebook and therefore I should define the parameters on playbook level, so the variables become available for both the Jupyter and nginx installation. I define the domain, the name and port to host the notebook from, and I supply the location of the SSL certificate and key.

```yaml
  vars:
    jupyter_domain: dev.jitsejan.com
    jupyter_name: 'dev'
    jupyter_port: 8181
    key_out: /home/jupyter/.jupyter/jupyter.key
    cert_out: /home/jupyter/.jupyter/jupyter.cert

```

If you want to prompt the user for input for certain variables you can use `vars_prompt`. In my playbook I want to ask the user (me) for the username and password to create an account on the Ubuntu box for me. It will ask to confirm both the user and password before it continues to run the playbook.

```yaml
  vars_prompt:
    - name: "user_name"
      prompt: "Enter a name for the new user"
      private: no
      confirm: no
    - name: "user_password"
      prompt: "Enter a password for the new user"
      private: yes
      encrypt: "sha512_crypt"
      confirm: yes
      salt_size: 7
```

Finally, I define the `roles` to be executed as part of the playbook. This is the part where you can easily add new roles when you want to add more services to your machine.

```yaml
roles:
  - base
  - common
  - { 
      role: 'spark',
      spark_version: '2.2.1',
      hadoop_version: '2.7'
    }
  - jupyter
  - {
      role: 'nginx',
      app_ip: localhost,
    }
```

As you can see, you can call the role as simple parameter, or call the role by specifying the role and any additional variable. For the Spark role we supply the Spark and Hadoop version. For the Nginx role we indicate that our app will only run on localhost. (We use Nginx as proxy to make it accessible on a public address).

### Roles
I have divided the roles along the way and I do not guarantee this is the most logical way of doing things. It makes sense for me now, so I am just going to go with it. The goal is to have building blocks to make the final application run smoothly with all dependencies in the right place.

#### Base role
The first role I created is the **base** role which will take care of the following:
- Check if all necessary packages are installed.
- Create the personal user account based on the prompt of the playbook.
- Add the user to sudo and create a password less login on the local computer.

The tasks to be executed are defined inside the role in the `tasks` folder. Ansible expect the `main.yml` inside this folder to have all the steps for the role. Variables can be defined in two folders, either in `vars/main.yml` or in `defaults/main.yml`. The defaults, as the name says, contains the default value for certain variables. These can be overwritten by variables defines in the `vars` folder. Note that some of the variables are passed through from the playbook and are not defined on this level. 

To install a package the `apt` module can be used. Variables are passed in using the double curly brackets (`{{ }}`).  The following is part of `roles/base/tasks/main.yml`. I will leave the rest out to keep this article short.
 
```yaml
- name: Ensure necessary packages are installed
  apt: 
    name: "{{ base_pkgs }}"
    state: present
    update_cache: yes
...
```

To keep things simple, I have only defined one package to be installed in `roles/base/vars/main.yml`. I prefer `mosh` over `ssh` since my internet is often buggy and I don't like to keep on reconnecting with ssh. 

``` yaml
base_pkgs:
  - mosh
```

#### Common role
The  **common** role currently only installs `openjdk-8-jdk`, `openjdk-8-jre-headless` and exports the `JAVA_HOME` variable. Java 8 is needed to make Spark work, since it is not compatible (yet) with Java 11. 

#### Jupyter role
At this point it gets more interesting. To deploy Jupyter on the VPS some more advanced steps are needed. Just to recap, the structure of the Jupyter role looks like this:

```bash
├── defaults
│   └── main.yml
├── files
│   ├── custom.css
│   └── requirements.txt
├── tasks
│   └── main.yml
├── templates
│   ├── etc
│   │   └── systemd
│   │       └── system
│   │           └── jupyter.service
│   └── jupyterhub_config.py.j2
└── vars
    └── main.yml
```

The `defaults`  contain the default values for the Jupyter deployment.  The `main.yml` has the following content, which basically tells the system that for the notebook server I want to use Python 3 as default and only run it from localhost. 

```yaml
---
jupyter_python_executable: python3
jupyter_package_manager: pip3
jupyter_package_manager_become: no
jupyter_package_state: latest
jupyter_password: 'sha1:b3af1b4adee9:9e86cb52435cc24db0b487451c10f6d348734645'
jupyter_open_browser: false
jupyter_ip: 'localhost'
```

Under the `files` folder you can put the files you wish to copy to the VPS. In my case I want to copy the `custom.css` and `requirements.txt` to the VPS. The CSS file contains the custom layout I like for my notebooks, the requirements file obviously contains the Python packages I wish to use.

The `tasks/main.yml`  is pretty lengthy, so I will summarize what it does:

- Ensure important Jupyter dependencies are installed
- Create a Jupyter user and group
- Create the folder for the data and the virtual environment
- Copy the `requirements.txt` and install the libraries
- Create the Jupyter configuration
- Create the SSL certificates
- Copy the custom CSS file to the server
- Make and run the *jupyter.service*

One of the nifty things of Ansible is conditional execution, only run certain tasks if a condition is met. For example, I will not recreate the virtual environment if it already exists, as shown in the code snippet below.

```yaml
- name: Check to see if the Jupyter environment exists
  stat: 
    path: /data/jupyter
  register: environment_exists
  become_user: jupyter
```

When the folder exists already, it will register `environment_exists` that can be used under the `when` condition with `environment_exists.stat.exists == False `.

```yaml
- block:
  - name: Install virtual environment
    pip:
      name: virtualenv
      executable: pip3
      state: latest
  - name: Create virtualenv root directory
    file:
      path: /data/jupyter
      state: directory
      owner: jupyter
      group: jupyter
      mode: 0755
  - name: Set up virtual environment
    shell: virtualenv -p python3 /data/jupyter
    become_user: jupyter
    changed_when: no
  when: environment_exists.stat.exists == False
```

In the `templates` folder I have used two different approaches. The first one is to *replicate* the location of the folder on the server by creating a similar directory structure.  The `jupyter.service` will be placed under `/etc/systemd/system/`. The second approach is the preferred method and doesn't create the *annoying* directory structure. It uses [Jinja](http://jinja.pocoo.org/) templates to easily configure files dynamically with variables. I have defined the structure of a `jupyterhub_config.py` with variables that will be filled in automatically by Ansible. As you might remember, some of these variables are part of the defaults of this role, while some other where defined on playbook level.

```python
# jupyterhub_config.py
c.NotebookApp.open_browser = {{ jupyter_open_browser }}
c.NotebookApp.ip = '{{ jupyter_ip }}'
c.NotebookApp.port = {{ jupyter_port }}
c.NotebookApp.password = '{{ jupyter_password }}'
c.NotebookApp.allow_origin = '*'
c.NotebookApp.allow_remote_access = True
c.NotebookApp.certfile = '{{ cert_out }}'
c.NotebookApp.keyfile = '{{ key_out }}'
c.NotebookApp.notebook_dir = '/data/notebooks/'
c.InteractiveShell.ast_node_interactivity = "all"
```

In the `vars/main.yml` I have only defined the Jupyter packages that I wish to install, the location of the Jupyter configuration and the variables to create the SSL certificate for the server.

#### Nginx role
The role for Nginx is relatively simple and only contains a couple of steps.

1. Install Nginx
2. Add reverse proxy for the Jupyter server
3. Create the symlink to add the proxy to available websites
4. Restart Nginx

To easily create the Nginx configuration file, I have created a template that will set the domain name, the port and the certificates. Since I am not aiming to use Nginx to host anything else, I haven't created any additional templates yet.

#### Spark role
Currently the Spark role is the final step of my playbook. This role will install Spark and download all necessary JAR files I need to work on my Data Engineering tasks. 

## Todo
There are a few things that I might still modify in my approach, since I have noticed that I could parameterize more steps in the playbook. An annoying issue is that the Jupyter server does not pick the right environment variables, so I need to think of a good way to set them before running the notebooks. Right now my workaround is to hardcode the paths to `SPARK_HOME` and `JAVA_HOME` inside the notebook itself. Secondly, the certificate that I create in this playbook is not trusted by the browser, because it is self-signed. I have used `openssl`, but I should look into `letsencrypt` or use the `acme` tool that Ansible provides. 

## Conclusion
Ansible is a fantastic tool to automate the provisioning of a VPS (or any other fresh Ubuntu installation). It took me often over several hours, and with Kubernetes days, to setup the Ubuntu box, but using Ansible I simply enter the username and password and after 10 minutes the system is ready. Another great benefit is the use of Jinja templates, which should be very familiar for a Python developer. My goal is to add more roles and keep everything up to date in my [GitHub repo](https://github.com/jitsejan/vps-provision).
