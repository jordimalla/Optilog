# Optilog

Optilog is a Django web application designed for logistics optimization in the meat industry. It manages transportation logistics between farms and slaughterhouses, optimizing routes and minimizing operational costs.

## Features

- **Data Management**: Register farms, slaughterhouses, slaughterhouse demands, farm animal supplies, travel costs, and maximum weekly transport capacities.
- **Advanced Modeling**: Utilizes advanced linear programming techniques to find optimal solutions.
- **Intuitive Interface**: Facilitates data input and management through a user-friendly web interface.
- **Results Visualization**: Provides visual tools for analyzing and visualizing optimization solutions.

## Installation with Docker

To install and run Optilog using Docker, follow these steps:

1. Clone the repository from GitHub:

   ```bash
   git clone https://github.com/jordimalla/Optilog.git
   cd Optilog

2. Build and start the Docker containers using Docker Compose:
   ```bash
   docker-compose up -d --build
This command builds the Docker images and starts the containers in detached mode.

3. Access the application in your web browser at http://localhost:8000.

4. Create a superuser for the Django application inside the Docker container:

   ```bash
   docker-compose exec web python manage.py createsuperuser

## Usage

1. Register farms and slaughterhouses, along with supply and demand information.
2. Input transportation costs and weekly maximum capacities.
3. Run optimization to obtain the best routes and transport assignments.
4. Visualize results and adjust parameters as needed.

## Stopping the Application
To stop and remove the Docker containers created by Docker Compose, run:

   ```bash
   docker-compose down
   ``````
## Contributions

Contributions are welcome! If you want to improve Optilog, please follow these steps:

- Fork the repository.
- Create a new branch (git checkout -b feature/improvement).
- Make your changes and commit them (git commit -am 'Add some awesome feature').
- Push to the branch (git push origin feature/improvement).
- Create a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
