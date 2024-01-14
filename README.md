Video demo:
https://youtu.be/mNV1xfbV0Sw

My project is a web application that allows users to browse, search, and view a database of artworks, and allows users to review artworks with a five-star rating system and a comment section.

Whereas access to the landing page, the catalog page, and the registration page do not require login credentials, all other functions of the app requires login credentials.

The application is run on flask. If accessing from the Visual Studio Code / GitHub environment that we’ve been using throughout the semester, one can run the application by going into the directory and typing flask run.

Upon entry, the user will be directed to the “landing” page. The user will see two options: “Catalog”, and “Feeling Lucky”.

If one clicks on “Catalog”, one will be directed to the /catalog page showing a list of artworks in alphabetical order, just below a search area. If one starts typing in the box below the prompt “Looking for something?”, the small thumbnails at the top of the page will be filtered in accordance to live input. At this point, if one clicks on any hyperlink for individual artwork pages, one will be redirected to the Login page.
Similarly, if one clicks on “Feeling Lucky” on the landing page, one will also be redirected to the Login page.

For a first-time visitor, at this point, the user should probably click on “Register” on the top right corner. The registration form should be self-explanatory. Once the user hits the register button,  provided that the username is accepted, and passwords match, one will be automatically logged in and redirected to the landing page.

Now, having logged in, the user can access a desired artwork page by clicking on a hyperlink on the catalog page, or, the user can click on “Feeling Lucky” on the landing page or the navigation bar to access an artwork at random.

Once on the artwork page, the user can see a description, a current average of all star ratings from all users,  and comments from other users if any. The user can then click on the stars and type into the comment box, and submit a review. If either of these is empty, the submission will not be successful. Once submitted, the page will refresh and display the new review to the user. Now the submit button is disabled and the delete button is enabled. The user can click on delete to delete the review, and the page will refresh.

The user can click on “My Collection” in the navigation bar to view a log of all of the user’s past reviews.

Finally,  the user can click on “Change Password”. The password change page should be self explanatory.

Have fun and thanks for visiting!
