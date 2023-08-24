
# QR Code Generator
The QR Code Generator is a simple web application built using Flask that allows users to generate QR codes from URLs. Users can enter a URL, and the application will fetch the QR code image using an external API and display it on the web interface.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

## Features
- Generate QR codes for URLs.
- Utilize the easy-qr-code API for QR code generation.
- Implement caching to reduce API requests for the same content.
- Input validation and error handling.
- Scheduled cleanup of generated QR code images.
- Unit tests for critical functions.

## Getting Started
### Prerequisites
Before running the application, ensure you have the following:
- Python 3.x installed
- An internet connection (for fetching QR code images)
- A valid API key for the RapidAPI QR Code Generator API

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/math002/qr-code-generator.git
   ```
2. Navigate to the project directory:
   ```sh
   cd qr-code-generator
   ```
3. Navigate to the project directory:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up your [RapidAPI key](https://rapidapi.com/ariefsam/api/easy-qr-code) in the '.env' file.

## Usage
1. Run the application:
   ```sh
   python main.py
   ```
2. This will start the Flask development server, and you should see output indicating that the server is running.
3. Open your web browser and go to 'http://localhost:5000'.
4. Enter a URL into the input field and click the "Generate QR Code" button.
5. The application will generate a QR code for the provided URL using the easy-qr-code API.
6. The generated QR code will be displayed on the page.
7. You can also see a list of previously generated QR codes on the same page.

## Features

-   Generates QR codes from URLs.
-   Caches QR code images to improve performance.
-   Provides error messages for invalid inputs and API errors.
-   Implements content security policies for enhanced security.
-   Utilizes logging for troubleshooting and monitoring.
-   Supports basic unit tests for key functionality.

## Technologies Used
-   Python
-   Flask
-   Requests
-   APScheduler
-   MarkupSafe
-   dotenv
-   cachetools

## Future Ideas

Here are some ideas and features that could be implemented in the future:

- User authentication and login functionality to enable users to create accounts and access their own QR code history.
- Implement a gallery where users can view previously generated QR codes and manage their saved QR codes.
- Enhance the UI/UX of the web application to make it more intuitive and user-friendly.
- Integrate more customization options for QR codes, such as color schemes, logos, and sizes.
- Optimize the application's performance and scalability for larger user bases.
- Provide detailed usage documentation and examples for developers who want to contribute to the project.

These ideas showcase the potential growth and improvement of the QR Code Generator application. Feel free to contribute your own ideas and suggestions!

## Contributing
Contributions are welcome! If you find a bug, want to improve the code, or add new features, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature:
```bash
  git checkout -b feature-name
```
3. Make your changes and commit them: 
```bash
  git commit -m "Add your message here"
```
4. Push your changes to your forked repository:
```bash
   git push origin feature-name
```
5. Create a pull request in the original repository.