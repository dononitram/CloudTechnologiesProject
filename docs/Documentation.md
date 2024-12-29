# Documentation

# 1. Introduction and Goals

This document follows the arc42 standard for software architecture documentation. The arc42 template provides a structured approach to capturing and communicating architectural decisions, design, and rationale.

## 1.1. Requirements Overview

The main goal of this project is to develop a system that integrates cloud services, machine learning models, and Excel functionalities for enhanced productivity and ease of use. The application must have the following functionalities:

- A cloud-hosted backend that manages data and handles user requests efficiently.
- A machine learning service to provide accurate predictions based on user inputs.
- An API integration for seamless communication between the backend, Excel, and the ML service.
- A user-friendly Excel interface to input data and display prediction results.
- A secure and scalable infrastructure to support multiple users and large datasets.

## 1.2. Quality Goals
| **Quality Goal**    | **Motivation**                                                                                                                           |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| **Efficiency**      | The system must process requests quickly and reliably to ensure a seamless user experience, especially for tasks involving Excel automation or predictions. |
| **Usability**       | The application must be intuitive and user-friendly to ensure that both non-technical users (working with Excel) and technical users can operate it easily. |
| **Maintainability** | The codebase should be clean and modular to allow for easy updates, including adding new machine learning models or changing integration endpoints. |
| **Scalability**     | The solution should handle increased usage, especially for larger datasets or multiple concurrent users accessing the machine learning services. |
| **Security**        | The application must protect sensitive data, including predictions and user inputs, while preventing unauthorized access to the system and its infrastructure. |


## 1.3. Stakeholders

| **Team**                  | **Name**                                   | **Expectations**                                                   |
|---------------------------|-------------------------------------------|-------------------------------------------------------------------|
| **Cloud Infrastructure Team** | • Donato Martín                        |  Build and maintain a secure and scalable cloud infrastructure.    |
|                           | • Adilet Dzhuraev                         |                                                                   |
|                           | • Nadir Mutallimov                        |                                                                   |
|                           | • Oğuzhan Demir                           |                                                                   |
|                           |                           |                                                                   |
| **Python Team**           | • Álvaro Tébar                            | Develop and integrate APIs and machine learning solutions.        |
|                           | • Baizhan Dossanov                        |                                                                   |
|                           | • Mohamed Bouguezine                      |                                                                   |
|                           | • Dashqin Mammadov                        |                                                                   |
|                           | • Mohammed Kadri                          |                                                                   |
|                           |                           |                                                                   |
| **Excel Integration Team** | • Marshal Tawanda Dhliwayo               | Automate and integrate Excel workflows with backend systems.      |
|                           | • Rusif Safarov                           |                                                                   |
|                           | • Ismail Talha Yanik                      |                                                                   |
|                           | • Eldar Zeynalli                          |                                                                   |
|                           | • Azad Azizade                            |                                                                   |


# 2. Constraints

## 2.1. Technical Constraints

| Constraint | Explanation |
| - | - |
| Oracle Cloud Infrastructure Hosting Solution | Oracle Cloud is used to host the project, providing scalability, security, and performance for the infrastructure.|
| Python Backend | The backend is developed in Python to handle API logic, data processing, and communication with machine learning services.|
| Python Machine Learning Service | Machine learning models are implemented to analyze data and provide predictions, such as in the Excel integration workflows.|
| Visual Basic Application in Excel |VBA in Excel is used to automate workflows, integrate with APIs, and streamline repetitive tasks for users. |

## 2.2. Organizational Constraints

| Constraint | Explanation |
| - | - |
| Team | Our team is divided into three sub-teams: Cloud Infrastructure, Python Development, and Excel Integration. Each team focuses on its specific domain for efficiency.|
| Time |  Deadline at the end of the semester, the time is divided among two hours per week of in-class work. We schedule multiple online meetings to catch up, give feedback, and set goals.|
| Tech Proficiency |Some members are still new to certain tools and technologies like Oracle Cloud and Python machine learning, necessitating a learning phase. |

## 2.3. Convention Constraints

| Constraint | Explanation |
| - | - |
| Clean Code | The code composing the application must prioritize clarity and cleanliness, facilitating comprehension and ease of maintenance in the long term. We adhere to camelCase for JavaScript and PascalCase for React, ensuring clear and descriptive names while steering clear of confusing prefixes. We need to adhere to the conventions of the programming languages we’re using, including JavaScript , HTML and CSS. |
| Arc42 | The project utilizes [Arc42](https://arc42.org/) for documentation purposes. |
| Usability | The application must be user-friendly, with a clean and intuitive interface that is easy to navigate. The user experience should be seamless and engaging, with a focus on accessibility and adaptability. So, to achieve this, we should use tools like Google LightHouse to measure the performance of the application. |

# 3. Context and Scope

# 4. Solution Strategy

# 5. Building Block View

# 6. Runtime View

# 7. Deployment View

# 8. Cross-Cutting Concepts

# 9. Architecture Decisions

The architecture decisions can be found in the Github Wiki: [Wiki ADRS](https://github.com/dononitram/CloudTechnologiesProject/wiki/ADRS)

# 10. Quality Requirements

# 11. Risks and Technical Debt

# 12. Glossary

# 13. References

# 13. Legend