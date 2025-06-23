## 🧑‍💼  User Management System

This project is a **Tkinter-based GUI application** built with Python. It manages user data, including personal details and addresses, and stores information using CSV files.

### 🚀 Features

* 🔐 **User Authentication**: Supports login with user ID and password.
* 👤 **User Management**:

  * Tracks number of users using a class variable
  * Allows setting and updating of personal details: name, phone, DOB, gender, etc.
* 🏠 **Address Handling**: Stores and manages address information like house number, city, pincode, and state.
* 💾 **Persistent Storage**: Reads and writes user data to a CSV file.
* 🖥️ **GUI Interface**: Built with Tkinter and ttk for modern widgets and interaction.

### 📁 Project Structure

* `Address` class:

  * Holds address-related information.
* `Person` class:

  * Manages user credentials and personal details.
  * Maintains a count of total users (`number_of_people`).
  * Includes methods to update user info.

### 🔧 Technologies Used

* Python 3.x
* Tkinter (`tk`, `ttk`, `messagebox`)
* CSV for data storage
* Regular expressions for validation

### ✅ Requirements

* Python 3.6+
* Tkinter (pre-installed with most Python distributions)

---
