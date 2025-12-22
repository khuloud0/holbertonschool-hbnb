https://raw.githubusercontent.com/khuloud0/holbertonschool-hbnb/5f510bc079e1063d454d31a2fc6ffe69e3e35878/part1/1.%20Detailed%20Class%20Diagram%20for%20Business%20Logic%20Layer.svg

# **HBnB System Class Diagram**

## **Main Classes:**

### **1. User**
- **Attributes**: id, first_name, last_name, email, password, is_admin, created_at, updated_at
- **Methods**: register(), update(), delete()
- **Description**: Represents a system user, can be either regular user or administrator

### **2. Place**
- **Attributes**: id, title, description, price, latitude, longitude, created_at, updated_at
- **Methods**: create(), update(), delete(), list()
- **Description**: Represents a property available for rental, has geographic location and price

### **3. Review**
- **Attributes**: id, rating, comment, created_at, updated_at
- **Methods**: create(), update(), delete(), list_by_place()
- **Description**: Represents user reviews/ratings for properties

### **4. Annenity**
- **Attributes**: id, name, description, created_at, updated_at
- **Methods**: create(), update(), delete(), list()
- **Description**: Represents amenities/features available in properties

## **Key Notes:**
- Each class contains timestamps (created_at, updated_at) for tracking
- Each class has basic CRUD operations
- Review has a special method list_by_place() to show reviews by property
- The system is designed for easy extensibility with new classes
