#pragma once

#include "ofMain.h"
#include "ofxCv.h"
#include "ofxXmlSettings.h"



class Trail : public ofxCv::RectFollower {
protected:
	ofColor color;
	ofVec2f cur, smooth;
	float startedDying;
	ofPolyline all;
public:
	Trail()
		:startedDying(0) {
	}
	void setup(const cv::Rect& track);
	void update(const cv::Rect& track);
	void kill();
	void draw();
	void draw_black();

};


class ofApp : public ofBaseApp{

	public:
		void setup();
		void update();
		void draw();

		void keyPressed(int key);

	    void loadXMLSettings(string settingsfile);

        ofVideoGrabber vidGrabber;
        ofVideoPlayer vidPlayer;
        ofPixels videoTrails;
        ofTexture videoTexture;
        ofImage segImage;
        ofFbo trailFbo;
        ofFbo drawingFbo;

        // program state
        bool bShowThreshold;
        
        // parameters set from xml file
        bool bUseCamera;
        string videoFile;

        float camWidth;
        float camHeight;
        float camXTweak;
        
        float contourMinArea;
        float contourMaxArea;
        
        float blurSize;
        
        float bgLearningTime;
        float bgThresh;
        float bgDilate;

		float trackPersistence;
		float trackMaxDist;

        cv::BackgroundSubtractorMOG2 bgfg;

    	// ofxCv running background
    	ofxCv::RunningBackground background;
		ofImage thresholded;
	    // cv::Mat fgmask;


		// ofxCv contour finder
        ofxCv::ContourFinder contourFinder;
    	ofxCv::RectTrackerFollower<Trail> tracker;
};
