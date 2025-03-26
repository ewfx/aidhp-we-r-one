# FinanceInsight Bank Application

## Overview

This Flask application provides a personalized financial overview and AI-driven product recommendations to users. It simulates a banking interface with a focus on customer engagement and insights. The application is designed with a clean, professional look and feel, inspired by the Wells Fargo theme.

## Artifacts:

- Demo Video: https://drive.google.com/file/d/1HBGjNPumqnTDPLUsUBTW1Gjo-4BiF2N3/view?usp=drive_link
- Presentation: https://docs.google.com/presentation/d/1n8dXNxeBCMWgDboJMoDpGiH-u3FXkbiXRzRtxvo5pd8/edit?usp=sharing
- Document: https://docs.google.com/document/d/1aTRgoR2ed3HDnGW9EHLjq0PUALrB0QJZoFGhj0NXQ9k/edit?tab=t.0

Screenshots:
![image](https://github.com/user-attachments/assets/f537c99b-5a8e-4060-b722-6d4cd5fb52ac)
![image](https://github.com/user-attachments/assets/8b7b4cf2-3e36-446d-a308-465cd6c4ee31)
![image](https://github.com/user-attachments/assets/0d8bb50f-212a-49aa-9610-8a87736897a7)
![image](https://github.com/user-attachments/assets/df55b791-f2fe-44e1-9b66-6697c37abac3)
![image](https://github.com/user-attachments/assets/a7aaf3f8-ec25-4ae6-a75d-535f66a6f2c6)
![image](https://github.com/user-attachments/assets/153d361b-a464-41b6-b992-b1d522032fb7)


**Architecture:**
![image](https://github.com/user-attachments/assets/41ec62db-382e-4432-a335-24f8d3629886)





## Features

-   **Customer Overview:** Displays key customer information, including personal details, financial summary, and account status.
-   **Engagement Metrics:** Visualizes customer engagement through interest, engagement, sentiment, and social media activity scores.
-   **Recent Transactions:** Shows a table of recent transactions with dates, amounts, and categories.
-   **AI-Recommended Products:** Offers personalized product recommendations based on the customer's profile.
-   **Admin View:** Provides an AI-generated customer persona and admin notes for bank employees (accessible via a tab).
-   **Database Integration:** Loads customer data and Wells Fargo product data from CSV files or sample data.
-   **AI Integration:** Uses Gemini AI to generate customer descriptions and product recommendations.

## Technologies Used

-   Flask: A Python web framework for building the application.
-   Tailwind CSS: A utility-first CSS framework for styling the user interface.
-   Gemini AI: Google's generative AI model for generating customer insights and product recommendations.
-   HTML/CSS/JavaScript: For building the frontend and interactivity.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up Gemini API key:**
    -   Obtain a Gemini API key from Google Cloud.
    -   Place the API key in the .env file
4.  **Prepare data:**
    -   Ensure that `Customer_DB/Customer_Data_with_Social_Media_Activity.csv` and `Product_DB/Wells_Fargo_Products_Full.csv` are in the correct directories or update the `CUSTOMER_DATA_CSV_URL` and `WELLS_FARGO_PRODUCTS_CSV_URL` variables in `app.py` with the correct paths or URLs.
5.  **Run the application:**
    ```bash
    python app.py
    ```
6.  **Access the application:**
    -   Open your web browser and navigate to `http://127.0.0.1:5000`.

## Application Structure

-   `app.py`: Contains the Flask application logic, including route definitions, data loading, and AI integration.
-   `index.html`: The main HTML template for the application's user interface.
-   `Customer_DB/Customer_Data_with_Social_Media_Activity.csv`: CSV file containing customer data.
-   `Product_DB/Wells_Fargo_Products_Full.csv`: CSV file containing Wells Fargo product data.
-   `static/`: Directory for static assets (e.g., CSS, JavaScript, images).
-   `templates/`: Directory for HTML templates.

## Important Considerations

-   **API Key Security:** Ensure that your Gemini API key is stored securely, preferably in environment variables, especially in a production environment.
-   **Data Paths:** Double-check the paths to your CSV data files to ensure they are correct.
-   **Error Handling:** Implement robust error handling to gracefully handle potential issues with data loading, API calls, and other operations.
-   **Scalability:** Consider scalability if you anticipate a large number of users.
-   **Security:** Implement appropriate security measures to protect user data and prevent vulnerabilities.

## Disclaimer

This application is a demo and uses sample data. It is not intended for production use with real customer data.

## 👥 Team
- **Eshaan Agarwal** - [[GitHub](https://github.com/Eshan-Agarwal16)]
- **Pranav Surendran** - [GitHub](https://github.com/Pranav418) 
- **Sharon A Sujitha** - [GitHub](https://github.com/sharonsujitha7) 
- **Shriroop Roychoudhury** - [GitHub](https://github.com/rshriroop01) 
- **Tejas C** - [GitHub](#) 
