#include "ofMain.h"
#include "ofApp.h"

//========================================================================
int main( ){
	// ofSetupOpenGL(400, 600, OF_WINDOW);			// <-------- setup the GL context

	ofGLFWWindowSettings settings;
	settings.setGLVersion(4, 1);
	settings.multiMonitorFullScreen = true;
	settings.windowMode = OF_FULLSCREEN;
	ofCreateWindow(settings);
	// this kicks off the running of my app
	// can be OF_WINDOW or OF_FULLSCREEN
	// pass in width and height too:
	ofRunApp(new ofApp());

}
