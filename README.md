# MealPlan Tracker

The MealPlan Tracker is a Python web application aimed at helping college students track their meal plan spending habits in order to minimize personal money loss. The application was built using the Flask framework with other extensions and packages, Bootstrap templates with additional styling (HTML/CSS) and the ORM SQLALchemy working with a Postgres database for deployment. The app is currently live on Heroku: http://mp-tracker.herokuapp.com/home

<img src="https://i.imgur.com/gfqbuDi.png">
<img src="https://i.imgur.com/BLw0Fcg.png">
<img src="https://i.imgur.com/5o2cs25.png">
<img src="https://i.imgur.com/MvPBUBg.png">

## Purpose

At my university, students with a meal plan are given a set amount of money into their ID card to use for food on campus. Due to the several food locations to choose from, how much you choose to spend in a day can vary. One day, you might choose to spend only $7...or $18, if you decide to eat from the more expensive locations. Either way, however much you spend will be deducted from your current meal plan total. What this means is that if you are not aware of your spending habits, your meal plan can reach $0 before the end of the semester. 

Thus, to survive of course, you’d have to add your own money into your meal plan account to continue to buy food. This application will handle all the work in forecasting whether your meal plan will last or not. With both outcomes, it will tell you additional useful details such as how much money you’ll lose/save, an estimated end date for your meal plan and a suggested amount to spend everyday to avoid adding your own money.

___

There are two main sections for people to use.

## Home Page

<img src="https://i.imgur.com/7hwXg0F.png">

The home page is designed for people to immediately see if their meal plan will last. There is no saved data. You input two important details into a form regarding your spending habits and all the information you’d need to know is displayed.

## User’s Profile Page

The user’s profile contains a personal dashboard based on their data. It is designed for people to log their past data, as well as to get a helpful visualization on their projected result. This data visualization emphasizes how much money you’d save or lose.

By highlighting this piece of information, the gain/loss field becomes a key detail to the user. If it is positive, then that lets you know that your meal plan will last. If it is negative, then that number is how you much you’d have to add to your meal plan.

<img src="https://i.imgur.com/EIlScSV.png">
<img src="https://i.imgur.com/9ElcAbx.png">
