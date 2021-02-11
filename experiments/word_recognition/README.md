# Word Recognition Test

## Description
In this experiment the participant is shown a series of images for a short amount of time (200 ms each), and has to decide whether the word presented was real (_press the "r" key_), or not (_"n" key_). The responses are evaluated and recorded along with reaction time and other useful pieces of information.

## Inputs

The inputs required for the experiment are located in the `data` directory.

  - `input/participant-info-questions.csv`: content of the form, that the participants will be asked to fill before the trials (e.g.: _id_, _age_, _gender_, ...)
  - `input/instructions.txt`: the instructions of the trial
  - `input/outro.txt`: the text that is presented after the trials (outro)
  - `input/stimuli.csv`: list of the presented words

## Outputs

The outputs created by the experiment are located in the `data` directory.

  - `data/participants-summary.csv`: a summary that contains the form responses of every participant
  - `data/<id>-<data>.csv`: the recorded and evaluated answers of the participant (a filename for `sample_participant` could be: `sample_participant-2021_febr_09_2216.csv`)

## Run the experiment

Instructions can be found [here](https://github.com/fulopkovacs/psychopy-projects#how-to-run-the-experiments).
