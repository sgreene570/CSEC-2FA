# CSEC-2FA

[![Docker Repository on Quay](https://quay.io/repository/sgreene570/csec-2fa/status "Docker Repository on Quay")](https://quay.io/repository/sgreene570/csec-2fa)

A project by Joel Eager and Stephen Greene for CSCI 455.

# Building

Note, docker must be installed.

```bash
docker build -t csec-2fa .
```

See the `Dockerfile` for instructions on manual python dependency installation.

# Running

```bash
./start-mysql.sh
docker run --network="host" csec-2fa
```
