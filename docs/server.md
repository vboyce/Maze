---
layout: default
---



This is instructions on how to set up and run an Ibex-maze server using a free-tier AWS EC2 instance. The free tier is available for a year, so to avoid charges close your account after you're done, or ask your lab to make an account and pay for your webserver if you want to continue long term. That said, the free-tier is useful for small-scale short-term work to try it out. 

Note: These instructions were tested with Ubuntu; I believe they generalize to MacOS and other Linux-based systems. If you use Windows, it will be easiest to use Windows Subsystem for Linux (see also [AWS documentation on using wsl with ec2](https://docs.amazonaws.cn/en_us/AWSEC2/latest/UserGuide/WSL.html))

 These instructions will make the most sense with a basic familiarity with terminal commands like `cd`, `ls`, and `cp`. If you aren't familar with them, that's okay! You can learn more about any of them on the web; I've also tried to link to some useful pages.
 Here are [two](https://medium.com/@grace.m.nolan/terminal-for-beginners-e492ba10902a) [tutorials](https://ubuntu.com/tutorials/command-line-for-beginners) on terminal basics. 

# Setting up a server

## On the website
1. Go to <https://aws.amazon.com/free> and follow the instructions to create an account. It'll want the normal type of information from you. It will want a credit card number, but they say they won't charge it if you stay in the free zone. There will be annoying captchas. (This is a free service for only a year; so be sure to close your account after if this is a class project, or encourage your lab to make an account and pay for your webserver if it's for research.)

2. Once you have an account, you can go to <https://aws.amazon.com/console/> and sign in. From the top menu (or using search) select ec2.

3. This page will show you the list of ec2 instances you have (currently 0). Click launch instance to create a new instance. 
Follow through the steps and do the following
* Name the server 
* make the image ubuntu 64-bit
* choose t2.micro size
* create a key-pair login (using ssh and pem) (this should cause the download of a server-name.pem file)
* allow ssh from anywhere (despite the warning); if you will only be logging in from one computer, you could restrict to just the current IP. 

4. When your instance is created, it should show up in the instance list. Click on it to do more set up.

5. Take note of what the *public* IPv4 for your server is. This will be listed in the instance summary and will be some numbers with dots in between like 12.345.67.89 . You will need this later. 

6. The last website thing we need is to make a port open so you'll be able to host experiments and have others see them. The most common port to have open is 3000, so we'll do that. To do this, you want to go to the security group -- probably called `sg-blahblahblah (launch-wizard-1)` and edit inbound rules. Add a rule for `type="custom tcp"`, `port range = 3000`, `source=anywhere`, and save rules. 

## On your computer

1. In order to ssh into the server, you need to put the .pem file where your computer will find it. Open a terminal and do the following:
```
cd ~/.ssh
cp ~/Downloads/myserver.pem .
chmod 400 myserver.pem
```

	(Replace myserver.pem with the name of your file, and the ~/Downloads/ with where it is if it isn't in downloads.) [Learn more about chmod](https://opensource.com/article/19/8/linux-chmod-command)

2. ssh into your server. You'll need to know what the public IP is (which you took note of in step 4 above). In this line, you should use the name of your pem file and your IP. Say yes to the prompt. 

```
ssh -i ~/.ssh/myserver.pem ubuntu@12.345.67.89
```

[Learn more about ssh](https://schh.medium.com/ssh-for-dummies-ea168e6ff547)

# Launching the ibex-maze sample
The fastest way to test that it's all working is to run the ibex-maze sample from your server.

1.(While ssh'd into the server) Install python 2.
``` 
sudo apt-get update
sudo apt install python2
```
say yes to prompt.

2. clone Ibex-with-Maze
```
git clone https://github.com/vboyce/Ibex-with-Maze.git
```

3. Test it:
```
cd Ibex-with-Maze/www
python2 server.py
```
In a web browser go to 12.345.67.89:3000 (use your servers IPv4 address that you used above). You should see the Ibex experiment.

# Your experiment 

For using the server with your experiment, there are two main considerations. One is how to copy files between your computer and the server. The other is how to not have the server disconnect while the experiment is running. 

## Copying your experiment to the server
I strongly recommend that you do your experiment development locally. When you can run the experiment just as you like it locally (i.e. on `localhost:3000`), then you're ready to copy it over. There are two options for transferring files between your computer and the server. 

### Option 1: use github (or gitlab or similar)
If you are saving your files to a github repo, you can use that as a transfer method. Make sure everything's committed, then ssh into the server (see above) and clone it to the server. If the project is private, you'll need to use your username and password.
```
git clone https://github.com/username/project.git
```

If you don't usually use git with terminal, you can learn more at [Git Guides](https://github.com/git-guides).

### Option 2: use scp
The other option is to use scp, which is a terminal tool for copying files to other servers. [Learn more about scp](https://linuxize.com/post/how-to-use-scp-command-to-securely-transfer-files/)
Say you have your experiment in the path `Research/my-ibex-experiment` Then, on your computer you would run the following to copy my-ibex-experiment over. 
``` cd ~/Research
scp -i ~/.ssh/myserver.pem -r my-ibex-experiment ubuntu@12.345.69.89:
```
If you then ssh into the server (see above) and do `ls` you will see the folder my-ibex-experiment. 

The key thing to remember is that scp is done from the local side, not the server side! When doing this, it's often helpful to have two terminal tabs open -- one on the server (it'll say that it's at ubuntu@ip-172-whatever) and one on local (where it'll say username@computername). Then you can check where files are located on the server or that they copied correctly. 

Sometimes, you may want to copy just one file to a specific place. For instance
``` 
cd ~/Research/my-ibex-experiment
scp -i ~/.ssh/myserver.pem fixed-file.txt ubuntu@12.345.69.89:my-ibex-experiment
```


## Running the experiment 
When running the experiment, you should use screen (or tmux) so that the server process keeps going even if your computer disconnects from the server. [Learn more about screen](https://linuxize.com/post/how-to-use-linux-screen/)
While ssh'd to the server,
```
screen
```
This starts a new screen, where you can enter commands as normal. Then you can launch your experiment.
```
cd ~/Research/my-ibex-experiment/www
python2 server.py
```
Now it's running, and you can disconnect from the screen by doing Ctrl-A Ctrl-D. Your terminal should go back to the previous display, but the experiment is still running (go to the website and check!). 

To get back to that screen (for instance to stop the experiment), you want to reconnect to the screen so do
``` screen -r
```

You can stop the experiment running with Ctrl+C. 

## Getting files back from the server
Now that you've run the experiment, you probably want the results files. Your options for copying the files off the server are the same as for copying files to the server. 

### Option 1: github
You could commit the results files from the server, push to the remote, and then pull them down only your local machine. If you're doing this and the repo is public, make sure you didn't collect any personally-identifying information that will be in the results files. You'll need to use your github username and password to authenticate.

If you don't usually use git with terminal, you can learn more at [Git Guides](https://github.com/git-guides).

## Option 2: scp
You ran your experiment and now you want to copy the results folder to your own computer. You'll need to know where the results folder is on the server -- say it's at `my-ibex-experiment/results`
From your computer, use cd to navigate to the folder you want to copy the results folder to.
``` cd ~/Research/my-ibex-experiment
```
Then use scp to copy the files.
```scp -i ~/.ssh/myserver.pem -r ubuntu@12.345.69.89:my-ibex-experiment/results . 
```
[Learn more about scp](https://linuxize.com/post/how-to-use-scp-command-to-securely-transfer-files/)

# Generalizations
* if you want to run multiple experiments at once, you can open up more ports, change the ports each experiment is running on to be all different, and use more screens to run them simultaneously. (Just keep track of what's running in which port and screen so you don't kill the wrong one by accident, or direct people to the wrong site!)

* This general process isn't just for running Ibex, it'll also work for other web-based experiments -- anything that you can run via terminal on localhost:3000, you can also run on your server in a similar way. Just make sure you install any dependencies needed on the server. (Example: I run experiments written with [Empirica](https://empirica.ly/) on an ec2 instance.)

* AWS EC2 instances happen to be the cloud service I use for running experiments. Aside from the EC2 specific set-up, the rest of the instructions will work for any server with open ports that you have ssh access to. Depending on the authentication method, you may not need to include `-i ~/.ssh/myserver.pem` in the ssh and scp lines, and may instead be asked for a password, or ssh keys may be used. 
