# truenas-backup

Scripts to (periodically) backup from truenas or any other unix-based NAS

## Deprecated

This script creates a backup using rsync, allowing it to run on any Linux machine. I am now running TrueNAS on my backup server, and am now using the TrueNAS snapshot replication feature. I have also written a script to perform these replication tasks on startup, and shutdown the system afterwards. See [WouterGritter/truenas-auto-replication](https://github.com/WouterGritter/truenas-auto-replication).
