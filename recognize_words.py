from psychopy import core, visual, event
import random

from Experiment import Experiment


# Create a subclass from Experiment
class WordRecognition(Experiment):
    def __init__(
        self,
        experiment_name: str,
        psychopy_version: str,
        input_filename: str,
        randomize_stimuli: bool,
    ):
        super().__init__(
            experiment_name=experiment_name,
            psychopy_version=psychopy_version,
        )

        self.load_input_from_csv(input_filename=input_filename)
        self.responses = []
        self.clock = core.Clock()

        if randomize_stimuli:
            self.randomize_stimuli()

    def randomize_stimuli(self):
        """
        Randomize the stimuli presentation order.
        """
        rand_stimuli_data = self.stimuli_data
        random.shuffle(rand_stimuli_data)
        self.rand_stimuli_data = rand_stimuli_data

    def present_stimulus(self, stimulus: list):
        """
        Present a single stimulus.
        """
        # Display the stimulus for 200 ms
        word = visual.TextStim(win=self.win, text=stimulus[0])
        word.draw()
        self.win.flip()
        core.wait(0.2)
        self.clock.reset()
        self.win.flip()

    def register_response(self, stimulus: list):
        """
        Register and evaluate the response of the participant to the presented stimulus.
        """
        response = event.waitKeys(keyList=["f", "r"])[0]
        if (response.lower() == "f" and stimulus[1] == "fake") or (
            response.lower() == "r" and stimulus[1] != "fake"
        ):
            result = "correct"
        else:
            result = "incorrect"

        rt = self.clock.getTime()
        self.responses.append([stimulus[0], stimulus[1], result, rt])

    def play_stimuli(self):
        """
        Present the stimuli and register the responses.
        """
        stimuli = self.stimuli_data
        if hasattr(self, "rand_stimuli_data"):
            stimuli = self.rand_stimuli_data

        for stimulus in stimuli:
            self.present_stimulus(stimulus)
            self.register_response(stimulus)


# Pause until there's a keypress
trial = WordRecognition(
    experiment_name="Word recognition",
    psychopy_version="2020.2.10",
    input_filename="stimuli.csv",
    randomize_stimuli=True,
)

# Save participant info
trial.get_participant_info(
    participant_info_csv_filename="participant-info-questions.csv",
    title="Please answer the following questions!",
)

# Create window for the trial
trial.win = visual.Window(
    fullscr=True,
    allowGUI=True,
    winType="pyglet",
    color="black",
)

# display instructions
trial.display_instructions("instructions.txt")

# Play stimuli
trial.play_stimuli()

# Save output
trial.save_output(
    output_csv_header=["word", "condition", "result", "reaction_time"],
    responses=trial.responses,
    participant_name=trial.participant_info["Participant ID:"],
)

# Save participant info to the summary
trial.save_participant_info(filename="participants-summary.csv")

# Display outro
trial.display_outro(outro_filename="outro.txt")
