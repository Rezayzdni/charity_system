# Charity System

## Overview

Charity System is a web-based platform designed to connect charitable organizations with benefactors (volunteers). The platform allows charities to create tasks and assign them to benefactors based on their availability and preferences. This project is built using Django for the backend and React for the frontend.

---

## Features

### Backend

- **Custom User Model**: Extends Django's `AbstractUser` to include additional fields like phone, address, gender, age, and description.
- **User Types**:
  - **Benefactors**: Volunteers with experience levels (Beginner, Intermediate, Expert) and weekly free time.
  - **Charities**: Organizations with unique registration numbers.
- **Task Management**:
  - Tasks can be created by charities with details like title, description, date, and filters (age/gender limits).
  - Tasks go through states: Pending → Waiting → Assigned → Done.
- **APIs**: RESTful endpoints for user management, charity/benefactor profiles, and task operations.
- **Database**: SQLite for development.
- **Testing**: Includes test cases for user registration, login, and task management.

### Frontend

- **React**: Used for building the user interface.
- **Routing**: Protected routes based on user type (stored in `localStorage`).
- **UI Frameworks**: Bootstrap and Reactstrap for responsive design.
- **API Integration**: Axios for communication with the backend.
- **Pages**:
  - Authentication
  - Tasks List 
  - Benefactor Profile
  - Charity Profile

---

## Technologies Used

### Backend

- **Django**: Web framework for building the backend.
- **Django REST Framework (DRF)**: For creating RESTful APIs.
- **SQLite**: Lightweight database for development.
- **django-cors-headers**: To handle Cross-Origin Resource Sharing (CORS).

### Frontend

- **React**: JavaScript library for building user interfaces.
- **React Router**: For client-side routing.
- **Bootstrap & Reactstrap**: For responsive and modern UI design.
- **Axios**: For making HTTP requests to the backend.

---

## Project Structure

### Backend

- **accounts**: Handles user authentication and profile management.
- **charities**: Manages charity and benefactor profiles, as well as task creation and assignment.
- **about_us**: Displays information about the platform members.
- **tests**: Contains test cases for backend functionality.

### Frontend

- **Pages**: Contains React components for different pages (e.g., Authentication, Tasks, Profiles).
- **Components**: Reusable UI components like Navbar and Login.
- **Public**: Static files like `index.html` and images.

---

## How to Run

### Backend

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend

1. Navigate to the `front` directory:
   ```bash
   cd front
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

---

## Future Improvements

- Implement real-time notifications for task updates.
- Enhance task filtering options.
- Deploy the application to a cloud platform.

---

## License

This project is licensed under the MIT License.
