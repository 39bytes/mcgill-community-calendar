## Inspiration

We wanted to create a centralized event calendar to make it easier for McGill students to know about everything happening soon on campus. The current problem is that students have to follow dozens of accounts on social media to be in the loop, but this clutters their feeds. With a single app that allows anyone to see everything happening soon at McGill, students can more easily get involved in the community, and school organizations or clubs can have greater reach.

## What it does

Clubs/organizations can register and login to create events that will appear on the main calendar page. These events can be anything, from open club meetings to fundraisers to workshops. Users can specify the name of their event, the location, the start date, and attach an image. They can also select from a list of tags to make it clear what type of event they're running. Students looking at the main calendar can then filter by tag to find events that interest them. If a student is interested by a specific organization, they can go to that organization's user page to find out about all of the future events they will be running.

## How we built it

- Created a full stack app in Python with Flask.
- Used TailwindCSS to style the website with some components from the Flowbite component library.
- User and event data is stored in an SQLite database using SQLAlchemy for the ORM.
- Image data is stored in an uploads folder on the server.

### Challenges we ran into

The main technical challenge was working with dates and times. It took a lot of bug fixing before finally getting it right. Processing image data was also challenging, Designing the main calendar was also a big challenge, but we are happy with the final result.

### Accomplishments that we're proud of

We're proud of the overall design of the website, as well as the UX of the app.
From a technical standpoint, our most proud features are the tag system for filtering, as well as pagination on the main calendar.

## What we learned

We learned a lot about the general process of developing a full stack app. In particular, we learned so much about CSS and UI design. We also learned how to build a project as a team using Git to collaborate with each other.

## What's next for McGill Community Calendar

- Integrating McGill's authentication system into the app to restrict login to registered McGill student associations.
- Add more tags to cover the range of different event types
- Further improving the UX of the website

## Credits

Arrow icon: [source](https://uxwing.com/back-arrow-icon/)
Pencil icon: [source](https://icon-icons.com/icon/edit-pencil/120034)
McGill bird logo: @mcgillu on Twitter
