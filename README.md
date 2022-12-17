# Shippio backend API assignment

#### Prerequisites

- Python
- Pipenv
- Docker
- Postmam

##### Installation

- Run the `pipenv shell` on the project root directory
- Run `docker-compose up --build`
- Run `docker exec -it vms_service_1 sh` and use `python manage.py createsuperuser` to create a super admin user

  > **_NOTE: This will save you some addition setting up time_** :
  > `username: admin password: shippio123`

- Inport these files into postman

  ```
  VMS.postman_collection.json
  vms_env.postman_environment.json
  ```

- Use Postman Collection Runner to generate users for the project

- Use the Runner on `Users` folder and set the loop to <number of wanted users> and daley to 10ms

  > \*\*\_NOTE: Make sure you have this options toggled on
  > 1- Keep variable values`
  > 2- Save Cookies after collection
  > To switch users - simply change the number on authorization tab
