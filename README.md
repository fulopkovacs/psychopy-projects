# [Work in Progress] Experiments Created With `psychopy`

This repo will contain a bundle of experiments created with `psychopy`. Feel free to fork/modify it.

## Experiments

### `word_recognition.py`
In this experiment the participant is show a sequence of images for a short amount of time (200 ms each), and has to decide whether the word presented was fake (_press the "f" key_), or real (_"r" key_). The responses are evaluated and recorded along with reaction time and other useful pieces of information.

- **inputs**:
  - `participant-info-questions.csv`: content of the form, that the participants will be asked to fill before the trials (e.g.: _id_, _age_, _gender_, ...)
  - `instructions.txt`: the instructions of the trial
  - `outro.txt`: the text that is presented after the trials (outro)
  - `stimuli.csv`: list of the presented words
- **outputs**:
  - `data/participants-summary.csv`: a summary that contains the form responses of every participant
  - `data/<id>-<data>.csv`: the recorded and evaluated answers of the participant (the filename for `sample_participant` would be: `sample_participant-2021_febr_09_2216.csv`)
