## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## New Story

* greet
    - utter_greet
* bot_challenge
    - utter_iamabot
* mood_great
    - utter_happy

## undefined

* Food_Ordering
    - utter_goodbye
* greet
    - utter_greet
* mood_great
    - utter_happy
* Food_Ordering
    - utter_Food_Ordering






## New Story

* greet
    - utter_greet
* mood_great
    - utter_happy
* Food_Ordering
    - utter_Food_Ordering
* deny
    - utter_goodbye




## New Story

* greet
    - utter_greet
* Get_In_Touch
    - utter_happy
* bot_challenge
    - utter_iamabot

