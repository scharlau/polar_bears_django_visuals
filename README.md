# Visualising Polar Bear Data with Python and Django
This is a demonstrator app focusing on different ways to use python and django to parse data for a web application using polar bear tracking data. 

We're building on the exercise done at https://github.com/scharlau/polar_bears_django which takes some open data on polar bear tracking in Alaska, USA, and puts it into a django based website. You don't need to have done that, but it might explain some context, if you're not sure what different parts do. The main goal of this exercise is to see how we use data from an app to generate charts, and map details.

The goal of 'deliberate practice' is to think about how you'd solve this challenge, and to work at developing code to make this work. There is no single 'correct' version of this code. The purpose of the exercise it become familiar with different ways of making the application work. You should explore how this simple application is done in python with flask and sqlite3 so that you understand how the components work together to show up in the views you see in the browser.

Under 'deliberate practice' we offer up the challenge, then think about options for developing a solution, and code for 12 minutes. After that we pause to discuss how people are approaching the problem, and what they're trying to do. This should be repeated three times and then wrapped up with time for people to express what they found most useful during the session. This should take an hour.

#### Getting Started 

We now want to add some extras so that we can start to visualise the data using some javascript libraries for charting and displaying maps. This will make the data on the pages more interesting.

We'll use https://www.chartjs.org for charts, and https://leafletjs.com for maps. That means there are no licensing issues to worry about in the future.

## Add a Map page for Each Bear

This is based on the tutorial at https://leafletjs.com/examples/quick-start/ All we're doing is making changes for our app. Use the details for pulling the CSS and JS files from unpkg.com to make life easier. You will also need an account at https://www.mapbox.com to use leaflet, and you should fit well within the free tier. We can get map pins from https://www.flaticon.com. 

In order to use any icons on the map (one colour for tagging, another for sightings), we need to add the folder for STATIC_URL in the settings.py file to our app. Add a folder 'static' next to the templates and migrations folders, and then save two icons there. Then we add the {% load static %} declaration at the top of the template file.

As we're only doing this in a basic way, we can do the following on our 'templates/bears/bear_detail.html' page. Add the stylesheet, script and style parts. These add the CSS for leaflet, and our map display, plus the JS for leaflet.

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

We're using the mapbox terrain tiles, as there are no streets. An alternative might be satellite. You'll need to add your own mapbox access token for this to work. For other maps, look at the tiles available from mapbox: https://docs.mapbox.com/api/maps/static-tiles/ and you can also look at the tiles from OpenStreetMap too: https://wiki.openstreetmap.org/wiki/Tiles 

We use the static tag in the iconUrl to convert the path with django to the icon, and separate the icon declaration so that we're not using a blue default one. This way, we could use red ones for each sighting by looping through those lat/long coordinates and creating a marker for each of them.

From here you could show the locations of the sightings on a map using the GPS coordinates. You could also do a chart showing how many sightings there were for each bear by date. You could also do something with the other categories to produce visualisations to suit your needs.

## Adding Charts to Show Trends

We'll add a chart to the main page showing the variations in the bears as a whole using the guide at https://www.chartjs.org/docs/latest/getting-started/ which should show the basic options in practice.

First, we ensure it all works by adding the basic scenario to our page. This will confirm the javascript is loading, and that our chart is displaying in the right location. Open 'templates/bears/bear_list.html' and add this code near the top of the file. This  will put the chart above the listing of the bears. This should be before the loop of bears details.

    <h1>Polar bears Tagged for Tracking</h1>
    <canvas id="myChart"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@2.8.0"></script>
    <script type= 'text/javascript'>
    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45]
        }]
    },

    // Configuration options go here
    options: {}
    });
    </script>
    
You should now reload the page and see a curvy line with a pink shaded area at the top of the page.

Our next step is to swap out the data above with relevant bear data using the attributes that we have. To do that we need to go back to our view and sift through our array of bears so that we can collect some of the values for the attributes by counting them, and collecting them in different variables, which we'll pass back to the template for use in the chart. 

If you look at the models.py file for the bear, then you'll see we have six variables, which we could use for display. Some will be straightforward, such as ear, either left or right, and sex, either male or female. Others, are more complicated such as the pTT_ID label, which is presumably unique for each bear, so there's no point doing that one. Similarly, we assume the lat/longs are also unique, but we could see if they can be grouped into a number locations with appropriate bounds, ie plus/minus a value.

We'll do an easy one to start: how many male/female, and how many left/right ears are tagged. We can do this by looping through each item in our collection, and counting values.

We can put this in the bears/views.py file as our updated bear_list method:

        def bear_list(request):
        bears = Bear.objects.all()
        left_ear = 0
        right_ear= 0
        male = 0
        female = 0

        for bear in bears:
                if bear.sex == 'M':
                        male += 1
                else:
                        female += 1
                if  bear.ear_applied == 'Left':
                        left_ear += 1
                else:
                        right_ear += 1
        
        return render(request, 'bears/bear_list.html', {'bears' : bears, 
        'left_ear': left_ear, 'right_ear': right_ear, 'male': male, 'female': female})

This is all fine, and works for our purposes. We just do if/else statements to drop items into our variables, and then pass them to the template.

In the template we change our javascript for the chart to look like this:

        var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'bar',

        // The data for our dataset
        data: {
        labels: ['Male', 'Female', 'Left Ear', 'Right Ear'],
        datasets: [{
            label: 'Polar Bears',
            order: number
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [{{ male }},{{ female }}, {{ left_ear }}, {{ right_ear }}]
        }]
        },

        // Configuration options go here
        options: { }
        });

We change it to a bar chart, and then give it a new label. We pass the variable into the data array using the familiar syntax. After you reload the page, it looks like there are no male bears. Looking at the list below, you can see that there are a number of male ones. What's going on?

For a clue look at the legend on the y-axis. It goes from 12->18. That's why it looks like there are none. Let's change that. 

Go to the configuration options and add these settings as part of the https://www.chartjs.org/docs/latest/axes/cartesian/linear.html then you'll find the bar chart goes from zero:

        // Configuration options go here
        options: { 
                scales: {
                        yAxes: [{
                                ticks: {
                                        beginAtZero: true
                                        }
                                }]
                        }
                }
        });

Now if you reload the page you'll see all 12 male bears. 

As you can see, it is not too complicated to add either charts, or maps. For charts, you need to do more data manipulation to create the variables that you want, and for most attributes that you might want to manipulate that will be easy: count items to get values and display the results. How, you count things will be the interesting part.

The challenge comes in deciding how complex you want your chart to be. We've used simple options here, but if you look through the examples, then you'll see there are many more options too. Enjoy.

    


