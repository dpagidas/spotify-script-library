# spotify-script-library
Spotify script is a python script that stores the user track history also counts the amount of times user heard it and finally makes a playlist with most played tracks after a specific time set by the user.

## Deployment

### Requirements

* Upgrade spotipy lib `pip install git+https://github.com/plamere/spotipy.git --upgrade`.
* Run `pip install -r requirements.txt` to install dependencies.

### How To Use This

1. Navigate over to https://developer.spotify.com/dashboard/login, and sign up for an Spotify developer account.
2. Register a new Spotify application click Edit Settings and make your Redirect URI `http://localhost:8888/callback`.
3. Fill in the relevant information in Environment Variables or straight to the code and add your `USERNAME` , `CLIENT_ID` , `CLIENT_SECRET`. To get your username you can follow this link for further instructions https://community.spotify.com/t5/Accounts/how-do-i-find-my-spotify-user-id/td-p/665532. Client id and Client secret you can get it from Spotify developer account.
4. On main() function set the time you want to stop the script and create the playlist.
4. Run `python spot.py` or push play button on PyCharm.


### Development
If you want to work on this application we’d love your pull requests and tickets on GitHub!

1.If you open up a ticket, please make sure it describes the problem or feature request fully.
2.If you send us a pull request, make sure you add a test for what you added, and make sure the full test suite runs with `make test`.

