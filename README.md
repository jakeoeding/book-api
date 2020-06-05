# Book Api

Basic RESTful api with book data

## Usage

### List all books

**Definition**

`GET /books`

**Response**

- `200 OK` on success

```json
[
    {
        "id:": "1",
        "title": "Moby-Dick",
        "author": "Herman Melville",
        "isbn": "9781503280786",
        "category": "fiction"
    },
    {
        "id:": "2",
        "title": "American Kingpin",
        "author": "Nick Bilton",
        "isbn": "9781591848141",
        "category": "nonfiction"
    }
]
```

**Definition**

`POST /books/`

**Arguments**

- `"title":string` book title
- `"author":string` author full name
- `"isbn":string` the 13 digit ISBN related to the title
- `"category:string"` the type of book: either fiction or nonfiction

**Response**

- `201 Created` upon success

```json
{
    "id:": "1",
    "title": "Moby-Dick",
    "author": "Herman Melville",
    "isbn": "9781503280786",
    "category": "fiction"
}
```
