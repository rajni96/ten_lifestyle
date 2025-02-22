# Booking API

## Overview
This project provides a RESTful API for managing bookings. It allows users to create and cancel bookings through defined endpoints.

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
  - [Booking Endpoints](#booking-endpoints)

## Setup Instructions

### Prerequisites
- Python 3.13+
- pip (Python package manager)
- virtualenv (recommended)

### Installation Steps

### Clone the repository:

`git clone git@github.com:rajni96/ten_lifestyle.git`

`cd ten_lifestyle`

### Create and activate virtual environment

`python -m venv venv`

`source venv/bin/activate`

### Install dependencies

`pip install -r requirements.txt`

### Run migrations

`python manage.py migrate`

### Load the CSV data

`python manage.py load_csv members.csv members`

`python manage.py load_csv inventory.csv inventory`

### Run the development server

`python manage.py runserver`

## API Documentation

### Booking Endpoints

#### 1. Book an Item
- **URL:** `/book/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "member": "<member_id>",
      "inventory": "<inventory_id>"
  }
  ```
- **Responses:**
  - **201 Created**
    ```json
    {
        "message": "Booking successful.",
        "booking_id": "<booking_id>"
    }
    ```
  - **400 Bad Request**
    ```json
    {
        "error": "<error_message>"
    }
    ```

#### 2. Cancel a Booking
- **URL:** `/cancel/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "booking_id": "<booking_id>"
  }
  ```
- **Responses:**
  - **200 OK**
    ```json
    {
        "message": "Booking canceled."
    }
    ```
  - **404 Not Found**
    ```json
    {
        "error": "Booking not found."
    }
    ```
  - **400 Bad Request**
    ```json
    {
        "error": "<error_message>"
    }
    ```

## Development

### Running Tests

`python manage.py test`

## Project Assumptions and Rationale

- Authentication is not implemented to keep the logic simple.
- CSV files are directly imported without validating the data Eg: booking count can be 3 for some users even though the max value can be 2.
- We are using SQLite as a database for easy development process.
- There is no atomic transaction handling done when booking or cancelling an inventory.
- Only basic test cases are implemented.