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
docker pull quay.io/sgreene/csec-2fa
```

# Running

```bash
./start-mysql.sh
docker run --network="host" -it csec-2fa /bin/bash
```

Now, the python3 files can be executed from within the docker container's shell.

```bash
python3 cli.py --help
```
