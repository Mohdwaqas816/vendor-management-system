# Vendor Management System with Performance Metrics

**Vendor Management System** using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics

## Pre-requisites

<details open>
<summary>Python 3.10 - 3.11</summary>
<br>

- [Python Download](https://www.python.org/downloads/)

</details>
<details open>
<summary>Code Editor (Preferred)</summary>
<br>

- [VS Code Download](https://code.visualstudio.com/download)
</details>

<details open>
<summary>Microsoft Visual Studio Build Tools (Optional)</summary>
<br>

- [Build Tool Download](https://visualstudio.microsoft.com/downloads/)
</details>

## Run Locally

Clone the project

```bash
  git clone https://github.com/Mohdwaqas816/vendor-management-system.git
```

Go to the project directory

```bash
  cd vendor_system
```

Create Virtual Environment (Suggested) [Link for Reference](https://virtualenv.pypa.io/en/latest/user_guide.html)

```bash
  # for windows os
  pip install virtualenv
  python -m virtualenv vendor-env     # you can choose the name whatever you want
  vendor-env\Scripts\activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python manage.py runserver 8000  # you can decide on which port you want to run
```

Confirm by pasting this url in browser

```bash
  http://127.0.0.1:8007/api/health/
```

### Woyila! congrats 🎊🎊🎉

## API Reference

#### Create a new vendor

```http
  POST /api/vendors/
```

| Parameter               | Type     | Description                             |
| :---------------------- | :------- | :-------------------------------------- |
| `name`                  | `string` | **Required**. name of vendor            |
| `contact_details`       | `string` | **Required**. Number of vendor          |
| `address`               | `string` | **Required**. address of vendor         |
| `vendor_code`           | `string` | **Required**. Unique code of vendor     |
| `on_time_delivery_rate` | `int`    | **Optional** Default - 0, between 0-100 |
| `quality_rating_avg`    | `int`    | **Optional** Default - 0, between 0-5   |
| `average_response_time` | `int`    | **Optional** Default - 0, between 0-100 |
| `fulfillment_rate`      | `int`    | **Optional** Default - 0, between 0-100 |

#### List all vendors

```http
  GET /api/vendors/
```

#### Retrieve a specific vendor's details

```http
  GET /api/vendors/{vendor_id}/
```

| Parameter | Type     | Description                         |
| :-------- | :------- | :---------------------------------- |
| `id`      | `string` | **Required**. Id of vendor to fetch |

#### Update vendor's detail

```http
  PUT /api/vendors/{vendor_id}/
```

| Parameter | Type     | Description                          |
| :-------- | :------- | :----------------------------------- |
| `id`      | `string` | **Required**. Id of vendor to update |

parameters you can update

```
{
        "name": "xyz",
        "contact_details": "123-456-789",
        "address": "xyz, street 22- 1105 Atlantis",
        "vendor_code": "ZUBDT",
        "on_time_delivery_rate": 5.0,
        "quality_rating_avg": 2.0,
        "average_response_time": 2.0,
        "fulfillment_rate": 0.0
}
```

#### Delete a vendor

```http
  DELETE /api/vendors/{vendor_id}/
```

| Parameter | Type     | Description                          |
| :-------- | :------- | :----------------------------------- |
| `id`      | `string` | **Required**. Id of vendor to delete |

# Rest Documentation coming soon...
