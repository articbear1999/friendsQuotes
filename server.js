const sqlite3 = require('sqlite3').verbose();
const port = 3000
const dbPath = 'C:/Users/Artic/PycharmProjects/friends/pythonsqlite.db'

var express = require("express");
var bodyParser = require("body-parser");
var app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.set('view engine', 'handlebars');
app.engine('html', require('hbs').__express);

twentyFiveList = ["3"]
twentyFourList = ["1","2","3","6","7"]
twentyThreeList = ["1","2","3","4","5","6","7","8","9"]
notInSTen = ["25","24","23","22","21","20","19","18"]

let db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY, (err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Connected to the sqlite3 database.');
  });

  // db.serialize(() => {
  //   db.each(`SELECT DISTINCT character
  //            FROM quotes WHERE character LIKE '%Joey%'`, (err, row) => {
  //     if (err) {
  //       console.error(err.message);
  //     }
  //     console.log(row);
  //   });
  // })
  

  var server = app.listen(port, function () { // create a server
    console.log("app running on port.", server.address().port);
});

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

//let query = `SELECT DISTINCT character FROM quotes WHERE character LIKE '%Joey%'`
let query = `SELECT * FROM quotes WHERE character LIKE '%Joey%' and season = 10 and episode = '01'`
app.post('/insert', function(req, res)
{
  character = req.body.characters
  season = req.body.seasons
  episode = req.body.episodes
  lines = req.body.lines
  character = (character !="Any") ? character = "character LIKE '%" + character + "%' " : character = ""
  // If the seasons don't have the episode entered
  if (!twentyFiveList.includes(season) && episode == "25")
  {
    res.send("Season : " + season + " does not have episode " + episode)
    return
  }
  if (!twentyFourList.includes(season) && episode == "24")
  {
    res.send("Season : " + season + " does not have episode " + episode)
    console.log(!twentyFourList.includes(season) + typeof(season))
    return
  }
  if (!twentyThreeList.includes(season) && episode == "23")
  {
    res.send("Season : " + season + " does not have episode " + episode)
    return
  }
  if(season == 10 && notInSTen.includes(episode))
  {
    res.send("Season : " + season + " does not have episode " + episode)
    return
  }
  if (season != "Any") //if season is selected
  {
    if(character != "") //if there is also a character selection
      season = "and season = " + season + " "
    else
      season = "season = " + season + " "
  }
  else //if you can select any season
    season = ""
  if (episode != "Any") //if season is selected
    {
      if(character != "" || season != "") //if there is any previous selection
        episode = "and episode = " + "'" + episode + "' "
      else
        episode = "episode = " + "'" + episode + "' "
    }
  else //if you can select any episode
    episode = ""
  query = (character == "" && season == "" && episode == "") ? query = "SELECT * FROM quotes " : query = "SELECT * FROM quotes WHERE "
  orderBy = " ORDER BY season, episode"
  //limit = " LIMIT " + lines
  if(parseInt(lines) < 1)
  {
      res.send("Error: Invalid amount of lines. Lines is smaller than 1")
      return
  }
  query = query + character + season + episode + orderBy
  console.log(query)
  db.all(query, [], (err, rows) => {
    if (err) {
      throw err;
    }
    rows.forEach((row) => {
    res.write('season:' + row.season + ' episode:' + row.episode + ' ' + row.character + ':' + row.quote + '\n')
    })
  })
})

app.get("/get-data", function(req, res) { // listens for requests to localhost
  charList = []
  db.all(query, [], (err, rows) => {
    if (err) {
      throw err;
    }
    rows.forEach((row) => {
      res.write(row.character + '\n')
      //console.log(row.character)
    })
  })
  console.log(season + character)
})

// db.close((err) => {
//   if (err) {
//     console.error(err.message);
//   }
//   console.log('Close the database connection.')};