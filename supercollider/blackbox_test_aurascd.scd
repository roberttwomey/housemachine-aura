// Text logger for Project Amelia / Bricolage, Pittsburgh, PA 2019
//
// by Robert Twomey, robert@roberttwomey.com

// ===============
// TEST ANSI COLORED MESSAGES
// ===============

// connect to text logger rpi
// m = NetAddr("192.168.1.254", 9999)
m = NetAddr("10.1.10.139", 9999)


//--------------

// ansi color references, from:
// https://bluesock.org/~willkg/dev/ansi.html

// 0	normal display
// 1	bold
// 4	underline (mono only)
// 5	blink on
// 7	reverse video on
// 8	nondisplayed (invisible

//  -- foreground --
// 30	black
// 31	red
// 32	green
// 33	yellow
// 34	blue
// 35	magenta
// 36	cyan
// 37	white

// -- background --
// 40	black
// 41	red
// 42	green
// 43	yellow
// 44	blue
// 45	magenta
// 46	cyan
// 47	white

// to print colors do:
// "\x1b[1;"++color_code_above++"m"+message+"\x1b[0m"

m.sendMsg("/amelia", "amelia:", "(white on blue)", "additional information");
m.sendMsg("/alert", "alert:", "(white on red)", "additional information");
m.sendMsg("/sensor", "sensor:", "(white on green)", "additional information", "more information");
m.sendMsg("/log", "testing some text", "more information");


