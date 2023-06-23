# TASK MANAGER


Task Manager is a task management system. It provides a platform for creating tasks, assigning them to individuals, and tracking their statuses. Registration and authentication are required to access the system.

## Features
* User registration and authentication
* User registration and authentication
* Task creation and assignment
* Task status management
* Task labels for organization


[Live view here](https://python-project-lvl4-production-5698.up.railway.app/)

## Installation


1. Make sure you have Docker and Docker Compose installed on your machine.

2. Clone the repository:

3. Navigate to the project directory:

```
cd task-manager
```
4. Copy the .env_example file to .env:
```
cp .env_example .env
```
5. Edit the .env file and configure the environment variables according to your preferences.

6. Build and run the Docker containers:

```
docker-compose up
```
7. Wait for the containers to be built and the application to start. You can access Task Manager in your browser at http://localhost:8000.

## Usage
1. Open your web browser and navigate to http://localhost:8000.
2. Register a new account by providing the required information.
3. Log in with your credentials.
4. Start creating tasks by clicking on the "New Task" button.
5. Assign tasks to users by selecting them from the list.
6. Update the status of tasks as they progress. You can change the status from "Open" to "In Progress" to "Completed" or any other relevant status.
7. Attach labels to tasks to categorize and organize them based on your needs.
8. Use the various features of Task Manager to effectively manage your tasks and collaborate with your team.


## Сode quality

| codeclimate | coverage | tests |
|:---:|:---:|:---:|
| [![codeclimate](https://api.codeclimate.com/v1/badges/52d3833c844707328f27/maintainability)](https://codeclimate.com/github/Nella611/python-project-lvl4/maintainability) | [![Test Coverage](https://api.codeclimate.com/v1/badges/52d3833c844707328f27/test_coverage)](https://codeclimate.com/github/Nella611/python-project-lvl4/test_coverage) | [![Actions Status](https://github.com/Nella611/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/Nella611/python-project-lvl4/actions) |


