export FLASK_APP=server/main.py
while true
do python3 -m flask run
echo
read -p " >> Enter to restart! (Ctrl+C to quit)"
done
