# haiku_bot
A program that generates haikus using the [DataMuse API](http://www.datamuse.com/api/) and Tweets them from [@haiku_b0t](https://twitter.com/haiku_b0t) using the Twitter Developer API. 

### Context
A haiku is a short form of poetry, consisting of 3 lines with a pattern of 5, 7, and 5 syllables per line. For example:

> Twitter haiku bot <br>
> A program of poetry <br>
> Writing sweet nothings

The program chooses a random topic word from a list of english nouns and uses it to seed the DataMuse API calls for each line of the haiku. The API parameters can be used to provide context and get a word that is closely related to the seed word. This is done recursively until the line's syllable count is reached. Once the haiku is generated, it is tweeted using the Twython library to interact with the Twitter API.

The entire process is automated by the twitter_bot.sh bash script, which generates and tweets the haiku, redirects the program output to a log file, and automatically commits and pushes changes to the log file to the GitHub repository. This bash script is ran as a cron job every 6 hours by adding this line to the crontab:

<code>0 */6 * * * bash <file path>/twitter_bot.sh</code>
  
Make sure that permissions are consistent between the local git repository and the crontab. The output from the cron job can also be redirected to a log file for debugging errors if necessary. ssh-agent must also be used when automatically pushing commits, since a password is required for ssh otherwise. This is not ecessary if you are not pushing the commits to a repo; all the commits will still be made and preserved locally.

### Python Libraries
Uses the [Twython Library](https://twython.readthedocs.io/en/latest/index.html) which is a python wrapper for the Twitter Developer API.
Needed in order to Tweet each haiku.


<code>pip install twython</code>

### Config
The Twitter API keys need to be added to the twitter_keys.py file. twitter_keys.py.def is a default example with the correct variable names, just replace the correct values for each API key and remove the last extension.
