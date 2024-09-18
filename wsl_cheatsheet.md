# WSL Cheat Sheet

## List and Manage WSL Instances

- **List all distributions with status:**
  ```bash
  wsl --list --verbose
  ```

- **Shut down all WSL instances:**
  ```bash
  wsl --shutdown
  ```

- **Terminate a specific distribution:**
  ```bash
  wsl --terminate <DistributionName>
  ```
  Example:
  ```bash
  wsl --terminate Ubuntu-22.04
  ```

- **Unregister (remove) a distribution:**
  ```bash
  wsl --unregister <DistributionName>
  ```
  Example:
  ```bash
  wsl --unregister Ubuntu
  ```

- **Install WSL (if not already installed):**
  ```bash
  wsl --install
  ```

- **Set default WSL distribution:**
  ```bash
  wsl --set-default <DistributionName>
  ```
  Example:
  ```bash
  wsl --set-default Ubuntu
  ```

- **Exit WSL:**
  ```bash
  exit
  ```

- **Install a specific distribution:**
  ```bash
  wsl --install -d <DistributionName>
  ```
  Example:
  ```bash
  wsl --install -d Ubuntu
  ```
