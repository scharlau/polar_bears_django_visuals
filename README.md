# Visualising Polar Bear Data with Python and Django
This is a demonstrator app focusing on different ways to use python and flask to parse data for a web application using polar bear tracking data. 

The goal of 'deliberate practice' is to think about how you'd solve this challenge, and to work at developing code to make this work. There is no single 'correct' version of this code. The purpose of the exercise it become familiar with different ways of making the application work. You should explore how this simple application is done in python with flask and sqlite3 so that you understand how the components work together to show up in the views you see in the browser.

Under 'deliberate practice' we offer up the challenge, then think about options for developing a solution, and code for 12 minutes. After that we pause to discuss how people are approaching the problem, and what they're trying to do. This should be repeated three times and then wrapped up with time for people to express what they found most useful during the session. This should take an hour.

#### Getting Started 
We're building on the exercise done at https://github.com/scharlau/polar_bears_django which takes some open data on polar bear tracking in Alaska, USA, and puts it into a django based website. Go do that if you haven't already.

We now want to add some extras so that we can start to visualise the data using some javascript libraries for charting and displaying maps. This will make the data on the pages more interesting.

We'll use https://www.chartjs.org for charts, and https://leafletjs.com for maps. That means there are no licensing issues to worry about in the future.

## Add a Map page for Each Bear

This is based on the tutorial at https://leafletjs.com/examples/quick-start/ All we're doing is making changes for our app. Use the details for pulling the CSS and JS files from unpkg.com to make life easier. You will also need an account at https://www.mapbox.com to use leaflet, and you should fit well within the free tier. We can get map pins from https://www.flaticon.com. 

In order to use any icons on the map (one colour for tagging, another for sightings), we need to add the folder for STATIC_URL in the settings.py file to our app. Add a folder 'static' next to the templates and migrations folders, and then save two icons there. Then we add the {% load static %} declaration at the top of the template file.

As we're only doing this in a basic way, we can do the following on our 'templates/bear_detail.html' page. Add the stylesheet, script and style parts. These add the CSS for leaflet, and our map display, plus the JS for leaflet.

Open the file and add {% load static %} as the first line in the file. Then add the changes below:

        <head>
        <title>Individual Polar Bear Tracking</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
         integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="crossorigin=""/>
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
        integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="crossorigin=""></script>
        <style>
        #mapid { height: 350px; }
        </style>
        </head>

With this in plsce we can now add the components for the map further down the page. We add this after the details for the bear, and before we list the sightings. We want to show where the bear was tagged. As you can see we're reusing the coordinates for latitude and longitude from above in the javascript.

     {{bear.ear_applied}}	
     </p>
     <div id="mapid"></div>
     <script type = "text/javascript">
     var mymap = L.map('mapid').setView([{{ bear.capture_lat}}, {{bear.capture_long}}], 6 );
     L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.mapbox-terrain-v2',
    accessToken: 'your.mapbox.access.token'
    }).addTo(mymap);
    var taggingIcon = L.icon({ 
    iconUrl: "{% static 'images/placeholder-yellow.png' %} ", 
    iconSize: [35, 35] });
    var marker = L.marker([{{ bear.capture_lat}}, {{bear.capture_long}}], {icon: taggingIcon }).addTo(mymap);
    </script>
     <p>Sightings for this bear via Radio Device</p>

We're using the mapbox terrain tiles, as there are no streets. An alternative might be satellite. You'll need to add your own mapbox access token for this to work.

We use the static tag in the iconUrl to convert the path with django to the icon, and separate the icon declaration so that we're not using a blue default one. This way, we could use red ones for each sighting by looping through those lat/long coordinates and creating a marker for each of them.

From here you could show the locations of the sightings on a map using the GPS coordinates. You could also do a chart showing how many sightings there were for each bear by date. You could also do something with the other categories to produce visualisations to suit your needs.

## Adding Charts to Show Trends

We'll add a chart to the main page showing the variations in the bears as a whole using the guide at https://www.chartjs.org/docs/latest/getting-started/ which should show the basic options in practice.



    


