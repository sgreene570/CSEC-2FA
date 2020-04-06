# CSEC-2FA

[![Docker Repository on Quay](https://quay.io/repository/sgreene570/csec-2fa/status "Docker Repository on Quay")](https://quay.io/repository/sgreene570/csec-2fa)

A project by Joel Eager and Stephen Greene for CSCI 455.

# Building

Note, docker must be installed.

```bash
docker build -t csec-2fa .
```

See `requirements.txt` for a list of required python3 dependencies. The included `Dockerfile` lists the
required system packages for debian-based systems.

Alternatively, a pre-built docker image may be pulled from [quay.io](https://quay.io/repository/sgreene570/csec-2fa).

ex:
```bash
docker pull quay.io/sgreene570/csec-2fa
```

# Running

Start a bash session within the docker container.

```bash
./start-mysql.sh
docker run --network="host" -it csec-2fa /bin/bash
```

Now, the python3 files can be executed from within the docker container's shell.
The file `cli.py` is the only top-level python file available, and is the intended entry point.

```bash
python3 cli.py --help
```

# Example run through

First, make sure to initialize the database.

```bash
python3 cli.py init
```

Then, use `python3 cli.py --help` to see the available commands.

Example of using SMS method:

```bash
$ python3 cli.py send-text verizon 5855555555
Enter a gmail address to send from: sxg6123@g.rit.edu
Enter the password for that gmail account:
Sending OTP code ************ to 5855555555@vtext.com...
Sent
```

Corresponding validation code for SMS:

```bash
$ python3 cli.py auth-text verizon 5855555555
Enter the received code: Jaij538mKzux
Success
```


