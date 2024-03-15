**Language > Specialist**: Markdown > Documentation Specialist
**Includes**: Markdown formatting, Docker, GitLab, Jenkins, SonarQube, and Bash commands
**Requirements**: V=2 (simple), focus on clear and structured documentation, incorporating best practices for readability and user guidance
## Plan
1. Structure the README with headings for each major section.
2. Include an introduction and prerequisites.
3. Detail the setup and configuration steps.
4. Include additional tips and troubleshooting.
5. Add URLs and commands in a user-friendly format.

---

# SonarQube, Jenkins, and GitLab Setup Guide

## Introduction

This guide provides step-by-step instructions for setting up a CI/CD stack using SonarQube, Jenkins, and GitLab using Docker. This setup is ideal for implementing a robust continuous integration and delivery pipeline.

## Prerequisites

Before starting, ensure you have Docker and Docker Compose installed on your system. You will also need root access on the host machine to set recommended values.

## System Configuration

As a root user, run the following commands on the host machine:

```bash
sysctl -w vm.max_map_count=262144
sysctl -w fs.file-max=65536
ulimit -n 65536
ulimit -u 4096
```

## Docker Compose Setup

1. **Prepare the Docker Compose File**: Locate the `docker-compose.yml` file at `son_namespace/deploy/jenkins-gitlab-sonarqube-pg-docker/docker-compose.yml`. Feel free to modify this file as per your requirements.

2. **Set Environment Variables**: Before launching the containers, update these environment variables in your docker-compose file:
    - `GITLAB_SECRETS_DB_KEY_BASE`
    - `GITLAB_HOST`
    - `SONARQUBE_JDBC_PASSWORD`
    - `POSTGRES_PASSWORD`

## Launching the Containers

Run the following command to launch the stack:

```bash
docker-compose up -d
```

*Note: The installation process might take some time.*

## Verification

To verify if all systems are up and running, execute:

```bash
docker ps
```

## Accessing the Services

- **Jenkins**: [http://your-ip-address:8001/](http://your-ip-address:8001/)
- **SonarQube**: [http://your-ip-address:8005](http://your-ip-address:8005/)
- **GitLab**: [http://your-ip-address:8003](http://your-ip-address:8003/)

## GitLab Account Setup

- **Create a New Account**:
    1. Execute `docker exec -it gitlab-container /bin/bash`.
    2. Access the GitLab Rails Console: `gitlab-rails console -e production`.
    3. Create a new user:
        ```ruby
        user = User.new({
          email: 'son@gmail.com',
          username: 'son',
          name: 'TSon dep trai',
          password: 'son123aA@',
          password_confirmation: 'son123aA@'
        })
        user.save!
        user.confirm
        exit
        ```

## Resetting GitLab Root Password

1. Access the server/container where GitLab is running.
2. Open the Rails console: `gitlab-rails console`.
3. Reset the root password:
    ```ruby
    user = User.find_by(username: 'root')
    user.password = 'son123aA@'
    user.password_confirmation = 'son123aA@'
    user.save!
    exit
    ```

## Jenkins Initial Setup

1. Retrieve the initial admin password:
    ```bash
    docker exec -it <your-jenkins-container-id> cat /var/jenkins_home/secrets/initialAdminPassword
    ```
2. Follow the on-screen instructions to install suggested plugins.
3. Access Jenkins at [http://10.16.150.138:8001/jenkins](http://10.16.150.138:8001/jenkins).

## CI/CD in Vietnamese

For Vietnamese guides on CI/CD integration with Jenkins and GitLab, visit this [Cloud365 article](https://news.cloud365.vn/ci-cd-phan-3-huong-dan-tich-hop-jenkins-va-gitlab/).

## Tokens for Integration

- **GitLab Personal Access Token**: `glpat-XBdL2BEZQCTLZx6g1Jns`
- **Jenkins API Token**: `1115afb0b2f0f2151c791c5534b6c41d79`


## Adding Sonarqube to Jenkins 
[Sonarqube official docs](https://docs.sonarsource.com/sonarqube/9.8/analyzing-source-code/ci-integration/jenkins-integration/)

## Output
![Result](image.png)

## Additional Configurations and Tips

- Follow the steps for [Jenkins integration with SonarQube](https://docs.sonarsource.com/sonarqube/9.8/analyzing-source-code/ci-integration/jenkins-integration/).
- If you encounter issues with Java versions for Jenkins slaves, ensure Java 11 is set as the default version on your system.