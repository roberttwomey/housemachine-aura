#include "ofApp.h"

using namespace cv;
using namespace ofxCv;



const float dyingTime = 1.0;

void Trail::setup(const cv::Rect& track) {
    // color.setHsb(ofRandom(0, 255), 255, 255, 255);
    color.set(255, 0, 0, 255);
    cur = toOf(track).getCenter();
    smooth = cur;
}

void Trail::update(const cv::Rect& track) {
    cur = toOf(track).getCenter();
    smooth.interpolate(cur, .25);
    all.addVertex(smooth);
}

void Trail::kill() {
    float curTime = ofGetElapsedTimef();
    if(startedDying == 0) {
        startedDying = curTime;
    } else if(curTime - startedDying > dyingTime) {
        dead = true;
    }
}

void Trail::draw() {
    ofPushStyle();
    // float size = 16;
    // // ofSetColor(255, 2);
    // if(startedDying) {
    //     ofSetColor(ofColor::red);
    //     size = ofMap(ofGetElapsedTimef() - startedDying, 0, dyingTime, size, 0, true);
    // }
    ofNoFill();
    ofSetColor(color);
    // ofDrawCircle(cur, size);d
    ofSetLineWidth(3);
    all.draw();
    // ofDrawBitmapString(ofToString(label), cur);
    ofPopStyle();
}

void Trail::draw_black() {
    ofPushStyle();
    // float size = 16;
    // // ofSetColor(255, 2);
    // if(startedDying) {
    //     ofSetColor(ofColor::red);
    //     size = ofMap(ofGetElapsedTimef() - startedDying, 0, dyingTime, size, 0, true);
    // }
    // ofNoFill();
    ofSetColor(0);
    // ofDrawCircle(cur, size);
    ofSetLineWidth(0.5);
    all.draw();
    // ofDrawBitmapString(ofToString(label), cur);
    ofPopStyle();
}


//--------------------------------------------------------------
void ofApp::setup(){
    ofSetVerticalSync(true);
    ofEnableAntiAliasing();

    loadXMLSettings("settings.xml");
    bShowThreshold = false;


    // camWidth = 1024;//2048;//1600;//3264; //1280;//  // try to grab at this size.
    // camHeight = 768;//1536;//1200;//2448; //960;//;

    if(bUseCamera) {
        // initialize video
        vidGrabber.setDeviceID(1);
        vidGrabber.initGrabber(camWidth, camHeight);    
        camWidth = vidGrabber.getWidth();
        camHeight = vidGrabber.getHeight();    
    } else {
        // load video file
        vidPlayer.load(videoFile);
        vidPlayer.play();   
        camWidth = vidPlayer.getWidth();
        camHeight = vidPlayer.getHeight();     
    }

    // float now = ofGetElapsedTimef();
    // while (ofGetElapsedTimef() < now + 5.0) {
    //     // do nothing;
    // }


    ofLog(OF_LOG_NOTICE, ofToString(camWidth)+" "+ofToString(camHeight));

    // allocate image frames
    videoTrails.allocate(camWidth, camHeight, OF_PIXELS_RGB);
    videoTexture.allocate(videoTrails);
    segImage.allocate(camWidth, camHeight, OF_IMAGE_GRAYSCALE);

    // allocate fbo for trail image
    trailFbo.allocate(camWidth, camHeight, GL_RGBA);
    trailFbo.begin();
    ofClear(0, 0, 0, 0);
    trailFbo.end();

    // allocate fbo for trail image
    drawingFbo.allocate(camWidth, camHeight, GL_RGB);
    drawingFbo.begin();
    ofClear(255);
    // ofClear(0);
    // ofSetColor(255);
    // ofDrawCircle(camWidth/2, camHeight/2, camHeight/2);
    drawingFbo.end();


    // initialize bgfg
    // bgfg.initialize(cv::Size(camWidth, camHeight), 0, 255);

    // pMOG2 = new BackgroundSubtractorMOG2();

    // initialize contour finder
    // contourFinder.setMinAreaRadius(1);
    // contourFinder.setMaxAreaRadius(500);
    contourFinder.setMinArea(contourMinArea);
    contourFinder.setMaxArea(contourMaxArea);
    contourFinder.setThreshold(bgThresh);

    // wait for half a frame before forgetting something
    tracker.setPersistence(trackPersistence);
    // an object can move up to 50 pixels per frame
    tracker.setMaximumDistance(trackMaxDist);

}

