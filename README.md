# CSEC-2FA

A project by Joel Eager and Stephen Greene for CSCI 455.

# Building

Note, docker must be installed.

```bash
docker build -t csec-2fa .
```

# Running

```bash
./start-mysql.sh
docker run --network="host" csec-2fa
```