(
m.sendMsg("/log", "\n|\\---/|
| o_o |
 \\_^_/");
)


m.sendMsg("/clear")
m.sendMsg("/up", 3)


# with newline
m.sendMsg("/sensor", "sensor:", "(white on green)", "additional information", "more information\n");


// color changing
m.sendMsg("/log", "good alert message: (red on black) ", "41");
m.sendMsg("/log", "good sensor reading: ", "37;42");
m.sendMsg("/log", "good amelia notification: (white on blue)", "37;44");



// ===============
// BROADCAST ADDRESSES
// ===============
// configure with broadcast addresses
NetAddr.broadcastFlag = true;
m = NetAddr("192.168.1.255", 9999);

m.sendMsg("/setserverip", 192, 168, 1, 10); //blackbox
m.sendMsg("/setserverip", 192, 168, 1, 20); //laptop

m.sendMsg("/writeeeprom");
m.sendMsg("/readeeprom");

m.sendMsg("/getnodeinfo");

// ===============


// ===============
// TEST TEXTUAL LOG
// ===============

// blackbox address
// m = NetAddr("192.168.1.20", 9999);
// NetAddr.broadcastFlag = true;
// m = NetAddr("192.168.1.255", 9999);

(
~messages = [
	"the front door is opened",
	"the front door has closed",
	"someone has thrown some garbage away",
	"someone is looking in the fridge",
	"the washing machine is running",
	"someone is warming something in the microwave",
	"the microwave is done",
	"someone is showering",
	"someone just used the toilet",
	"someone just used the toilet",
	"the back door is open",
	"the back door is closed",
	"someone got into bed",
	"someone got out of bed",
	"the car left",
	"the car is back",
	"the baby is crying",
	"the baby is hungry",
	"the baby is bored",
	"the baby is tired",
	"the dog is eating dinner",
	"the dog is drinking water"];
)
m.sendMsg('/'++~messages.choose()++' ');
m.sendMsg('/'++$\n)

(
~sensornames = [
'/debug', '/table', '/garbage', '/studio', '/bedroomdoor', '/desklamp', '/bed', '/livingroom', '/couch', '/diningroom', '/announce', '/nodeinfo', '/lamp', '/washingmachine', '/print', '/chair2', '/frontdoor', '/chair', '/toaster', '/occupancy', '/bathroomdoor', '/toilet', '/sink', '/basement', '/kitchen', '/fridge'
]
)
m.sendMsg(~sensornames.choose());
// m.sendMsg('/'++$\n)

(
~playbackRoutine = Routine {
	inf.do {
		// m.sendMsg(~sensornames.choose());
		m.sendMsg('/'++~messages.choose());
	// Wait half second before saying we're done
	0.7.rrand(4.0).postln.wait;
		// "done".postln;
	}
}.play;
)

~playbackRoutine.stop()


// ===============
// TEST EVENT RECORDER
// ===============



(
~nums = (0..9,30..37,40..47);
~nums.do{ |i| m.sendMsg("/log", "X", i.asString) };
)
for (0, 47, { |i| m.sendMsg("/log", "X", i.asString)});

(0..5)
// --------------

m.sendMsg("/\\033[0;32mGREEN\\033[0m", 0)
m.sendMsg("\x1b[0;37;40mTEST\x1b[0m", 0)

m.sendMsg("/led", 7, 1); // on
m.sendMsg("/led", 7, 0); // on

m.sendMsg("/analogpin", 1, 100, "/toilet"); // on
m.sendMsg("/led", 7, 1); // on
m.sendMsg("/led", 7, 0); // off

m.sendMsg("/setnodeid", "/toilet");

m.sendMsg("/setserverip", 192, 168, 1, 10); //blackbox
m.sendMsg("/setserverip", 192, 168, 1, 20); //laptop

m.sendMsg("/writeeeprom");
m.sendMsg("/readeeprom");
m.sendMsg("/loaddefaults");
m.sendMsg("/getnodeinfo");

m.sendMsg("/settemperature", 80.0)
m.sendMsg("/sethumidity", 35.0)
m.sendMsg("/getdht")









// OLD STUFF


(
s = Server.default;
s.boot;
~bDoLogging = false;
)


(

// set up log files, and periodic log routine to start new file

~bDoLogging = false;
// ~datapath = "/home/rtwomey/housemachine/data/logs/";
~datapath = "/Users/rtwomey/housemachine/data/logs/";

~logroutine = Routine( {
	inf.do {
		var waitTime = 10.0 * 60;
		var logfilename;

		// open new file
		logfilename = ~datapath++Date.getDate.stamp++".txt";
		~logfile = File(logfilename, "w");

		// start logging
		~bDoLogging = true;

		// log for long time

		waitTime.wait;

		~bDoLogging = false;
		~logfile.close;
	}
}).play();

~startTime = Date.getDate.rawSeconds;
)

~logroutine.free();

(
// OSC responders
~pathkeys = [ \piezo, \chair, \door, \table, \toilet, \washingmachine, \motion, \frontoor, \humidity, \occupancy, \temperature, \shower, \microwave, \announce, \debug, \particleip, \nodeid, \nodeinfo, \testbundle, \digitalpins, \analogpins, \digitalpin, \analogpin, \dht11];

~oscfuncs = Dictionary.new;

~pathkeys.do { |path|
	var thisaddr = '/'++path;
	// path.postln;
	~oscfuncs.put(path,
		[{|msg, time, addr, recvPort|
			var thisDate, thisSeconds, tstampstring, msgstring, addrstring;

			msgstring = msg.join("\t");
			addrstring = [addr.ip, addr.port].join("\t");

			thisDate = Date.getDate;
			thisSeconds = "%.%".format(thisDate.second.asString.padLeft(2, "0"), thisDate.rawSeconds.frac.trunc(1e-4).asString.padRight(6, "0").split($.)[1]);
			tstampstring = thisDate.format("%H:%M:")++thisSeconds;

			// nowSeconds = Date.getDate.rawSeconds - ~startTime;
			// tstampstring =

			// [msg, time, addr, recvPort].postln;
			[tstampstring, msg, addrstring, recvPort].postln;
			// [tstampstring, msg.reverse, addrstring, recvPort].postln;
			~bDoLogging.if {
				~logfile.write( "%\t%\t%\t%\n".format(tstampstring, msgstring, addrstring, recvPort) );
				~logfile.flush();
			};

			},
	thisaddr.asSymbol]);
	thisaddr.postln;
};


// ~oscfuncs.do{ | func | func.remove };
//oscFuncs.postln;

~oscresponders = ();

~oscfuncs.keys.do{ | key |
	var specs, func, addr;

	specs = ~oscfuncs[key];
	# func, addr = specs;
	// specs.postln;
	~oscresponders.put(key, OSCFunc.newMatching(func, addr, recvPort: 9999));

};


)

~logroutine.play()

~logroutine.stop()



// receiving messages from photon
(

~bDoLogging = false;
~oscresponders.do{ | resp | resp.remove };
~oscfuncs.do{ | func | func.remove };
~oscfuncs.postln;
)


// printer stuff
m = NetAddr("192.168.1.10", 9999); //
m.sendMsg("/print", 1);
m.sendMsg("/print", 0);
m.sendMsg("/log", 1);
m.sendMsg("/log", 0);

m = NetAddr("192.168.1.103", 8888);



m.sendMsg("/readapin", 10); // 10 - 16 are A0 - A5

// devices with dictionary
(
~devices=Dictionary.new();

~deviceAddresses = [
	[ \lamp, "192.168.1.30"],
	[ \hotplate, "192.168.1.31", \on, 0, 0, \off, 0, 1],
	[\desklamp, "192.168.1.32", \on, 0, 0, \off, 0, 1]
];

~deviceAddresses.do{ |dev|
	var name, addr;
	name = dev[0];
	addr = dev[1];
	~devices[name]=NetAddr(addr, 8888);
	postln("created netaddr"+name);
};
)

~devices[\hotplate].sendMsg("/setdpin", 0, 0); // on
~devices[\hotplate].sendMsg("/setdpin", 0, 1); // off

~devices[\lamp].sendMsg("/setdpin", 0, 0); // on
~devices[\lamp].sendMsg("/setdpin", 0, 1); // off

~devices[\desklamp].sendMsg("/setdpin", 0, 0); // on
~devices[\desklamp].sendMsg("/setdpin", 0, 1); // off


 store device behaviors
~devices[\lamp].sendMsg("/setserverip", 192, 168, 1, 10);
~devices[\lamp].sendMsg("/setnotify", 0, 1);
~devices[\lamp].sendMsg("/writeeeprom");
~devices[\desklamp].sendMsg("/setserverip", 192, 168, 1, 10);
~devices[\desklamp].sendMsg("/writeeeprom");

// hotplate
m = NetAddr("192.168.1.109", 8888); // hotplate
m.sendMsg("/setdpin", 0, 0); // on
m.sendMsg("/setdpin", 0, 1); // off

// lamp
m = NetAddr("192.168.1.105", 8888); // lamp
m.sendMsg("/setdpin", 0, 0); // on
m.sendMsg("/setdpin", 0, 1); // off

j = Array.series(10);
postln(j[2..])

array
// digital notify
m.sendMsg("/setnotify", 0, 0);
Routine( { (0..15).do { |i| m.sendMsg("/settrigger", i, 0); i.postln; 1.0.wait};}).play
Routine( { (100..115).do { |i| m = NetAddr(format("192.168.1.%", i), 8888); m.sendMsg("/setdpin", 0, 0); i.postln; 0.5.wait};}).play


// analog notify
m.sendMsg("/setnotify", 0, 0);
m.sendMsg("/settrigger", 10, 1);
m.sendMsg("/setthreshold", 10, 2000);
m.sendMsg("/setnotify", 10, 0);
m.sendMsg("/setnotify", 10, 1);

m.sendMsg("/getnodeinfo");
m.sendMsg("/getnotify")
m.sendMsg("/getthreshold")
m.sendMsg("/gettrigger")
m.sendMsg("/getnodeid")

Date.getDate.rawSeconds.postln; Date.getDate.secStamp.postln; Date.getDate.rawSeconds.frac.trunc(1e-4).asString.padRight(6, "0").split($.)[1].postln;
m.disconnect()

n = NetAddr("192.168.1.100", 9999);
n.sendMsg("/chair", 0);

OSCFunc.trace(true, false)
OSCFunc.trace(true, true)
OSCFunc.trace(false, true)

"ssh pi@narrator.local 'festival --tts soft_rains.txt'".unixCmdGetStdOut