//--------------------------------------------------------------
void ofApp::update(){
    ofBackground(0, 0, 0);

    bool bIsFrameNew;
    if(bUseCamera) {
        vidGrabber.update();
        bIsFrameNew = vidGrabber.isFrameNew();
    } else {
        vidPlayer.update();
        bIsFrameNew = vidPlayer.isFrameNew();
    }    

    if(bIsFrameNew){
        // smooth iamge    
        if(bUseCamera) {
            blur(vidGrabber, blurSize);            
        } else {
            blur(vidPlayer, blurSize);
        };

        // ofxCv::imitate(thresholded, vidGrabber.getPixels());//, CV_8UC1); //CV_8UC3);//

        // do bgfg
        background.setLearningTime(bgLearningTime);//learningTime);
        background.setThresholdValue(bgThresh);//thresholdValue);
        
        if(bUseCamera) {
            background.update(vidGrabber, thresholded);
        } else {
            // background.update(vidPlayer, thresholded);


            Mat cImage, fgmask, shadowLessMask;
            ofxCv::copy(vidPlayer, cImage);
            // ofxCv::imitate(thresholded, vidGrabber.getPixels(), CV_8UC1); //CV_8UC3);//

            // MOG2 example
            // https://github.com/naus3a/ofxCvMOG2/blob/master/src/ofxCvMOG2.cpp
            bgfg.operator()(cImage, fgmask);
            // ofxCv::toOf(fgmask, thresholded);
            ofxCv::threshold(fgmask, shadowLessMask, 254);
            ofxCv::toOf(shadowLessMask, thresholded);
            
        }


        // thresholded.update();
        dilate(thresholded, thresholded, bgDilate);

        // do countour detection
        contourFinder.findContours(thresholded);

        // do tracking
        tracker.track(contourFinder.getBoundingRects());

        const std::vector<unsigned int>& labels = tracker.getCurrentLabels();
        if(labels.size() <= 0) {
            trailFbo.begin();
            ofClear(0, 0, 0, 0);
            trailFbo.end();
        }
    }

}

//--------------------------------------------------------------
void ofApp::draw(){
    ofEnableAlphaBlending();
    ofSetColor(255);
    ofDrawRectangle(0, ofGetWindowHeight()/2.0, ofGetWindowWidth(), ofGetWindowHeight());

    // center images and scale to fill height of screen
    ofPushMatrix();
    float sf = 0.5 * ofGetWindowHeight()/camHeight;
    float xoffset = 0.5*(ofGetWindowWidth()-(camWidth*sf));
    ofTranslate(xoffset, 0);
    ofScale(sf, sf);

    ofTranslate(camXTweak, 0);
    if (bUseCamera) {
        vidGrabber.draw(0, 0, camWidth, camHeight);        
    } else {
        vidPlayer.draw(0, 0, camWidth, camHeight);
    }


    // draw contour lines
    // contourFinder.draw();
    std::vector<ofPolyline> polylines = contourFinder.getPolylines();

    // ofTranslate(-0.5*camWidth*(1.0-300.0/camHeight), 0);
    ofPushStyle();
    ofSetColor(0, 255, 0);
    ofSetLineWidth(4);
    for(std::size_t i = 0; i < polylines.size(); i++)
        polylines[i].draw();
    ofPopStyle();

    // draw trails on both live frame and cumulative drawing
    vector<Trail>& followers = tracker.getFollowers();
    for(int i = 0; i < followers.size(); i++) {
        trailFbo.begin();
        followers[i].draw();
        trailFbo.end();
        drawingFbo.begin();
        followers[i].draw_black();
        drawingFbo.end();
    }

    // draw live trails to screen
    trailFbo.draw(0, 0, camWidth, camHeight);

    // draw thresholded image
    ofTranslate(0, camHeight);

    // draw cumulative drawing to screen
    drawingFbo.draw(0, 0, camWidth, camHeight);


    if(bShowThreshold and thresholded.isAllocated())
        thresholded.draw(0, 0, camWidth, camHeight);
    
    ofPopMatrix();
}

void ofApp::loadXMLSettings(string settingsfile) {
    
    ofxXmlSettings xml;

    xml.loadFile(settingsfile);

    bUseCamera = (xml.getValue("usecamera", 0) > 0);
    bool bFullscreen = (xml.getValue("fullscreen", 0) > 0);
    ofSetFullscreen(bFullscreen);
    // bHideCursor = (xml.getValue("hidecursor", 0) > 0);
    
    // video file input
    videoFile = xml.getValue("videofile", "/Volumes/Work/Projects/housemachine_aura/data/video/overhead_test.mov");
    
    // capture size
    camWidth = xml.getValue("camwidth", 1280);
    camHeight = xml.getValue("camheight", 960);
    camXTweak = xml.getValue("xtweak", 0);

    // bg fg segmentation settings
    bgLearningTime = xml.getValue("bglearningtime", 30);
    bgThresh = xml.getValue("bgthresh", 15);
    bgDilate = xml.getValue("bgdilate", 3);

    // contour tracking settings
    blurSize = xml.getValue("blur", 10.0);
    contourMinArea = xml.getValue("minarea", 600.0);
    contourMaxArea = xml.getValue("maxarea", 30000.0);

    trackPersistence = xml.getValue("trackpersistence", 15);
    trackMaxDist = xml.getValue("trackmaxdist", 50);
    // debug information (text, mouse, thumbnail) //
    // bHideCursor = (xml.getValue("hidecursor", 0) > 0);
    // bDebug = (xml.getValue("debug", 0) > 0);
    // bool bFullscreen = (xml.getValue("fullscreen", 0) > 0);
    // ofSetFullscreen(bFullscreen);
    // screen_width = xml.getValue("screenwidth", screen_width);
    // screen_height = xml.getValue("screenheight", screen_height);

}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){
    if(key == 'r')
        background.reset();
    if(key == 'f')
        ofToggleFullscreen();
    if(key == 't')
        bShowThreshold = !bShowThreshold;
}
//
