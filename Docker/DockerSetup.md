# Docker Setup

## Windows 10

- **NOTE** You can use WSL 2 instead of Hyper-V with latest Docker Desktop for faster performance
  - Open Powershell as admin and enter: `Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-Hypervisor`
  - [Install the WSL 2 Linux Kernel](https://docs.microsoft.com/en-us/windows/wsl/wsl2-kernel)
    - Install a Linux distribution on Win 10 if needed
  - Restart mcahine
- Enable virtualization in Bios

  - `Advanced` -> `CPU Configuration`
  - May be under `Secure Virtual Machine` mode option

- Optional: Enable Hyper-V if needed:
  - open powershell as administrator
  - `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All`

## VS Code Extensions:

- Docker extension by MicroSoft
