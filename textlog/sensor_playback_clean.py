#!/usr/local/bin/python3
# import matplotlib
# import matplotlib.pyplot as plt
import numpy as np
import datetime
import glob, os
import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import seaborn as sns
import sys
from time import mktime
import time
import random
from time import sleep

# from datetime import datetime

ignorelist = [ "/192.168.1.12", "/ranger2", "/piezo", "/photon3", "/stove", "/shower", "/photon"] #, "/microwave"]

#Create a new function:
def num_missing(x):
  return sum(x.isnull())


def print_sensors(days, hours, activations, figpath="/Users/rtwomey/housemachine/data/time/"):
	# print x, y, sensors

	# plt.plot(x, y)
	# plt.gcf().autofmt_xdate()
	# plt.show()

	zippeddata = zip(days, hours, activations)

	filtereddata = [ sample for sample in zippeddata if sample[2] not in ignorelist]

	# print(set(data['sensors']))
	sensornames = set([ item[2] for item in filtereddata])
	print(sensornames)
	exit()


	# Strip Plot
	data = pd.DataFrame()
	data['days']= [datetime.datetime.strftime(sample[0], "%m.%d") for sample in filtereddata]
	# data['start_time']=[matplotlib.dates.datestr2num(sample[1].strftime("%H:%M:%S")) for sample in filtereddata]
	data['sensors'] = [sample[2] for sample in filtereddata]
	data['hours'] = [r[1].hour for r in filtereddata]

	# count frequency by DataFrame column
	# https://stackoverflow.com/questions/36004976/count-frequency-of-values-in-pandas-dataframe-column
	# print data['sensors'].value_counts()

	# count frequency across rows by hours
	# http://hamelg.blogspot.com/2015/11/python-for-data-analysis-part-19_17.html
	# ctdata = pd.crosstab(index=data["hours"], columns=data["sensors"], margins=True)
	ctdata = pd.crosstab(index=data["sensors"], columns=data["hours"], margins=True)
	
	# manually clean up data
	ctdata.to_csv("sensor_frequencies.csv", sep=',')
	# exit()

	# normalize across rows
	# normdata = ctdata.div(ctdata.sum(axis=1), axis=0)
	
	# normalize down columns
	normdata = ctdata.div(ctdata.sum(axis=0), axis=1)
	
	# print normalized sensor values
	print(normdata.to_string(float_format=lambda x: '%.5f' % x))
	
	print(ctdata.to_string())

	
	maxActivations = 1000
	activations = ctdata.loc["All",:]
	activations = activations.div(activations.sum()).multiply(maxActivations*2)[:-1]
	print(activations.to_string())

	# exit()

	timemultiplier=0.5
	activationmultiplier=8

	random.seed(1.0)
	sys.stdout.write("\033c")
	sys.stdout.flush()
	sleep(3.0)
	count = 0

	duration = int(30.0 * timemultiplier)

	# print sensors by hours
	for i in range(0,24):
		
		hourprobs = normdata.loc[:,i][:-1]
		hourprobs = hourprobs.div(hourprobs.sum())

		numactivations = int(activations.iloc[i]) * activationmultiplier
		numactivations = min(400, numactivations)
		# print "\n=== %04d (%d) ===\n" % (i, numactivations)
		
		
		
		# print numactivations
		# print hourprobs.sort_values(i)
		
		timeout_start = time.time()

		# sys.stdout.write("%02d00 %d " % (i, numactivations))
		sys.stdout.write("%02d00 " % i)
		sys.stdout.flush()
		sleep(1.0)
		
		if numactivations > 0:
			timeunit = float(duration) / numactivations
		else: 
			timeunit = duration

		# print timeunit, duration
		# exit()

		while time.time() < timeout_start+duration:
		# for j in range():
			sensor = np.random.choice(normdata.loc[:,0].keys()[:-1], p=hourprobs)
			sys.stdout.write(sensor[1:]+" ")
			sys.stdout.flush()
			# sleep(random.uniform(0.3, 2.2) * timemultiplier)
			sleep(random.uniform(0.3*timeunit, 2.2*timeunit))
			if random.randrange(5) < 1:
				sys.stdout.write("\n")
			count = count + 1

		print()

		sys.stdout.write("\033c")
		sys.stdout.flush()
		count = 0
				# print sensor.lstrip("/"),

	

