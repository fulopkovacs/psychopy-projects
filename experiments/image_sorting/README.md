# Image Sorting Test

## Description
In this experiment the participant is shown images of object and animals in three conditions and has to categorize them.

### Condition 1
- The participant is asked to press the `LEFT` arrow key for animals, the `RIGHT` arrow key for objects.
- Every image is repeated once, they are shown in a random order.
- The participant receives feedback (evaluation of the response + reaction time) after pressing a key.

### Condition 2
- Same as _Condition 1_, except the keys to press for animals and objects are switched.

### Condition 3
- If the image is upside down and depicts an...
  - ..._animal_: `LEFT` arrow key
  - ..._object_: `RIGHT` arrow key.
- If the image is NOT upside down and depicts an...
  - ..._animal_: `RIGHT` arrow key
  - ..._object_: `LEFT` arrow key.
- The images are not repeated.
- There's no feedback after the responses.

## Inputs

The inputs required for the experiment are located in the `data` directory.

  - `input/participant-info-questions.csv`: content of the form, that the participants will be asked to fill before the trials (e.g.: _id_, _age_, _gender_, ...)
  - `input/instructions-condition-1.txt`: the instructions of the first condition
  - `input/instructions-condition-2.txt`: the instructions of the second condition
  - `input/instructions-condition-3.txt`: the instructions of the third condition
  - `input/outro.txt`: the text that is presented after the trials (outro)
  - `input/stimuli-info.csv`: list of the presented images

## Outputs

The outputs created by the experiment are located in the `data` directory.

  - `data/participants-summary.csv`: a summary that contains the form responses of every participant
  - `data/<id>-<data>.csv`: the recorded and evaluated answers of the participant (a filename for `sample_participant` could be: `sample_participant-2021_febr_09_2216.csv`)

## Run the experiment

Instructions can be found [here](https://github.com/fulopkovacs/psychopy-projects#how-to-run-the-experiments).
