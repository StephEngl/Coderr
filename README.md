# Coderr Django Project

Coderr provides the robust backend infrastructure necessary to power a dynamic freelancer developer platform. Built with Python, Coderr offers a secure and scalable foundation for connecting clients with talented developers. Key features include a comprehensive API for seamless data exchange, a secure authentication system to protect user data, and thorough testing to ensure reliability and stability.

## ✨ Features

- 🌐 Api
- 🔐 Auth
- 🧪 Testing


## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/-Python-blue?logo=python&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-636363?logo=django&logoColor=white&style=flat)

## 🚀 Getting Started

Follow these steps to set up and run the project locally.


### ⚙️ Prerequisites

- Python 3.10+
- pip (Python package manager)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended)

### 📦 Installation

1. **Clone the repository**
    ```sh
    git clone https://github.com/StephEngl/Coderr.git
    cd Coderr
    ```

2. **Create and activate a virtual environment**
    ```sh
    python -m venv env
    source env/Scripts/activate  # On Mac: env\bin\activate
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations**
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser (optional, for admin access)**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server**
    ```sh
    python manage.py runserver
    ```

7. **If your frontend uses guest users, create one for business and customer user in the admin panel:**
    - Go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).
    - Create a business user with:
        - Username: `GuestBusiness`
        - Email: `business.guest@coderr.de`
        - Password: `321Coderr987+`
    - Create a customer user with:
        - Username: `GuestCustomer`
        - Email: `customer.guest@coderr.de`
        - Password: `321Coderr987+`
     - **Important:** Go to "User profiles" and create one for each user.
          
    > **Note:** Don't forget to add the Guest user information to your frontend configuration so it can authenticate as the guest user.

## 📚 API Documentation

This project includes automatically generated API documentation with Swagger UI and Redoc.

- The OpenAPI schema is available at:  
  `/api/schema/`

- Interactive Swagger UI can be accessed at:  
  `/api/schema/swagger-ui/`  
  Use this web interface to explore and test the API endpoints easily.

- Alternative documentation with Redoc is available at:  
  `/api/schema/redoc/`

These endpoints are integrated using [drf-spectacular](https://github.com/tfranzel/drf-spectacular) and configured in the Django URL patterns for convenient API exploration during development and testing.

## 📁 Project Structure

- [`core`](core) – Project configuration, global settings, and root URLs
- [`app_auth`](app_auth) – Handles user authentication, login, and registration
- [`app_meta`](app_meta) – Provides general platform information and metadata
- [`app_offers`](app_offers) – Manages offer creation, updates, and retrieval
- [`app_orders`](app_orders) – Handles order creation, management, and statistics
- [`app_reviews`](app_reviews) – Manages user reviews and feedback functionality

### 🔗 API Endpoints

#### 🛡️ Authentication
- `POST /api/login/` – Login
- `POST /api/registration/` – Register

#### 📊 Meta
- `GET /api/base-info/` – Retrieve base information

#### 👤 Profile
- `GET /api/profile/{user_id}/` – Retrieve user profile
- `PATCH /api/profile/{user_id}/` – Partial-update userprofile
- `GET /api/profiles/business/` – List all business-user-profiles
- `GET /api/profiles/customer/` – List all customer-user-profiles

#### 🛒 Orders
- `GET /api/completed-order-count/{business_user_id}/` – Get the number of completed orders for a business user
- `GET /api/order-count/{business_user_id}/` – Get the total number of orders for a business user
- `GET /api/orders/` – List all orders
- `POST /api/orders/` – Create a new order
- `PATCH /api/orders/{id}/` – Partially update an order
- `DELETE /api/orders/{id}/` – Delete an order

#### 🎁 Offers
- `GET /api/offerdetails/{id}/` – Retrieve offer details
- `GET /api/offers/` – List all offers
- `POST /api/offers/` – Create a new offer
- `GET /api/offers/{id}/` – Retrieve a specific offer
- `PATCH /api/offers/{id}/` – Partially update an offer
- `DELETE /api/offers/{id}/` – Delete an offer

#### 📝 Reviews
- `GET /api/reviews/` – List all reviews
- `POST /api/reviews/` – Create a new review
- `PATCH /api/reviews/{id}/` – Partially update a review
- `DELETE /api/reviews/{id}/` – Delete a review

## 🔒 Security Information

- **Secret Key:** Never share your Django `SECRET_KEY`. Use environment variables for production.
- **Debug Mode:** Set `DEBUG = False` in production.
- **Allowed Hosts:** Update `ALLOWED_HOSTS` in `settings.py` for your deployment.
- **Passwords:** Change default passwords (like the Guest user) in production.
- **Database:** Use strong credentials and restrict access.
- **HTTPS:** Always use HTTPS in production.
- **Admin Panel:** Restrict admin access and use strong passwords.
- **.env Files:** Make sure `.env` files are not pushed to the repo (see `.gitignore`).
- **Database Files:** Do not commit database files (`*.sqlite3`).

## 👥 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/StephEngl/Coderr/.git`
3. **Create** a new branch: `git checkout -b feature/your-feature`
4. **Commit** your changes: `git commit -am 'Add some feature'`
5. **Push** to your branch: `git push origin feature/your-feature`
6. **Open** a pull request

Please ensure your code follows the project's style guidelines and includes tests where applicable.

---

For more details, see the [`core/settings.py`](core/settings.py ) and [`core/urls.py`](core/urls.py ) files.