def plot_sensors(days, hours, activations, figpath="/Users/rtwomey/housemachine/data/time/"):
	# print x, y, sensors

	# plt.plot(x, y)
	# plt.gcf().autofmt_xdate()
	# plt.show()

	# print set(sensors)
	# exit()

	zippeddata = zip(days, hours, activations)

	filtereddata = [ sample for sample in zippeddata if sample[2] not in ignorelist]

	# Strip Plot
	data = pd.DataFrame()
	data['days']= [datetime.datetime.strftime(sample[0], "%m.%d") for sample in filtereddata]
	data['start_time']=[matplotlib.dates.datestr2num(sample[1].strftime("%H:%M:%S")) for sample in filtereddata]
	data['sensors'] = [sample[2] for sample in filtereddata]
	data['hours'] = [r[1].hour for r in filtereddata]

	# count frequency by DataFrame column
	# https://stackoverflow.com/questions/36004976/count-frequency-of-values-in-pandas-dataframe-column
	# print data['sensors'].value_counts()

	# count frequency across rows by hours
	# http://hamelg.blogspot.com/2015/11/python-for-data-analysis-part-19_17.html
	# ctdata = pd.crosstab(index=data["hours"], columns=data["sensors"], margins=True)
	ctdata = pd.crosstab(index=data["sensors"], columns=data["hours"], margins=True)
	
	# manually clean up data
	ctdata.to_csv("data/sensor_frequencies.csv", sep=',')
	# exit()

	# normalize across rows
	# normdata = ctdata.div(ctdata.sum(axis=1), axis=0)
	
	# normalize down columns
	normdata = ctdata.div(ctdata.sum(axis=0), axis=1)
	
	# print normalized sensor values
	print(normdata.to_string(float_format=lambda x: '%.5f' % x))
	
	print(ctdata.to_string())

	
	maxActivations = 1000
	activations = ctdata.loc["All",:]
	activations = activations.div(activations.sum()).multiply(maxActivations*2)[:-1]
	print(activations.to_string())

	# exit()

	# print sensors by hours
	for i in range(0,24):
		
		hourprobs = normdata.loc[:,i][:-1]
		hourprobs = hourprobs.div(hourprobs.sum())
		numactivations = int(activations.iloc[i])
		
		print("\n=== %04d (%d) ===\n" % (i, numactivations))
		
		# print numactivations
		# print hourprobs.sort_values(i)
		
		for j in range(numactivations):
			sensor = np.random.choice(normdata.loc[:,0].keys()[:-1], p=hourprobs)
			print(sensor[1:], end=",")
		print()

	# plotting
	sns.set(style="whitegrid", color_codes=True)
	# # sns.swarmplot(x="day", y="start_time", data=data, ax=ax)
	# ax = sns.stripplot(x="day", y="start_time", hue="locations", data=data, jitter=True, size=data['duration'])
	# ax = sns.stripplot(x="day", y="start_time", hue="sensors", data=data)
	ax = sns.stripplot(x="days", y="start_time", hue="sensors", size=16, alpha=.2, jitter=True, data=data)
	# ax = sns.stripplot(x="sensors", y="start_time", hue="sensors", size=16, alpha=.2, jitter=True, data=data)
	# sns.despine()

	fig = plt.gcf()

	ax.yaxis_date()
	ax.set(ylim=(min(data['start_time']), max(data['start_time'])))

	# Put a legend to the right of the current axis
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

	fig.autofmt_xdate()
	fig.canvas.set_window_title('Sensor Times')
	
	# save figure to disk
	# plt.figure(figsize = (16,10))
	# figpath = os.path.join(figpath, "sensor_times_cumulative.png")
	# plt.savefig(figpath, bbox_inches='tight')
	# print "saved figure to disk:\n", figpath


	# show figure
	plt.show()

	# figpath = os.path.join("/Users/rtwomey/housemachine/time/", "sensors.png")
	# figpath = "/Users/rtwomey/housemachine/data/time/sensors.png"
	# plt.savefig(figpath)#, bbox_inches='tight')
	# print "saved figure to disk:\n", figpath


