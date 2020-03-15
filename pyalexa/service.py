from __future__ import print_function
import random
import boto3


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }




def get_welcome_response():
    """ Message that is sent right when you launch your application
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to BlindSight!"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I'm sorry, I didn't understand you. Come again?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using BlindSight. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass



def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()

def getAge():
    dynamodb=boto3.client('dynamodb')
    mydata=dynamodb.scan(TableName="LatestAlexaTable")
    facedict=mydata['Items'][0]["FaceDict"]
    tectdict=mydata['Items'][0]["TextDict"]
    labeldict=mydata['Items'][0]["LabelDict"]
    finalstringresponse=""
    card_title="Get Age"
    counter = 1

    if len(facedict['M'])>0:


        for face in facedict['M']:
            stringcounter = ""
            agelow=facedict['M'][face]['M']['ageLow']['N']
            agehigh=facedict['M'][face]['M']['ageHigh']['N']
            location=facedict['M'][face]['M']['Location']['S']
            gendervalue=facedict['M'][face]['M']['genderValue']['S']
            if counter == 1:
                stringcounter = "1st"
            elif counter == 2:
                stringcounter = "2nd"
            elif counter == 3:
                stringcounter ="3rd"
            else:
                stringcounter = str(counter)+"th"
            counter+=1
            finalstringresponse = finalstringresponse + "The "+str(stringcounter)+" "+str(gendervalue)+" in the "+str(location)+" appears to be between "+str(agelow)+" and "+str(agehigh)+" years old. "
    else:
        finalstringresponse="There were no faces detected in this image."
    return build_response({}, build_speechlet_response(
        card_title, finalstringresponse, None, False))

def getLabels():
    dynamodb=boto3.client('dynamodb')
    mydata=dynamodb.scan(TableName="LatestAlexaTable")
    facedict=mydata['Items'][0]["FaceDict"]
    tectdict=mydata['Items'][0]["TextDict"]
    labeldict=mydata['Items'][0]["LabelDict"]
    stringcounter = ""
    finalstringresponse=""
    card_title="What's up in this picture"
    counter = 1
    if len(labeldict['M'])>0:

        for label in labeldict['M']:
            seenobject=labeldict['M'][label]['L'][0]['S']
            objectlocation=labeldict['M'][label]['L'][1]['S']
            if counter == 1:
                stringcounter = "1st"
            elif counter == 2:
                stringcounter = "2nd"
            elif counter == 3:
                stringcounter ="3rd"
            else:
                stringcounter = str(counter)+"th"
            counter+=1
            finalstringresponse = finalstringresponse + "There is a "+str(seenobject)+ " in the "+str(objectlocation)+ " of the image. "
    else:
        finalstringresponse="There were no objects detected in that image."
    return build_response({}, build_speechlet_response(
        card_title, finalstringresponse, None, False))

def getEmotion():
    dynamodb=boto3.client('dynamodb')
    mydata=dynamodb.scan(TableName="LatestAlexaTable")
    facedict=mydata['Items'][0]["FaceDict"]
    tectdict=mydata['Items'][0]["TextDict"]
    labeldict=mydata['Items'][0]["LabelDict"]
    finalstringresponse=""
    card_title="Get Emotional Sentiment"
    counter = 1
    if len(facedict['M'])>0:
        for face in facedict['M']:
            stringcounter = ""
            emotion=facedict['M'][face]['M']['emotion']['S']
            emotconf=facedict['M'][face]['M']['emotionConf']['N'][:4]
            location=facedict['M'][face]['M']['Location']['S']
            gendervalue=facedict['M'][face]['M']['genderValue']['S']
            if counter == 1:
                stringcounter = "1st"
            elif counter == 2:
                stringcounter = "2nd"
            elif counter == 3:
                stringcounter ="3rd"
            else:
                stringcounter = str(counter)+"th"
            counter+=1
            finalstringresponse = finalstringresponse + "The "+str(stringcounter)+" "+str(gendervalue)+" in the "+str(location)+" appears to be "+str(emotion)+", and I am " +str(emotconf) + " percent sure on that. "
    else:
        finalstringresponse="There were no faces detected in that image."
    return build_response({}, build_speechlet_response(
        card_title, finalstringresponse, None, False))

def getText():
    dynamodb=boto3.client('dynamodb')
    mydata=dynamodb.scan(TableName="LatestAlexaTable")
    facedict=mydata['Items'][0]["FaceDict"]
    textdict=mydata['Items'][0]["TextDict"]
    labeldict=mydata['Items'][0]["LabelDict"]
    stringcounter = ""
    finalstringresponse=""
    card_title="What's up in this picture"
    counter = 1
    if len(textdict['M']) > 0:
        for text in textdict['M']:
            transcription=textdict['M'][text]['L'][0]['S']
            objectlocation=textdict['M'][text]['L'][1]['S']
            if counter == 1:
                stringcounter = "1st"
            elif counter == 2:
                stringcounter = "2nd"
            elif counter == 3:
                stringcounter ="3rd"
            else:
                stringcounter = str(counter)+"th"
            counter+=1
            finalstringresponse = finalstringresponse + "There is a "+str(transcription)+ " in the "+str(objectlocation)+ " of the image. "
    else:
        finalstringresponse="There was no text detected in the image."
    return build_response({}, build_speechlet_response(
        card_title, finalstringresponse, None, False))



def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AgeIntent":
        return getAge()
    elif intent_name == "EmotionIntent":
        return getEmotion()
    elif intent_name == "AvgAgeByFirstNameIntent":
        pass
    elif intent_name == "FirstNameIntent":
        pass
    elif intent_name == "FirstNameCountIntent":
        pass
    elif intent_name == "GenderIntent":
        pass
    elif intent_name == "LabelsIntent":
        return getLabels()
    elif intent_name == "TextIntent":
        return getText()

    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")


    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
