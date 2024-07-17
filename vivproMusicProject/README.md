# vivproMusicProject

This project is a Django-based RESTful API for managing songs and their ratings. The project includes endpoints to list songs, retrieve individual songs, and rate songs.

## Features

- List all songs
- Retrieve details of a specific song
- Filter songs by title
- Rate a song
- Retrieve the rating of a song

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/Gullu06/vivproMusicProject.git
   cd vivproMusicProject

2. Create and activate a virtual environment:

  ```sh
  python -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install the dependencies:
  pip install -r requirements.txt

4. Apply the migrations:
  python manage.py migrate

5. **Load Sample Data**
```bash
    python manage.py import_songs path/to/your/data.json
```
e.g. :
```bash
  python manage.py import_songs "C:\Users\Priyanshi Chouhan\OneDrive\Documents\Python\vivproProject\vivproMusicProject\playlist.json"
```

5. Run the development server:
```bash
  python manage.py runserver
```

# Running Tests
```bash
  python manage.py test
```

# API Endpoints

- List Songs
  URL: /api/songs/
  Method: GET

- Retrieve a Song
  URL: /api/songs/{id}/
  Method: GET

- Rate a Song
  URL: /api/songs/{id}/rate/
  Method: PATCH

- Retrieve Song Rating
  URL: /api/songs/{id}/rate/
  Method: GET