def plot_sensors2(days, hours, activations, figpath="/Users/rtwomey/housemachine/data/time/"):
	# print x, y, sensors

	# plt.plot(x, y)
	# plt.gcf().autofmt_xdate()
	# plt.show()

	# print set(sensors)
	# exit()

	# Strip Plot
	data = pd.DataFrame()
	data['day']= [datetime.datetime.strftime(day, "%m.%d") for day in days]
	
	# PROBLEMS
	# data['start_time']=[mdates.date2num(datetime.datetime.combine(hour.time())) for hour in hours]
	data['start_time']=[matplotlib.dates.datestr2num(hour.strftime("%H:%M:%S")) for hour in hours]
	data['sensors'] = [activation for activation in activations]

	# print sensors
	# print data['locations']

	sns.set(style="whitegrid", color_codes=True)
	# # sns.swarmplot(x="day", y="start_time", data=data, ax=ax)
	# ax = sns.stripplot(x="day", y="start_time", hue="locations", data=data, jitter=True, size=data['duration'])
	# ax = sns.stripplot(x="day", y="start_time", hue="sensors", data=data)
	ax = sns.stripplot(x="day", y="start_time", hue="sensors", jitter=True, data=data)
	fig = plt.gcf()

	ax.yaxis_date()
	ax.set(ylim=(min(data['start_time']), max(data['start_time'])))

	# Put a legend to the right of the current axis
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

	fig.autofmt_xdate()
	fig.canvas.set_window_title('Sensor Times')
	
	# save figure to disk
	# plt.figure(figsize = (16,10))
	# figpath = os.path.join(figpath, "sensor_times_cumulative.png")
	# plt.savefig(figpath, bbox_inches='tight')
	# print "saved figure to disk:\n", figpath

	# show figure
	plt.show()

	# figpath = os.path.join("/Users/rtwomey/housemachine/time/", "sensors.png")
	# figpath = "/Users/rtwomey/housemachine/data/time/sensors.png"
	# plt.savefig(figpath)#, bbox_inches='tight')
	# print "saved figure to disk:\n", figpath

def get_sensor(days, hours, activations, logs, searchterm):

	sensorlist = set(activations)
	# sensors = []
	# offsets = []

	# leftspace = 0
	# i=0

	# sensorlist = [ "chair", "table", "lamp", "desklamp", "couch", "fridge", "microwave",  "stove", "garbage", "toilet", "shower", "bed", "washingmachine", "print", 
	# 	"frontdoor", 
	# 	# "backdoor", "kitchendoor", "bedroomdoor", 
	# 	# "bathroomdoor", 
	# 	"basementdoor",
	# 	"kitchen", "diningroom", "basement", "livingroom", "studio",
	# 	# "occupancy", "temperature", "humidity" 
	# 	]                     

	# for sensor in sensorlist:
	# 	# sensors.append(sensor[1:])
	# 	sensors.append(sensor)
	# 	offsets.append(leftspace)
	# 	leftspace = leftspace + len(sensor) + len("  ")
	# 	i = i + 1

	# data = zip(hours, activations)

	# data = zip(hours, activations, logs)

	rhours = []
	rdays = []
	rsensors = []

	for index, sensor in enumerate(activations):
		if sensor == searchterm:
			# print hours[index], logs[index]
			rhours.append(hours[index])
			rdays.append(days[index])
			rsensors.append(sensor)
			#datetime.time.strftime("%H.%M.%S", hours[index])

	plot_sensors2(rdays, rhours, rsensors)


