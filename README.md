# E-Commerce Website

## 📌 Project Overview
This is a full-stack **E-Commerce Web Application** built using **Django** for the backend and **React.js** for the frontend. The platform allows users to browse products, add them to the cart, proceed to checkout, and manage their profiles.

## 🚀 Features
- 🔹 User Authentication (Login, Register, Logout)
- 🔹 Product Listings with Categories
- 🔹 Product Detail Page
- 🔹 Shopping Cart Functionality
- 🔹 Secure Checkout Process
- 🔹 Profile & Address Management
- 🔹 Order History & Tracking

## 🛠 Tech Stack
### Frontend:
- **React.js** - Component-based UI development
- **Bootstrap** - Responsive design
- **Axios** - API communication

### Backend:
- **Django** - Web framework for Python
- **Django REST Framework (DRF)** - API development
- **MySQL** - Database management
- **Stripe API** - Payment processing

## 📂 Project Structure
```bash
├── backend/        # Django backend files
│   ├── ecom/      # Main Django project
│   ├── app/       # Django app for e-commerce
│   ├── templates/ # HTML templates (if used)
│   ├── static/    # Static files like CSS, JS, images
├── frontend/       # React frontend
│   ├── src/       # React components
│   ├── public/    # Public assets
│   ├── package.json  # Frontend dependencies
│   ├── index.js   # Main entry point
│   ├── App.js     # Main App component
├── db.sqlite3      # SQLite database (if used)
├── manage.py       # Django management commands
```

## ⚙️ Setup Instructions
### 1️⃣ Backend Setup
```sh
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2️⃣ Frontend Setup
```sh
cd frontend
npm install
npm start
```

## 🔗 API Endpoints
### Authentication
- `POST /api/register/` - Register a new user
- `POST /api/login/` - Login user

### Products
- `GET /api/products/` - List all products
- `GET /api/products/<id>/` - Get product details

### Cart
- `POST /api/cart/add/` - Add product to cart
- `GET /api/cart/` - View cart items

### Orders
- `POST /api/checkout/` - Process order
- `GET /api/orders/` - View order history

## 📌 Future Enhancements
- ✅ Wishlist functionality
- ✅ User Reviews & Ratings
- ✅ Admin Dashboard

## 🤝 Contributors
- Nikhil - Developer

## 📜 License
This project is open-source and available under the **MIT License**.
