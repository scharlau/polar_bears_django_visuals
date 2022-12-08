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

## Deploying to PythonAnywhere 
I also deployed this to https://scharlau.pythonanywhere.com as an experiment. I found various issues moving it to MySQL, which made it take longer than expected. 
ONE: Issues with deploying the django app were easy enough. Adding libraries to the requirements.txt file and ensuring they were in the correct format for the file was trial and error: 
* refresh the deployment on pythonanywhere, 
* check the web page, and then
* check the error log
* make changes to requirements.txt file and run pip install ... on pythonanywhere and then repeat

TWO: Issues with migrations on pythonanywhere using mysql. This should've been easy too: add dj_database_url library, and then point to relevant database on the mysql server in a .env file with suitable username and password, and then run the migrations. However, the migrations wouldn't run, so I needed to run the 'create table' command myself on the server. Then the parse_csv script would run and run and run, but not save any data into the database tables.

I used sqlmigrate command to generate sql for creating tables, but this was for sqlite instead of mysql. I rewrote them as mysql commands, and ran them on the server. This gave me the tables. 

                CREATE TABLE bears_bear (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, bearID INT NOT NULL, pTT_ID INT NOT NULL, capture_lat DECIMAL NOT NULL, capture_long DECIMAL NOT NULL, sex VARCHAR(2) NOT NULL, age_class VARCHAR(2) NOT NULL, ear_applied VARCHAR(2) NOT NULL, created_date DATETIME NOT NULL);

                CREATE TABLE bears_sighting (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, deploy_id INT NOT NULL, recieved VARCHAR(10) NOT NULL, latitude DECIMAL NOT NULL, longitude DECIMAL NOT NULL, temperature INTEGER NOT NULL, created_date DATETIME NOT NULL, bear_id_id INT NOT NULL, FOREIGN KEY (bear_id_id) REFERENCES bears_bear (id));

However, when using manage.py dumpdata to generate json of data to use with manage.py loaddata command, that says it worked, but did not put the data of 6344 objects into the tables either.

SUCCESS! I did the following:
a) remove the sqlite database - or rename the file so that django doesn't see it.
b) add the remote database details to the settings.py file
c) run manage.py migrate again, and then load the db.json file

I guess the sqlite db info was confusing things. 

## Setting up Continuous Deployment on PythonAnywhere
On PythonAnywhere the free account doesn't let you deploy you code with a 'git push ...' command. That requires the paid account. Using the free account you can set up GitHub to trigger a deploy to PythonAnywhere by adding a webhook to your application. After you do this, your application will pull the last commit from GitHub after it recieves a notification sent from GitHub. We can then also use the PythonAnywhere API to reload our application too. What follows is based on the notes found at
1. https://dev.to/soumyaranjannaik/automatically-deploying-django-app-to-pythonanywhere-through-github-282j for the webhook details, and
2. https://github.com/marketplace/actions/reload-pythonanywhere-webapp for the reload details. This didn't work for me as you'll see below. Nor did a similar exercise in trying to create my own action to reload the app using the PythonAnywhere API via a GitHub Action.

#### You need to be working in the virtualenv on PythonAnywhere
Before you go any further look at your dashboard and confirm the name of the virtualenv that you have for your webapp. Now open a console and run this command to ensure that you are using that virual environment:

                workon polar-bear-visual-virtualenv

You should now see a something like (polar-bear-visual-virtualenv) <timestamp> ~$ to show that you're now in the virtual environment. If you forget to ensure you're working in the virtualenv, then you'll run around in circles trying to get things working, but they won't

First, follow the first three steps at number 1 above, and also remember to update your requiremnts.txt file with the addition of GitPython. In the 'third' step there this is the bears/urls.py file as we've added a new method to the views.py file, so we need to list it here.

Second, do step 4. Yes, you do need a new key to use as a 'deploy key' with GitHub you can't reuse one that you've already registered there for something else. If you've already created an ssh key to use with GitHub, then you need to give this key a new name such as id_deploy_rsa.  After you register it at GitHub in step 5, it should trigger an email saying that a new key has been added.

Third, when you're working through step 7 for the 'webhook' and setting it up on GitHub you might need to cycle through things to get the code working correctly. I found that I had issues getting GitPython to be included - I forgot to ensure that I was in the virtualenv on PythonAnywhere. I was in '.venv', but that wasn't the same. After that was sorted it was down to fixing the path needed for the git.repo(...) method. I did the following:
1. set line in views.py on local machine
2. make local commit to git repo and push to remote
3. pull remote to pythonanywhere
4. refresh web app in 'web' part of the dashboard
5. try to set webhook in GitHub
6. check 'recent deliveries' and then the most recent one, and check the 'response' tab to see the error message - usually 'NoSuchPathError' and then it would show the attempted path, which I could then try to fix
7. Repeat from step 1
8. eventually I got 'response 200' and then could see the green tick next to the webhook to show it was in place, and working.

## Setting up the Reload of the application on PythonAnywhere 
First, go to your PythonAnywhere 'Account' page and click on the tab for 'API Token' and create a new token.
Second, we want to use the details found at https://www.pythonanywhere.com/forums/topic/27634/ to create a python script to run that will reload our web application. Create a file in the root of your application that sits next to manage.py called 'reload.py'. Then put this code into the file:

        import requests
        import os

        # add each of the variables to your environment as follows without the < > marks
        # on linux/macOS as below, on windows go here: https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/
        # export PA_USERNAME=<username on pythonanywhere>

        # use this if running from GitHub Action
        pa_username = os.environ["PA_USERNAME"]
        api_token = os.environ["API_TOKEN"]
        domain_name = os.environ["DOMAIN_NAME"]

        response = requests.post(
        'https://www.pythonanywhere.com/api/v0/user/{pa_username}/webapps/{domain_name}/reload/'.format(
                pa_username=pa_username, domain_name=domain_name
        ),
        headers={'Authorization': 'Token {token}'.format(token=api_token)}
        )
        if response.status_code == 200:
        print('reloaded OK')
        else:
        print('Got unexpected status code on reload attempt {}: {!r}'.format(response.status_code, response.content))

Second, add the environment variables as noted above for the pa_username, api_token, and domain_name to your system. Yes, you could just write them here, that would work too if you don't intend to push this file to GitHub, but keep it out of your repository.
Third, you should be able to run the file and have it successfully reload your application. 

With this in place you can now edit the application, make a local commit, and then push to GitHub where the webhook will trigger a pull from GitHub to PythonAnywhere. Then you can run the reload script. All fine and good.

### Adding reload.py to a GitHub Action
Ideally, when the webhook was called it would trigger a GitHub Action to run the reload script. If you look in the workflow folder, you'll find an action, which does this. However, it always encouters a reponse 500, server error. You'll also find a 'main.yml' file, which does something similar via JS, but that doesn't work either. If you want to pursue this yourself, then you need to do the following:

First, go to 'Secrets' in the GitHub settings page for the app, and then go to 'Actions' and create three new ones, which you'll need for the action script that you'll create in a minute.
        A) API_Token - add the value of the token you created in the step above.
        B) PA_USERNAME - add the value of your username on PythonAnywhere
        C) DOMAIN_NAME - this is the URL of your application which is normally <username>.pythonanywhere.com 
Third, add a copy of the reload.yml file as a new 'action'. Go to 'Actions'->'New Workflow'->'set up a workflow yourself' and then add the content there and make a commit.
Fourth, you should now be able to run this workflow and check any errors and see if they can be fixed, or at least determine why it fails. 