def printWithOffset(word, offset, output = sys.stdout):
	output.write(" "*offset + word+"\r")
	output.flush()
	

def collapse_days(days, hours, sensordata):

	print("Collapsing day by hour...", end="")
	sensorlist = set(sensordata)
	sensors = []
	offsets = []

	leftspace = 0
	i=0

	sensorlist = [ "chair", "table", "lamp", "desklamp", "couch", "fridge", "microwave",  "stove", "garbage", "toilet", "shower", "bed", "washingmachine", "print", 
		"frontdoor", 
		# "backdoor", "kitchendoor", "bedroomdoor", 
		# "bathroomdoor", 
		"basementdoor",
		"kitchen", "diningroom", "basement", "livingroom", "studio",
		# "occupancy", "temperature", "humidity" 
		]                     

	for sensor in sensorlist:
		# sensors.append(sensor[1:])
		sensors.append(sensor)
		offsets.append(leftspace)
		leftspace = leftspace + len(sensor) + len("  ")
		i = i + 1

	one_full_day = []

	for i in range(24):
		start = "%02d.00.00" % i
		finish = "%02d.59.59" % i

		print("%02d00" % i, end="")
		sys.stdout.flush()
		# print ""
		# print ""
		# print "=== %s - %s ===" % (start, finish)
		# print ""

		# print start,

		results = []

		for index, hour in enumerate(hours):
			if datetime.datetime.strptime(start, "%H.%M.%S").time() < hour < datetime.datetime.strptime(finish, "%H.%M.%S").time():
				# print "%s-%s (%0.2f)\t%s" % (datetime.datetime.strftime(hours[fname], "%H:%M:%S"), 
				# 	datetime.datetime.strftime((hours[fname]+datetime.timedelta(seconds=durations[fname])), "%H:%M:%S"),
				# 	durations[fname], 
				# 	fname.split(root)[1])

				results.append([sensordata[index][1:], hour])
				# results.append(sensordata[index][1:])

				# totalhourduration = totalhourduration + durations[fname]
				# durationsbyroom[locations[fname]] = durationsbyroom[locations[fname]] + durations[fname]
				# print asrlines[fname]
				# for line in asrlines[fname].lstrip("\n").split("\n"):
				# 	print line, "\n\t\t\t\t" ,

		one_full_day.append(results)
		# print results

		# for result in set(results):
		# 	# print "%s_%s_%s.txt" % (room, start, finish)
		# 	# outf = open("data/sensors_%02d00_hour.txt" % i, "w")
		# 	# print result[0]+"\t"+result[1]
		# 	print result,
		# 	# outf.write(result+",")
		# print ""
		# 	# outf.close()

		# for idx, sensor in enumerate(sensors):
		# 	if sensor in results:
		# 		print sensor,
		# 	else:
		# 		print " "*len(sensor),

		# print ""

			
	print()

	for hour, results in enumerate(one_full_day):
		# print "%02d:00:00 %d\t" % (hour, len(results)),
		print("%02d:00:00  " % hour, end="")
		# print results
		# exit()

		# print set of active sensors by hour
		activesensors = set([item[0] for item in results])
		# print set(activesensors)

		for idx, sensor in enumerate(sensors):
			if sensor in activesensors:
				print(sensor, end="")
			else:
				print(" "*len(sensor), end="")

		print()

		# print all sensors by event
		# for thissensor, time in sorted(results, key = lambda x: x[1]):
		# 	print datetime.datetime.strftime(time, "%H:%M:%S"),
		# 	for sensor in sensors:
		# 		if sensor == thissensor:
		# 			print sensor, 
		# 		else:
		# 			print " "*len(sensor),
		# 	print ""

		# sensornamesthishour = [item[0] for item in results]

		# for sensor in sensors:
		# 	if sensornamesthishour.count(sensor) > 5:
		# 		print sensor,
		# 	else:
		# 		print " "*len(sensor),

		# print ""



