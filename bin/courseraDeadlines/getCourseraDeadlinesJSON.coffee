

args = require('system').args

# console.log args

sessionId = args[2]
resFileDir = args[3]
resFilePath = resFileDir + sessionId

console.log "sessionId = " + sessionId
console.log "resFileDir = " + resFileDir
console.log "resFilePath = " + resFilePath

# sessionId = "datasci-002"
# resFileDir = "/home/c3h3/c3h3works/NodeProjects/try_ical/courseraDeadlinesJson/"
# resFilePath = resFileDir + sessionId

courseraDeadlineURL = "https://class.coursera.org/" + sessionId + "/api/course/calendar"

console.log "courseraDeadlineURL = " + courseraDeadlineURL


req = require "request"
fs = require 'fs'
ical = require "ical"

res = req courseraDeadlineURL, (err,res,body) -> 
	cal = ical.parseICS body
	calJson = JSON.stringify cal
	fs.writeFile resFilePath, calJson, (err) ->
		if err
			throw err
		else
			console.log 'It\'s saved!' 







