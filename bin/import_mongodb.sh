for i in coursera_courses coursera_sessions coursera_universities coursera_instructors coursera_deadlines
do
    mongoimport -d coursera -c $i --file $i.json
done