def sensorSubstitutions(sensorname):

	if sensorname.startswith("/occupancy"):
		return sensorname[:10]

	# if sensorname.endswith("occupancy"):
	# 	return sensorname[:-len("occupancy")]

	if sensorname.startswith("/kitchendoor"):
		return "/kitchendoor"

	if sensorname.startswith("/hotplate"):
		return "/stove"

	if sensorname == "/photon":
		return sensorname

	if sensorname.startswith("/microwave"):
		return "/bed"

	if sensorname.startswith("/studiooccupancy"):
		return "/studio"

	return sensorname



days = []
hours = []
activations = []
logs = []

count = 0
root = "/Users/rtwomey/housemachine/data/sensors/logs"
ignoreaddresses = ["/particleip", "/log" ] #, "/temperature" ]
# "/humidity"
# "/digitalpin", 
print("Reading sensor logs:", end="")

for path, subdirs, files in os.walk(root):
	for file in files:
		count = count + 1
		if count % 10 == 0:
			sys.stdout.write(". ")
			sys.stdout.flush()

		name, extension = os.path.splitext(file)
		if extension == ".csv":
			# print os.path.join(path, name)
			try:

				date, trashtime = name.split("_")
				thisdate = datetime.datetime.strptime(date, "%Y%m%d")
				# thishour = datetime.time.strptime(time, "%H%M%S")
				# print date, time
				# x.append(thisdate)
				# y.append(thishour)
			except:
				# print e
				# print "ignoring", name
				continue
			
			f = open(os.path.join(path, file),'r')
			for line in f.readlines():
				# print line
				line = line.rstrip(";\n")
				vals = line.split(';')
				# print vals
				try:				
					thistime = datetime.datetime.strptime(vals[-1], "%H:%M:%S.%f").time()
				except:
					# print e
					# print "ignoring", line
					continue

				lastsensor = None
				lasttime = None

				if vals is not None:
					oscmsg = vals[0]

					# for val in vals:
					# 	if val.startswith("/"):
					# 		lastOSCAddress = val

					# pick appropriate name for sensor
					if oscmsg not in ignoreaddresses:
						if oscmsg == "/analogpin":
							sensorname = vals[3]
						elif oscmsg == "/digitalpin":
							sensorname = vals[3]
						elif oscmsg == "/dht11":
							if float(vals[1]) > 80.0:
								sensorname = vals[4]
							else:
								continue
						elif oscmsg == "/motion":
							sensorname = vals[2]
						elif oscmsg == "/nodeid":
							sensorname = vals[1]
						elif oscmsg == "/temperature":
							# sensorname = vals[2]
							if float(vals[1]) > 81.0 and vals[2] == "shower":
								sensorname = vals[2]
							else:
								continue
						elif oscmsg == "/humidity":
							sensorname = vals[2]
						else:
							sensorname = oscmsg
							# continue

						# add slash if necessary
						if not sensorname.startswith("/"):
							sensorname = "/"+sensorname

						# # screen for state change or elapsed time
						if lastsensor != sensorname:
							lastsensor = sensorname
							lasttime = thistime
						else:
							# if thistime - lasttime > datetime.datetime.senconds
							# ignore repeats
							# print file,lastsensor,lasttime
							continue


						# if lastOSCAddress is not None:
						# 	if lastOSCAddress in ignoreaddresses:
						# 		print file,line
						# 	else:
						# 		x.append(thisdate)
						# 		y.append(thistime)
								
						# 		sensorname = sensorSubstitutions(sensorname)
								
						# 		sensors.append(lastOSCAddress)

						days.append(thisdate)
						hours.append(thistime)
						
						sensorname = sensorSubstitutions(sensorname)
						activations.append(sensorname)
						logs.append(file)

		if extension == ".sc_txt":
			try:
				date, trashtime = name.split("_")
				thisdate = datetime.datetime.strptime(date, "%Y%m%d")
				# thishour = datetime.time.strptime(time, "%H%M%S")
				# print date, time
			except:
				# print e
				# print "ignoring", name
				continue

			f = open(os.path.join(path, file),'r')
			for line in f.readlines():
				# print line
				vals = line.split(',')
				# print vals
				try:				
					timestr = vals[0].lstrip("[ ")
					thistime = datetime.datetime.strptime(timestr, "%H:%M:%S.%f").time()
				except:
					# print e
					# print "ignoring", line
					continue

				sensorname = line[line.rfind("/"):].split(" ")[0].rstrip(",")

				if sensorname not in ignoreaddresses:
					days.append(thisdate)
					hours.append(thistime)
					
					# substitute or transform sensor names
					sensorname = sensorSubstitutions(sensorname)					
					activations.append(sensorname)
					logs.append(file)

		if extension == ".txt":
			try:
				date, trashtime = name.split("_")
				thisdate = datetime.datetime.strptime(date, "%y%m%d")
				thishour = datetime.datetime.strptime(trashtime, "%H%M%S").time()
				# print date, time
			except:
				# print e
				# print "ignoring", name
				continue

			f = open(os.path.join(path, file),'r')

			lastsensor = None
			lasttime = None
			for line in f.readlines():
				# print line
				vals = line.split('\t')
				# print vals

				# check sensor time
				try:				
					timestr = vals[0]

					thistime = datetime.datetime.strptime(timestr, "%H:%M:%S.%f").time()
				except:
					# print e
					# print "ignoring", line

					try:				
						timestr = vals[0]

						thistime = datetime.datetime.strptime(timestr, "%H%M%S.%f").time()
					except:
						# print e
						# print "ignoring", line
						continue


				# check sensor value
				if len(vals)>1:
					oscmsg = vals[1]

					if oscmsg not in ignoreaddresses:
						if oscmsg == "/analogpin":
							# cut out those low sensor readings
							if int(vals[3]) > 500:
								sensorname = vals[4]
							else:
								# print vals[4]
								continue
						elif oscmsg == "/digitalpin":
							sensorname = vals[4]
						elif oscmsg == "/dht11":
							# sensorname = vals[5]
							if float(vals[3]) > 81.0:
								sensorname = vals[5]
							else:
								continue
						elif oscmsg == "/motion":
							sensorname = vals[3]
						elif oscmsg == "/nodeid":
							sensorname = vals[2]
						elif oscmsg == "/temperature":
							sensorname = vals[3]
							if sensorname == "shower":
								continue
							else:
								print(vals)
						elif oscmsg == "/humidity":
							sensorname = vals[3]
						else:
							sensorname = oscmsg
							# continue

						if not sensorname.startswith("/"):
							sensorname = "/"+sensorname

						# # screen for state change or elapsed time
						# if lastsensor != sensorname:
						# 	lastsensor = sensorname
						# 	lasttime = thistime
						# else:
						# 	t2 = datetime.datetime.combine(thisdate, thistime)
						# 	t1 = datetime.datetime.combine(thisdate, lasttime)

						# 	if t2 - t1 < datetime.timedelta(seconds=5):
						# 		continue
							# ignore repeats
							# print file,lastsensor,lasttime
						
						days.append(thisdate)
						hours.append(thistime)	

						sensorname = sensorSubstitutions(sensorname)					
						activations.append(sensorname)
						logs.append(file)

						if sensorname.find("\xff") > 0: 
							print("strange character", file)
	break

print("done.")

print("read",len(activations),"sensor events...")
# plot using matplotlib / seaborn

# plot_sensors(days, hours, activations)
print_sensors(days, hours, activations)

# collapse_days(days, hours, activations)

# data = zip(days, hours, activations, logs)
# print data[:10]

# get_sensor(days, hours, activations, logs, "/microwave")



