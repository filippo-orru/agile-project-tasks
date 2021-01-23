# Agile Manager
Agile Manager is a small web tool that lets you have a broad overview of given tasks and their progress state.

# Deployed Version
http://ffactory.ml/agile-project-tasks/

# Run instructions
 - Install python3 (macos: `brew install python3`)
 - Install nodejs
 - Install requirements: `python -m pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt`
 - Install node modules: `npm ci`
 - Install sqlite3 if not pre-installed (eg. from https://www.sqlite.org/download.html)
 - Install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html
 - if linux/macos:
   - `chmod a+x start.sh`
   - start the server with `./start.sh`
   - To reload: kill the script with control+c and press enter
   - To kill: press ctrl+c twice

 - else if windows:
   - start with `.\start.bat`
   - To reload: kill the script with control+c and restart it
   
# Dev instructions
 - To constantly auto-generate .css out of .scss files every time you apply a change, run watcher.bat (Windows), or watcher.sh (Mac and Linux).
 - To manually compile scss, run `npm run css`
 
# Used libraries
 - Bootstrap 4 ([documentation](https://getbootstrap.com/docs/4.5/getting-started/introduction/))
 - Bootstrap Validator ([documentation](http://1000hz.github.io/bootstrap-validator/?underwear=on)) to use, implement validator.js in html
 
# Developers
 - Amann Anna-Caterina
 - Buraczewska Diana
 - Mühlbacher Jan
 - Orru Filippo
 - Toporsch Sebastian
 - Weigl Tobias
