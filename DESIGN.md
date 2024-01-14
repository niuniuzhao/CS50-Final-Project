Here is a tour of the main labour-intensive technical manoeuvres and/or functions deployed to back up the project.

## app.py
- Started with the usual imports and configurations; note that json is imported for later use with Javascript.
- def lucky() is the function that gives the user an artwork page at random. It does so by randomly generating an integer in the range of artwork IDs stored in the artwork database, and then calling the artwork page associated with that artwork ID.
- def catalog() is the function that extracts artwork information from the artwork database and hands it over for catalog.html to render.
- def artwork(id) uses a couple of SQLite3 queries to extract information about: the artwork with the given id number, the rating and commentary information of all users, and the rating and commentary information of the particular user in session. The pieces of information are then handed over to the HTML page to be variously displayed.
- def review() is the function that allows the HTML review form on an artwork page to be submitted and recorded in the reviews database.  The function checks for the validity of inputs before uploading inputs into the database.
- def deletereview() does the opposite. The function searches for the review to be deleted in the reviews database via the user ID and artwork ID passed to it by the HTML form.
- def mycollection(), similar to def catalog(), prints the user’s review history by extracting information from the artwork database and the review database, ordering it by time.
- def register() takes username and password inputs via HTML forms, checks for validity, and uploads information to the users database.
- def login() takes username and password inputs via HTML forms, checks for validity against the users database, and logs the user in.
- def password() allows the user to change password. It does so by taking username, old password, new password inputs via HTML forms, checking validity against the users database and updating the users database.
- app.py sometimes call the functions in helpers.py. The apology function renders customised apology page with apology message as a variable. The login required function makes sure the user is directed to the login page when access is not allowed.

## Javascript
- The Javascript associated with artwork.html backs up the five-star rating interface, and communicates with the backstage databases via app.py.
  - In general, the strategy is to (a) associate each star in a five-star bar with an integer, so that the star’s “value” can be compared with values in the database, and (b) add on-click functions to control the status of stars, which can then be styled in css.
  - More specifically, for the first bar of stars, which the user can interact with, the script is told by app.py whether there is already a rating/review associated with this user + artwork combination in the database. If there is, the script identifies the star with the corresponding integer, and the CSS script colours the star(s). If there isn’t the script listens for the users clicks, and submits the value of that star when the submit button is hit.
- For the second bar of stars, which the user cannot interact with, the script gets the average rating value from app.py and asks CSS to highlight the star(s) associated with that value.
  - The Javascript associated with catalog.html backs up the live search and filter feature. In general, the strategy is to translate data from the backstage artworks database, passed by app.py and translated by json, into an array in Javascript. We can then make copies of a HTML template and populate them based on that array, and also change the status of these copies based on comparing their elements to user input. The status is then styled in CSS to create a live filtering effect.

## Databases
- There are three databases in the background. An artworks database with an auto-incremented artwork_id field as primary ID, name (of artwork), artist (name), year, text description, and image_path leading to the image in the static folder. A users database with auto-incremented id field as primary ID, username, and hashed password. A reviews database with auto-incremented review_id as primary ID, associated user_id and artwork_id, rating, text comment, and timestamp.
