<!--
  github.com/Ash5457 profile
  assets/header.svg     built by scripts/build_header.py
  metrics.terminal.svg  rendered by lowlighter/metrics
  Both refresh daily via .github/workflows/profile.yml
-->

<p align="center">
  <img src="assets/header.svg" alt="ash@fedora running fastfetch: Akash Bahl, IT support moving into security. CompTIA A+ certified, working toward a Microsoft Azure/M365 cert. Windows Server AD and Tailscale labs. Keswick, Ontario. Open to helpdesk and junior SOC roles." />
</p>

<p align="center">
  <img alt="Windows Server" src="https://img.shields.io/badge/Windows%20Server-161b22?style=flat-square&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAyNCAyNCc%2BPGcgZmlsbD0nbm9uZScgc3Ryb2tlPScjM2ZiOTUwJyBzdHJva2Utd2lkdGg9JzInPjxyZWN0IHg9JzMnIHk9JzMuNScgd2lkdGg9JzE4JyBoZWlnaHQ9JzcnIHJ4PScxLjUnLz48cmVjdCB4PSczJyB5PScxMy41JyB3aWR0aD0nMTgnIGhlaWdodD0nNycgcng9JzEuNScvPjwvZz48ZyBmaWxsPScjM2ZiOTUwJz48Y2lyY2xlIGN4PSc3JyBjeT0nNycgcj0nMS4zJy8%2BPGNpcmNsZSBjeD0nNycgY3k9JzE3JyByPScxLjMnLz48L2c%2BPC9zdmc%2B" />
  <img alt="Active Directory" src="https://img.shields.io/badge/Active%20Directory-161b22?style=flat-square&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAyNCAyNCc%2BPGcgZmlsbD0nbm9uZScgc3Ryb2tlPScjM2ZiOTUwJyBzdHJva2Utd2lkdGg9JzInPjxyZWN0IHg9JzguNScgeT0nMi41JyB3aWR0aD0nNycgaGVpZ2h0PSc1LjUnIHJ4PScxJy8%2BPHJlY3QgeD0nMi41JyB5PScxNicgd2lkdGg9JzcnIGhlaWdodD0nNS41JyByeD0nMScvPjxyZWN0IHg9JzE0LjUnIHk9JzE2JyB3aWR0aD0nNycgaGVpZ2h0PSc1LjUnIHJ4PScxJy8%2BPHBhdGggZD0nTTEyIDh2NE02IDE2di00aDEydjQnLz48L2c%2BPC9zdmc%2B" />
  <img alt="PowerShell" src="https://img.shields.io/badge/PowerShell-161b22?style=flat-square&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAyNCAyNCc%2BPHBhdGggZmlsbD0nbm9uZScgc3Ryb2tlPScjM2ZiOTUwJyBzdHJva2Utd2lkdGg9JzIuNicgc3Ryb2tlLWxpbmVjYXA9J3JvdW5kJyBzdHJva2UtbGluZWpvaW49J3JvdW5kJyBkPSdNNCA2bDYgNi02IDZNMTIuNSAxOEgyMCcvPjwvc3ZnPg%3D%3D" />
  <img alt="Fedora Linux" src="https://img.shields.io/badge/Fedora%20Linux-161b22?style=flat-square&logo=fedora&logoColor=3fb950" />
  <img alt="Bash" src="https://img.shields.io/badge/Bash-161b22?style=flat-square&logo=gnubash&logoColor=3fb950" />
  <img alt="Python" src="https://img.shields.io/badge/Python-161b22?style=flat-square&logo=python&logoColor=3fb950" />
  <br />
  <img alt="Tailscale" src="https://img.shields.io/badge/Tailscale-161b22?style=flat-square&logo=tailscale&logoColor=3fb950" />
  <img alt="WireGuard" src="https://img.shields.io/badge/WireGuard-161b22?style=flat-square&logo=wireguard&logoColor=3fb950" />
  <img alt="Wireshark" src="https://img.shields.io/badge/Wireshark-161b22?style=flat-square&logo=wireshark&logoColor=3fb950" />
  <img alt="VMware" src="https://img.shields.io/badge/VMware-161b22?style=flat-square&logo=vmware&logoColor=3fb950" />
  <img alt="TryHackMe" src="https://img.shields.io/badge/TryHackMe-161b22?style=flat-square&logo=tryhackme&logoColor=3fb950" />
</p>

### `$ cat about.txt`

I learn by building on my own hardware, then writing up what broke and how I fixed it. Each writeup covers the goal, the setup, and the troubleshooting log.

### `$ ls ~/projects`

**[secure-remote-access](https://github.com/Ash5457/secure-remote-access)** · `RDP` `Tailscale` `WireGuard` `Windows Firewall` `Fedora`\
Encrypted remote desktop from a Fedora laptop to a Windows 11 Pro machine over public Wi-Fi, with RDP never exposed to the internet. Walks through a layer-by-layer diagnosis of a Kerberos/NTLM logon failure and a routing conflict between two WireGuard-based tools.

**[ad-lab](https://github.com/Ash5457/ad-lab)** · `Windows Server` `AD DS` `PowerShell` `Group Policy` `DNS`\
An Active Directory domain built entirely from PowerShell scripts on Server 2016, then migrated side by side to Server 2025: schema extension, replication checks, all five FSMO roles transferred, a scream test with the old DC powered off, a clean demotion and the functional-level raise. Every step links to a screenshot or transcript, and the [troubleshooting log](https://github.com/Ash5457/ad-lab/blob/main/TROUBLESHOOTING.md) covers 11 problems, including a DC blue-screening mid-migration.

**[fedora-hardening](https://github.com/Ash5457/fedora-hardening)** · `LUKS` `btrfs` `systemd` `firewalld` `SELinux` `Bash` · *in progress*\
Auditing and hardening my daily-driver Fedora laptop across eight modules: disk, packages, logs, systemd, sudo, firewalld, SELinux and power. Each module records the findings, the changes, how I verified them and how to roll back. Every output is redacted and scanned for secrets by script before it is published. [Module 01](https://github.com/Ash5457/fedora-hardening/blob/main/01-disk-layout/NOTES.md) maps the LUKS2 and btrfs layout and backs up the LUKS header off-machine.

**[HackDetect](https://github.com/Ash5457/HackDetect)** · `Python` `OOP`\
Terminal social deduction game built for a university game studies course. Analysts investigate a simulated breach while one player may secretly be the attacker planting false evidence.

### `$ ssh Ash5457@metrics`

<p align="center">
  <img src="metrics.terminal.svg" alt="GitHub activity rendered as a terminal session, regenerated daily by GitHub Actions" />
</p>

### `$ ./contact.sh`

[LinkedIn](https://www.linkedin.com/in/akashbahl-toronto/) · [akashbahl1926@gmail.com](mailto:akashbahl1926@gmail.com)
