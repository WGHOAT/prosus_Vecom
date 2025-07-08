# Prosus Vecom

## Project Description

Prosus Vecom is a voice-controlled e-commerce application that allows users to interact with an online store using voice commands. The application uses a combination of voice recognition, web scraping, and a large language model (LLM) to provide a seamless and intuitive user experience.

## Features

- **Voice-controlled navigation:** Navigate the application and browse products using voice commands.
- **Product search:** Search for products by voice and view the search results on the screen.
- **Product details:** Get detailed information about a product, including its price, description, and customer reviews.
- **Shopping cart:** Add products to your shopping cart and view the contents of your cart.
- **Checkout:** Complete the checkout process and purchase the items in your shopping cart.

## Installation

To install the application, you will need to have the following dependencies installed:

- Python 3.13
- Node.js
- npm

Once you have these dependencies installed, you can clone the repository and install the required packages by running the following commands:

```
git clone https://github.com/your-username/prosus-vecom.git
cd prosus-vecom
pip install -r requirements.txt
cd react-app
npm install
```

## Usage

To run the application, you will need to start the backend server and the frontend application.

To start the backend server, run the following command from the root directory of the project:

```
uvicorn app.main:app --reload
```

To start the frontend application, run the following command from the `react-app` directory:

```
npm start
```

Once the application is running, you can access it by opening a web browser and navigating to `http://localhost:3000`.