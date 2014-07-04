for i in coursera_courses coursera_sessions coursera_universities coursera_instructors coursera_deadlines
do
    mongoexport --host kahana.mongohq.com:10019 -u c3h3 -p c3h3 -d coursera -c $i -o $i.json
done

