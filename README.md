# SMT_Project_Experience
Repository for SMT Project Experience

## How to Install and Run the Web Application (for Developers) ##
1. Install nodejs
    * To check if you have node installed run ```node --version``` in your terminal or command line
    * If you do not have node installed, you may install it through this [link](https://nodejs.org/en/download/)

2. Open the repository and enter the directory by running  ```cd app\vue``` in the terminal.

3. Open another terminal and connect to the APIs by running  ```uvicorn app.main:app --reload``` in the terminal. Ensure that you are connected to SMU's VPN.

4. Run ```npm install``` to download the necessary dependencies.

5. Run ```npm run dev``` to start a development environment. 

6. Visit [localhost:3000](http://localhost:3000/) to view the application. 

The steps above work for both Mac and Windows OS