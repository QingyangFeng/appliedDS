var btn = document.querySelector('.btn');

btn.addEventListener('click', function (event){   
    var username = document.querySelector('#userInput1').value;
    var numberOfTweets = document.querySelector('#userInput2').value;
   
    if (!username) {
      alert('please enter a username');
    } else if (!numberOfTweets) {
      alert('please enter a number of tweets');
    } else { 
    event.preventDefault();
   
    var template = `
        <h2>Twitter Messages</h2>
    
        <div class="row">
            <div class="col-10">
                <img id="img" class='rounded img-fluid' alt="profile picture" height="200" width="200"></img>
            </div>
        </div> 
        <div id='output'></div>

    `; 
    document.getElementById('twitterMessage').innerHTML = template;
    const url = 'http://localhost:5000/streamdata/' + username + '/' 
    + numberOfTweets + '/' + 'json';
    
    getData(url);
    };
});

function getData(url) {
    fetch(url)
    .then(function(response){
        return response.json();
    })
    .then(function(data) {
        
        var info = JSON.parse(data[0]);
        var profilePicURL = info.user.profile_image_url;
        
        getImage(profilePicURL);
        
        var output = `
            <p>Name: ${info.user.name}, Screen name: ${info.user.screen_name}</p>
            <p>Location: ${info.user.location}, Time Zone: ${info.user.time_zone}</p>
        `;
         
        data.forEach(function(message){
            var post = JSON.parse(message)
            output += `
            <div>
                <h3>${post.created_at}</h3>
                <p>${post.text}</p>
                <p>Retweet count: ${post.retweet_count}, Favourite count: ${post.favorite_count}</p>
            </div>
           `; 
        });
        document.getElementById('output').innerHTML = output;
    })
};


// displaying an image
function getImage(url) {
    var request = new Request(url);
    
    fetch(request)
    .then(function(response) {
        return response.arrayBuffer()
    })
    .then(function(buffer) {
        var base64Flag = 'data:image/jpeg;base64,';
        var imageStr = arrayBufferToBase64(buffer);

    document.querySelector('#img').src = base64Flag + imageStr;
  });
};

function arrayBufferToBase64(buffer) {
  var binary = '';
  var bytes = [].slice.call(new Uint8Array(buffer));

  bytes.forEach((b) => binary += String.fromCharCode(b));

  return window.btoa(binary);
};
